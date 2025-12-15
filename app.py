from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import os
import zipfile
import uuid
import json
from analyzer import analyze_images, extract_design_dna, identify_pattern, segment_image, segment_columns
from ocr import extract_texts
from ai_refine import refine_and_generate_wp
from wp_theme.prompts.runner import ThemeBuilder
from dotenv import load_dotenv
import threading
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
TEMP_OUT_DIR = os.path.join(BASE_DIR, 'temp_out')
DOC_INFO_PATH = os.path.join(BASE_DIR, 'docs', 'info.md')
ENV_PATH = os.path.join(BASE_DIR, '.env')

app = Flask(__name__)
app.secret_key = 'img2html-secret'
# Límite de tamaño de carga (100 MB)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
load_dotenv()
try:
    if not os.path.isfile(os.path.join(BASE_DIR, '.env')):
        with open(os.path.join(BASE_DIR, '.env'), 'w', encoding='utf-8') as f:
            f.write('')
except Exception:
    pass

ALLOWED_EXTENSIONS = {'.zip'}
SAFE_IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}
FONT_EXTS = {'.ttf', '.otf', '.woff', '.woff2'}
SAFE_TEXT_EXTS = {'.txt', '.md', '.markdown'}
SAFE_XML_EXTS = {'.xml'}
MAX_ZIP_FILES = 500
MAX_ZIP_UNCOMPRESSED = 300 * 1024 * 1024  # 300 MB
PROGRESS = {}

def allowed_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS

def _sanitize_slug(text: str):
    slug = ''.join(ch if ch.isalnum() or ch in ('-', '_') else '-' for ch in (text or ''))
    slug = slug.strip('-_').lower()
    if not slug:
        slug = 'img2html-theme'
    return slug[:64]

def _safe_extract_zip(zf: zipfile.ZipFile, dest_dir: str):
    total_uncompressed = 0
    count = 0
    for info in zf.infolist():
        name = info.filename
        # Evitar traversal
        if '..' in name or name.startswith('/') or name.startswith('\\'):
            continue
        ext = os.path.splitext(name)[1].lower()
        # Solo extraer contenidos que podamos aprovechar: imágenes, fuentes, texto y XML
        if (
            ext not in SAFE_IMAGE_EXTS
            and ext not in FONT_EXTS
            and ext not in SAFE_TEXT_EXTS
            and ext not in SAFE_XML_EXTS
        ):
            continue
        total_uncompressed += getattr(info, 'file_size', 0)
        count += 1
        if count > MAX_ZIP_FILES or total_uncompressed > MAX_ZIP_UNCOMPRESSED:
            break
        target_path = os.path.abspath(os.path.join(dest_dir, name))
        if not target_path.startswith(os.path.abspath(dest_dir)):
            continue
        # Crear directorio padre si no existe
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with zf.open(info) as rf, open(target_path, 'wb') as wf:
            wf.write(rf.read())

@app.template_filter('basename')
def basename_filter(p):
    return os.path.basename(p)

@app.route('/', methods=['GET'])
def index():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    runtime_path = os.path.join(base_dir, 'wp_theme', 'prompts', 'runtime.json')
    runtime = {}
    try:
        with open(runtime_path, 'r', encoding='utf-8') as f:
            runtime = json.load(f)
    except Exception:
        runtime = {}
    gemini_keys = ['GOOGLE_API_KEY']
    for rm in (runtime.get('remote_models') or []):
        if rm.get('provider') == 'google' and rm.get('enabled'):
            for name in (rm.get('tokens') or []):
                gemini_keys.append(name)
    has_gemini = any(os.environ.get(k) for k in gemini_keys)
    openai_keys = ['OPENAI_API_KEY']
    for rm in (runtime.get('remote_models') or []):
        if rm.get('provider') == 'openai' and rm.get('enabled'):
            for name in (rm.get('tokens') or []):
                openai_keys.append(name)
    has_openai = any(os.environ.get(k) for k in openai_keys)
    # Detectar si hay modelos locales configurados (LM Studio / Ollama)
    local_models = runtime.get('local_models') or []
    has_local = any(bool(lm.get('enabled')) for lm in local_models)
    local_names = [lm.get('name') or lm.get('id') for lm in local_models if lm.get('enabled')]
    ollama_endpoint = os.environ.get('OLLAMA_ENDPOINT') or 'http://localhost:11434/api/generate'
    cred_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') or ''
    cred_exists = bool(cred_path and os.path.isfile(cred_path))
    cred_valid = False
    if cred_exists:
        try:
            with open(cred_path, 'r', encoding='utf-8') as f:
                obj = json.load(f)
            cred_valid = _is_valid_service_account_json(obj)
        except Exception:
            cred_valid = False
    env = {
        'gemini': has_gemini,
        'openai': has_openai,
        'local': has_local,
        'local_names': [n for n in local_names if n],
        'ollama_endpoint': ollama_endpoint,
        'vision_path': cred_path,
        'vision_exists': cred_exists,
        'vision_valid': cred_valid
    }
    return render_template('index.html', env=env)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('zipfile')
    theme_name = request.form.get('theme_name', '').strip() or 'Img2HTML AI Theme'
    theme_slug = _sanitize_slug(request.form.get('theme_slug', '').strip() or '')
    theme_description = request.form.get('theme_description', '').strip() or 'Tema de bloques generado y refinado con IA desde imágenes'
    theme_version = request.form.get('theme_version', '').strip() or '1.0.0'
    theme_author = request.form.get('theme_author', '').strip() or ''
    theme_uri = request.form.get('theme_uri', '').strip() or ''
    theme_textdomain = request.form.get('theme_textdomain', '').strip() or ''
    theme_tags = request.form.get('theme_tags', '').strip() or ''
    theme_license = request.form.get('theme_license', '').strip() or 'GPLv2 or later'
    theme_screenshot_file = request.files.get('theme_screenshot')
    css_framework = request.form.get('css_framework', 'tailwind')  # tailwind, bootstrap, none
    google_api_key = request.form.get('google_api_key') or ''
    enable_slicing = request.form.get('enable_slicing') or ''
    precise_slicing = request.form.get('precise_slicing') or ''
    save_env = request.form.get('save_env') or ''
    enable_seo = request.form.get('enable_seo') or ''
    google_application_credentials = request.form.get('google_application_credentials') or ''
    google_application_credentials_file = request.files.get('google_application_credentials_file')
    if not file or file.filename == '':
        flash('Adjunta un archivo ZIP válido')
        return redirect(url_for('index'))
    if not allowed_file(file.filename):
        flash('El archivo debe ser un ZIP')
        return redirect(url_for('index'))
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    batch_id = str(uuid.uuid4())
    batch_dir = os.path.join(UPLOAD_DIR, batch_id)
    os.makedirs(batch_dir, exist_ok=True)
    zip_path = os.path.join(batch_dir, secure_filename(file.filename))
    file.save(zip_path)
    with zipfile.ZipFile(zip_path, 'r') as zf:
        _safe_extract_zip(zf, batch_dir)
    images = []
    from PIL import Image as PILImage
    for root, _, files in os.walk(batch_dir):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in SAFE_IMAGE_EXTS:
                p = os.path.join(root, f)
                try:
                    im = PILImage.open(p); im.verify()
                    images.append(p)
                except Exception:
                    pass
    if not images:
        flash('El ZIP no contiene imágenes válidas')
        return redirect(url_for('index'))
    plan = analyze_images(images)
    for s in plan['sections']:
        s['pattern'] = identify_pattern(s)
        try:
            from analyzer import identify_pattern_variant
            s['pattern_variant'] = identify_pattern_variant(s)
        except Exception:
            s['pattern_variant'] = ''
        try:
            from analyzer import identify_pattern_variant
            s['pattern_variant'] = identify_pattern_variant(s)
        except Exception:
            s['pattern_variant'] = ''
    if google_api_key and save_env:
        _update_env_file(ENV_PATH, 'GOOGLE_API_KEY', google_api_key)
    if google_application_credentials:
        try:
            if os.path.isfile(google_application_credentials):
                with open(google_application_credentials, 'r', encoding='utf-8') as f:
                    obj = json.load(f)
                if not _is_valid_service_account_json(obj):
                    flash('El archivo de credenciales indicado no parece ser un Service Account válido')
                    google_application_credentials = ''
            else:
                flash('La ruta de credenciales indicada no existe')
                google_application_credentials = ''
        except Exception:
            flash('No se pudo leer el archivo de credenciales indicado')
            google_application_credentials = ''
        if google_application_credentials and save_env:
            _update_env_file(ENV_PATH, 'GOOGLE_APPLICATION_CREDENTIALS', google_application_credentials)
    if google_application_credentials_file and getattr(google_application_credentials_file, 'filename', ''):
        try:
            data = google_application_credentials_file.read()
            obj = json.loads(data.decode('utf-8'))
            if _is_valid_service_account_json(obj):
                target_path = os.path.join(BASE_DIR, 'service-account.json')
                with open(target_path, 'wb') as wf:
                    wf.write(data)
                google_application_credentials = target_path
                if save_env:
                    _update_env_file(ENV_PATH, 'GOOGLE_APPLICATION_CREDENTIALS', target_path)
            else:
                flash('El JSON subido no es un Service Account válido')
        except Exception:
            flash('No se pudo procesar el archivo de credenciales subido')
    # Guardar screenshot si se subió
    screenshot_path = None
    if theme_screenshot_file and theme_screenshot_file.filename:
        try:
            from werkzeug.utils import secure_filename
            screenshot_ext = os.path.splitext(theme_screenshot_file.filename)[1].lower()
            if screenshot_ext in {'.png', '.jpg', '.jpeg', '.webp'}:
                screenshot_filename = f'screenshot{screenshot_ext}'
                screenshot_path = os.path.join(batch_dir, screenshot_filename)
                theme_screenshot_file.save(screenshot_path)
        except Exception as e:
            print(f"Error al guardar screenshot: {e}")
    
    request.environ['img2html_batch_dir'] = batch_dir
    request.environ['img2html_plan'] = plan
    request.environ['img2html_theme_name'] = theme_name
    request.environ['img2html_theme_slug'] = theme_slug or _sanitize_slug(theme_name)
    request.environ['img2html_theme_description'] = theme_description
    request.environ['img2html_theme_version'] = theme_version
    request.environ['img2html_theme_author'] = theme_author
    request.environ['img2html_theme_uri'] = theme_uri
    request.environ['img2html_theme_textdomain'] = theme_textdomain
    request.environ['img2html_theme_tags'] = theme_tags
    request.environ['img2html_theme_license'] = theme_license
    request.environ['img2html_theme_screenshot'] = screenshot_path
    request.environ['img2html_css_framework'] = css_framework
    request.environ['img2html_enable_seo'] = bool(enable_seo)
    return render_template('plan.html', plan=plan, batch_id=batch_id, theme_name=theme_name, theme_slug=theme_slug, theme_description=theme_description, theme_version=theme_version, theme_author=theme_author, theme_uri=theme_uri, theme_textdomain=theme_textdomain, theme_tags=theme_tags, theme_license=theme_license, css_framework=css_framework, google_api_key=google_api_key, enable_slicing=enable_slicing, precise_slicing=precise_slicing, save_env=save_env, google_application_credentials=google_application_credentials)

def _set_progress(batch_id, percent, message):
    try:
        PROGRESS.setdefault(batch_id, {})
        PROGRESS[batch_id]['percent'] = int(max(0, min(100, percent)))
        PROGRESS[batch_id]['message'] = str(message or '')
        PROGRESS[batch_id]['ready'] = bool(PROGRESS[batch_id].get('ready'))
    except Exception:
        pass

@app.route('/progress/<batch_id>', methods=['GET'])
def progress_status(batch_id):
    st = PROGRESS.get(batch_id) or {'percent': 0, 'message': 'Esperando...', 'ready': False}
    return app.response_class(response=json.dumps(st), status=200, mimetype='application/json')

@app.route('/result/<batch_id>', methods=['GET'])
def conversion_result(batch_id):
    st = PROGRESS.get(batch_id) or {}
    used_ai = bool(st.get('used_ai'))
    provider = st.get('provider') or ''
    ocr_provider = st.get('ocr_provider') or ''
    saved_env = bool(st.get('saved_env'))
    return render_template('done.html', output_dir='temp_out', theme_dir='wp_theme', used_ai=used_ai, saved_env=saved_env, provider=provider, ocr_provider=ocr_provider)

def _do_convert_async(ctx):
    batch_id = ctx.get('batch_id')
    theme_name = ctx.get('theme_name', 'Img2HTML AI Theme')
    theme_slug = ctx.get('theme_slug', '')
    theme_description = ctx.get('theme_description', 'Tema de bloques generado y refinado con IA desde imágenes')
    theme_version = ctx.get('theme_version', '1.0.0')
    theme_author = ctx.get('theme_author', '')
    theme_uri = ctx.get('theme_uri', '')
    theme_textdomain = ctx.get('theme_textdomain', '')
    theme_tags = ctx.get('theme_tags', '')
    theme_license = ctx.get('theme_license', 'GPLv2 or later')
    css_framework = ctx.get('css_framework', 'tailwind')
    google_api_key = ctx.get('google_api_key') or ''
    enable_slicing = ctx.get('enable_slicing') or ''
    precise_slicing = ctx.get('precise_slicing') or ''
    enable_seo = bool(ctx.get('enable_seo'))
    save_env = ctx.get('save_env') or ''
    google_application_credentials = ctx.get('google_application_credentials') or ''
    _set_progress(batch_id, 5, 'Inicializando conversión')
    try:
        batch_dir = os.path.join(UPLOAD_DIR, batch_id)
        images = []
        fonts = []
        text_files = []
        xml_files = []
        for root, _, files in os.walk(batch_dir):
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                full = os.path.join(root, f)
                if ext in SAFE_IMAGE_EXTS:
                    images.append(full)
                elif ext in FONT_EXTS:
                    fonts.append(full)
                elif ext in SAFE_TEXT_EXTS:
                    text_files.append(full)
                elif ext in SAFE_XML_EXTS:
                    xml_files.append(full)
        _set_progress(batch_id, 10, 'Cargando imágenes')
        plan = analyze_images(images)
        for s in plan['sections']:
            s['pattern'] = identify_pattern(s)
        _set_progress(batch_id, 20, 'Detectando patrones y secciones')
        
        # Análisis visual profundo con Qwen2-VL (opcional)
        try:
            from analyzer import enhance_section_with_vision
            use_vision = os.environ.get('USE_VISION_ANALYSIS', 'true').lower() == 'true'
            if use_vision:
                _set_progress(batch_id, 22, 'Análisis visual profundo')
                for s in plan['sections']:
                    try:
                        s = enhance_section_with_vision(s, use_qwen2vl=True)
                    except Exception:
                        pass
        except Exception:
            pass
        
        dna = extract_design_dna(images)
        _set_progress(batch_id, 30, 'Extrayendo paleta DNA')
        try:
            ocr_texts, ocr_provider = extract_texts(images)
        except Exception:
            ocr_texts, ocr_provider = ({}, '')
        _set_progress(batch_id, 40, f'OCR: {ocr_provider or "N/A"}')
        # Exportar contenido WXR (para importador de contenidos)
        try:
            _export_wxr(TEMP_OUT_DIR, plan, ocr_texts)
        except Exception:
            pass
        os.makedirs(TEMP_OUT_DIR, exist_ok=True)
        assets_dir = os.path.join(TEMP_OUT_DIR, 'assets')
        os.makedirs(assets_dir, exist_ok=True)
        copied = []
        for section in plan['sections']:
            for img in section['images']:
                name = os.path.basename(img)
                dst = os.path.join(assets_dir, name)
                if not os.path.isfile(dst):
                    with open(img, 'rb') as rf, open(dst, 'wb') as wf:
                        wf.write(rf.read())
                copied.append(name)
            try:
                from PIL import Image as PILImage
                if section.get('images'):
                    p0 = section['images'][0]
                    im = PILImage.open(p0)
                    w, h = im.size
                    ratio = h / float(max(1, w))
                    if enable_slicing or ratio >= 1.5:
                        segs = segment_image(p0, assets_dir, precise=bool(precise_slicing))
                        if segs:
                            layout_rows = []
                            images_flat = []
                            for sp in segs:
                                copied.append(os.path.basename(sp))
                                cols = segment_columns(sp, assets_dir, precise=bool(precise_slicing))
                                if cols:
                                    widths = []
                                    total_w = 0
                                    for c in cols:
                                        try:
                                            cim = PILImage.open(c)
                                            w2, _ = cim.size
                                            widths.append(w2)
                                            total_w += w2
                                        except Exception:
                                            widths.append(0)
                                    ratios = []
                                    ratios_percent = []
                                    if total_w > 0:
                                        ratios = [round(w2/float(total_w), 3) for w2 in widths]
                                        ratios_percent = [int(round(r*100)) for r in ratios]
                                    row = {
                                        'segment': os.path.basename(sp),
                                        'columns': [os.path.basename(c) for c in cols],
                                        'ratios': ratios,
                                        'ratios_percent': ratios_percent
                                    }
                                    layout_rows.append(row)
                                    for c in cols:
                                        images_flat.append(c)
                                        copied.append(os.path.basename(c))
                            if images_flat:
                                section['images'] = images_flat
                            else:
                                section['images'] = segs
                            section['segments'] = [os.path.basename(s) for s in segs]
                            if layout_rows:
                                section['layout_rows'] = layout_rows
                    section['pattern'] = identify_pattern(section)
            except Exception:
                pass
        _set_progress(batch_id, 65, 'Generando HTML estático')
        info_md = ''
        if os.path.isfile(DOC_INFO_PATH):
            try:
                with open(DOC_INFO_PATH, 'r', encoding='utf-8') as f:
                    info_md = f.read()
            except Exception:
                info_md = ''
        # Añadir información adicional proveniente de archivos de texto/XML del ZIP
        if text_files or xml_files:
            extra_sections = []
            if text_files:
                extra_sections.append("## Contenido de texto detectado en el ZIP")
                for tf in text_files:
                    try:
                        with open(tf, 'r', encoding='utf-8', errors='ignore') as rf:
                            snippet = rf.read(4000)
                        extra_sections.append(f"### {os.path.basename(tf)}\n\n{snippet}\n")
                    except Exception:
                        continue
            if xml_files:
                extra_sections.append("## Archivos XML detectados en el ZIP")
                for xf in xml_files:
                    base = os.path.basename(xf)
                    # No volcamos XML completo para no inflar el prompt; sólo un aviso
                    extra_sections.append(f"- {base}")
            if extra_sections:
                info_md = (info_md or '') + "\n\n" + "\n".join(extra_sections)
        html_path = os.path.join(TEMP_OUT_DIR, 'index.html')
        css_path = os.path.join(TEMP_OUT_DIR, 'styles.css')
        title = plan['title']
        sections_html = []
        section_files = []
        for idx, section in enumerate(plan['sections']):
            section_file = f"{section['slug']}.html"
            section_files.append(section_file)
            file_name = os.path.join(TEMP_OUT_DIR, section_file)
            html_file = open(file_name, 'w', encoding='utf-8')
            paragraph_texts = []
            for p in section['images']:
                t = ocr_texts.get(p, '')
                if t:
                    paragraph_texts.append(t)
            paragraph = '\n\n'.join(paragraph_texts) if paragraph_texts else ''
            paragraph = paragraph.replace('\n\n', '<br/><br/>')
            prev_link = ''
            if idx > 0:
                prev_chapter_file = f"{plan['sections'][idx-1]['slug']}.html"
                prev_link = f'<p><a href="{prev_chapter_file}">Anterior</a></p>'
            next_link = ''
            if idx < len(plan['sections']) - 1:
                next_chapter_file = f"{plan['sections'][idx+1]['slug']}.html"
                next_link = f'<p><a href="{next_chapter_file}">Siguiente</a></p>'
            content = f"""
<html>
  <head>
    <link rel=\"stylesheet\" href=\"styles.css\">
  </head>
  <body>
    <div>
      <h1>{section['label']}</h1>
      <p>{paragraph}</p>
      {prev_link}
      {next_link}
    </div>
  </body>
</html>
"""
            html_file.write(content)
            html_file.close()
            imgs_html = ''.join([f'<img src="assets/{os.path.basename(p)}" alt="{section["name"]}">' for p in section['images']])
            sections_html.append(f'<section id="{section["slug"]}"><h2>{section["label"]}</h2><p><a href="{section_file}">Abrir sección</a></p>{imgs_html}</section>')
        html_content = f"""
<!doctype html>
<html lang=\"es\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n  <meta name=\"description\" content=\"Sitio generado desde imágenes\">\n  <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">\n  <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>\n  <link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap\" rel=\"stylesheet\">\n  <link rel=\"stylesheet\" href=\"styles.css\">\n  <title>{title}</title>
</head>
<body>
  <header class=\"site-header\"><div class=\"container\"><h1>{title}</h1></div></header>
  <main class=\"site-main\"><div class=\"container\">
    {''.join(sections_html)}
  </div></main>
  <footer class=\"site-footer\"><div class=\"container\">Generado con img2html</div></footer>
  <script type=\"application/json\" id=\"img2html-plan\">{plan}</script>
  <script type=\"application/json\" id=\"img2html-info\">{info_md}</script>
</body>
</html>
"""
        with open(html_path, 'w', encoding='utf-8') as hf:
            hf.write(html_content)
        css_content = """
:root { --bg: #0b0c0f; --fg: #ffffff; --muted: #a3a3a3; --primary: #4f46e5; }
* { box-sizing: border-box }
html, body { height: 100% }
body { margin: 0; background: var(--bg); color: var(--fg); font-family: 'Inter', system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif }
.container { width: min(1100px, 92%); margin: 0 auto; padding: 24px }
.site-header, .site-footer { background: #121318 }
h1 { font-size: 28px; margin: 0 }
h2 { font-size: 22px; margin: 24px 0 12px }
section { padding: 16px 0; border-top: 1px solid #1f2330 }
img { max-width: 100%; display: block; border-radius: 8px; margin: 8px 0 }
"""
        with open(css_path, 'w', encoding='utf-8') as cf:
            cf.write(css_content)
        _set_progress(batch_id, 80, 'Construyendo tema FSE')
        wp_theme_dir = os.path.join(BASE_DIR, 'wp_theme')
        os.makedirs(wp_theme_dir, exist_ok=True)
        try:
            if google_api_key:
                os.environ['GOOGLE_API_KEY'] = google_api_key
                if save_env:
                    _update_env_file(ENV_PATH, 'GOOGLE_API_KEY', google_api_key)
            if google_application_credentials:
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_application_credentials
                if save_env:
                    _update_env_file(ENV_PATH, 'GOOGLE_APPLICATION_CREDENTIALS', google_application_credentials)
            builder = ThemeBuilder(output_dir=wp_theme_dir, context=dna)
            builder.bootstrap()
            builder.run_prompt('01_theme_json_full.json')
            builder.run_prompt('52_template_parts_catalog.json')
            builder.run_prompt('51_templates_catalog.json')
            builder.run_prompt('53_patterns_catalog.json')
            
            # Construcción mejorada del tema
            try:
                from theme_builder import build_complete_theme, generate_theme_screenshot
                from blocks_builder import setup_css_framework, create_custom_blocks
                build_complete_theme(
                wp_theme_dir, 
                plan, 
                dna, 
                images, 
                theme_name, 
                theme_description, 
                theme_slug, 
                css_framework,
                theme_version=ctx.get('theme_version', '1.0.0'),
                theme_author=ctx.get('theme_author', ''),
                theme_uri=ctx.get('theme_uri', ''),
                theme_textdomain=ctx.get('theme_textdomain', ''),
                theme_tags=ctx.get('theme_tags', ''),
                theme_license=ctx.get('theme_license', 'GPLv2 or later')
            )
                # Configurar framework CSS
                setup_css_framework(wp_theme_dir, css_framework)
                try:
                    from theme_builder import apply_typography_and_spacing, update_theme_json_colors
                    apply_typography_and_spacing(wp_theme_dir, dna, plan)
                    update_theme_json_colors(wp_theme_dir, dna)
                except Exception as _e:
                    pass
                # Crear bloques personalizados (con prefijo BEM desde theme_slug)
                create_custom_blocks(wp_theme_dir, css_framework, plan, theme_slug)
                # Generar screenshot SVG
                generate_theme_screenshot(wp_theme_dir, plan, dna, theme_name, theme_description)
                # SEO básico opcional
                if enable_seo:
                    _enable_seo_meta(wp_theme_dir)
            except Exception as e:
                print(f"Error en construcción del tema: {e}")
                import traceback
                traceback.print_exc()
            
            result = refine_and_generate_wp(TEMP_OUT_DIR, info_md, plan, wp_theme_dir, images=images, dna=dna)
            used_ai = bool(result.get('used_ai')) if isinstance(result, dict) else False
            provider = (result.get('provider') if isinstance(result, dict) else '') or ''

            # Integrar fuentes personalizadas incluidas en el ZIP (si las hay)
            try:
                _integrate_fonts_into_theme(wp_theme_dir, fonts)
            except Exception:
                pass
        except Exception:
            used_ai = False
            provider = ''
        PROGRESS.setdefault(batch_id, {})
        PROGRESS[batch_id]['used_ai'] = used_ai
        PROGRESS[batch_id]['provider'] = provider
        PROGRESS[batch_id]['ocr_provider'] = ocr_provider
        PROGRESS[batch_id]['saved_env'] = bool(save_env)
        PROGRESS[batch_id]['ready'] = True
        _set_progress(batch_id, 100, 'Conversión completada')
    except Exception as e:
        _set_progress(batch_id, 100, 'Error en conversión')

@app.route('/start_convert', methods=['POST'])
def start_convert():
    batch_id = request.form.get('batch_id')
    ctx = {
        'batch_id': batch_id,
        'theme_name': request.form.get('theme_name', '').strip() or 'Img2HTML AI Theme',
        'theme_slug': request.form.get('theme_slug', '').strip() or '',
        'theme_description': request.form.get('theme_description', '').strip() or 'Tema de bloques generado y refinado con IA desde imágenes',
        'theme_version': request.form.get('theme_version', '').strip() or '1.0.0',
        'theme_author': request.form.get('theme_author', '').strip() or '',
        'theme_uri': request.form.get('theme_uri', '').strip() or '',
        'theme_textdomain': request.form.get('theme_textdomain', '').strip() or '',
        'theme_tags': request.form.get('theme_tags', '').strip() or '',
        'theme_license': request.form.get('theme_license', '').strip() or 'GPLv2 or later',
        'css_framework': request.form.get('css_framework', 'tailwind'),
        'google_api_key': request.form.get('google_api_key') or '',
        'enable_slicing': request.form.get('enable_slicing') or '',
        'precise_slicing': request.form.get('precise_slicing') or '',
        'save_env': request.form.get('save_env') or '',
        'google_application_credentials': request.form.get('google_application_credentials') or '',
        'enable_seo': request.form.get('enable_seo') or ''
    }
    _set_progress(batch_id, 1, 'Preparando...')
    t = threading.Thread(target=_do_convert_async, args=(ctx,), daemon=True)
    t.start()
    return redirect(url_for('progress_ui', batch_id=batch_id))

@app.route('/progress_ui')
def progress_ui():
    batch_id = request.args.get('batch_id') or ''
    return render_template('progress.html', batch_id=batch_id)

@app.route('/convert', methods=['POST'])
def convert():
    batch_id = request.form.get('batch_id')
    theme_name = request.form.get('theme_name', '').strip() or 'Img2HTML AI Theme'
    theme_slug = request.form.get('theme_slug', '').strip() or ''
    theme_description = request.form.get('theme_description', '').strip() or 'Tema de bloques generado y refinado con IA desde imágenes'
    css_framework = request.form.get('css_framework', 'tailwind')
    google_api_key = request.form.get('google_api_key') or ''
    enable_slicing = request.form.get('enable_slicing') or ''
    precise_slicing = request.form.get('precise_slicing') or ''
    save_env = request.form.get('save_env') or ''
    enable_seo = request.form.get('enable_seo') or ''
    google_application_credentials = request.form.get('google_application_credentials') or ''
    if not batch_id:
        flash('Falta el identificador del lote')
        return redirect(url_for('index'))
    batch_dir = os.path.join(UPLOAD_DIR, batch_id)
    if not os.path.isdir(batch_dir):
        flash('El lote indicado no existe')
        return redirect(url_for('index'))
    images = []
    fonts = []
    text_files = []
    xml_files = []
    for root, _, files in os.walk(batch_dir):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            full = os.path.join(root, f)
            if ext in SAFE_IMAGE_EXTS:
                images.append(full)
            elif ext in FONT_EXTS:
                fonts.append(full)
            elif ext in SAFE_TEXT_EXTS:
                text_files.append(full)
            elif ext in SAFE_XML_EXTS:
                xml_files.append(full)
    if not images:
        flash('El lote no contiene imágenes válidas')
        return redirect(url_for('index'))
    plan = analyze_images(images)
    for s in plan['sections']:
        s['pattern'] = identify_pattern(s)
        try:
            from analyzer import identify_pattern_variant
            s['pattern_variant'] = identify_pattern_variant(s)
        except Exception:
            s['pattern_variant'] = ''
    dna = extract_design_dna(images)
    try:
        ocr_texts, ocr_provider = extract_texts(images)
    except Exception:
        ocr_texts, ocr_provider = ({}, '')
    # Exportar contenido WXR (para importador de contenidos)
    try:
        _export_wxr(TEMP_OUT_DIR, plan, ocr_texts)
    except Exception:
        pass
    os.makedirs(TEMP_OUT_DIR, exist_ok=True)
    assets_dir = os.path.join(TEMP_OUT_DIR, 'assets')
    os.makedirs(assets_dir, exist_ok=True)
    copied = []
    for section in plan['sections']:
        for img in section['images']:
            name = os.path.basename(img)
            dst = os.path.join(assets_dir, name)
            if not os.path.isfile(dst):
                with open(img, 'rb') as rf, open(dst, 'wb') as wf:
                    wf.write(rf.read())
            copied.append(name)
        try:
            from PIL import Image as PILImage
            if section.get('images'):
                p0 = section['images'][0]
                im = PILImage.open(p0)
                w, h = im.size
                ratio = h / float(max(1, w))
                if enable_slicing or ratio >= 1.5:
                    segs = segment_image(p0, assets_dir, precise=bool(precise_slicing))
                    if segs:
                        layout_rows = []
                        images_flat = []
                        for sp in segs:
                            copied.append(os.path.basename(sp))
                            cols = segment_columns(sp, assets_dir, precise=bool(precise_slicing))
                            if cols:
                                widths = []
                                total_w = 0
                                for c in cols:
                                    try:
                                        cim = PILImage.open(c)
                                        w2, _ = cim.size
                                        widths.append(w2)
                                        total_w += w2
                                    except Exception:
                                        widths.append(0)
                                ratios = []
                                ratios_percent = []
                                if total_w > 0:
                                    ratios = [round(w2/float(total_w), 3) for w2 in widths]
                                    ratios_percent = [int(round(r*100)) for r in ratios]
                                row = {
                                    'segment': os.path.basename(sp),
                                    'columns': [os.path.basename(c) for c in cols],
                                    'ratios': ratios,
                                    'ratios_percent': ratios_percent
                                }
                                layout_rows.append(row)
                                for c in cols:
                                    images_flat.append(c)
                                    copied.append(os.path.basename(c))
                        if images_flat:
                            section['images'] = images_flat
                        else:
                            section['images'] = segs
                        section['segments'] = [os.path.basename(s) for s in segs]
                        if layout_rows:
                            section['layout_rows'] = layout_rows
                section['pattern'] = identify_pattern(section)
                try:
                    from analyzer import identify_pattern_variant
                    section['pattern_variant'] = identify_pattern_variant(section)
                except Exception:
                    section['pattern_variant'] = ''
        except Exception:
            pass
    info_md = ''
    if os.path.isfile(DOC_INFO_PATH):
        try:
            with open(DOC_INFO_PATH, 'r', encoding='utf-8') as f:
                info_md = f.read()
        except Exception:
            info_md = ''
    # Añadir información adicional proveniente de archivos de texto/XML del ZIP
    if text_files or xml_files:
        extra_sections = []
        if text_files:
            extra_sections.append("## Contenido de texto detectado en el ZIP")
            for tf in text_files:
                try:
                    with open(tf, 'r', encoding='utf-8', errors='ignore') as rf:
                        snippet = rf.read(4000)
                    extra_sections.append(f"### {os.path.basename(tf)}\n\n{snippet}\n")
                except Exception:
                    continue
        if xml_files:
            extra_sections.append("## Archivos XML detectados en el ZIP")
            for xf in xml_files:
                base = os.path.basename(xf)
                extra_sections.append(f"- {base}")
        if extra_sections:
            info_md = (info_md or '') + "\n\n" + "\n".join(extra_sections)
    html_path = os.path.join(TEMP_OUT_DIR, 'index.html')
    css_path = os.path.join(TEMP_OUT_DIR, 'styles.css')
    title = plan['title']
    sections_html = []

    section_files = []
    chapter_keys = list(range(len(plan['sections'])))
    for idx, section in enumerate(plan['sections']):
        section_file = f"{section['slug']}.html"
        section_files.append(section_file)
        file_name = os.path.join(TEMP_OUT_DIR, section_file)
        html_file = open(file_name, 'w', encoding='utf-8')
        paragraph_texts = []
        for p in section['images']:
            t = ocr_texts.get(p, '')
            if t:
                paragraph_texts.append(t)
        paragraph = '\n\n'.join(paragraph_texts) if paragraph_texts else ''
        paragraph = paragraph.replace('\n\n', '<br/><br/>')
        prev_link = ''
        if idx > 0:
            prev_chapter_file = f"{plan['sections'][idx-1]['slug']}.html"
            prev_link = f'<p><a href="{prev_chapter_file}">Anterior</a></p>'
        next_link = ''
        if idx < len(plan['sections']) - 1:
            next_chapter_file = f"{plan['sections'][idx+1]['slug']}.html"
            next_link = f'<p><a href="{next_chapter_file}">Siguiente</a></p>'
        content = f"""
<html>
  <head>
    <link rel="stylesheet" href="styles.css">
  </head>
  <body>
    <div>
      <h1>{section['label']}</h1>
      <p>{paragraph}</p>
      {prev_link}
      {next_link}
    </div>
  </body>
</html>
"""
        html_file.write(content)
        html_file.close()
        imgs_html = ''.join([f'<img src="assets/{os.path.basename(p)}" alt="{section["name"]}">' for p in section['images']])
        sections_html.append(f'<section id="{section["slug"]}"><h2>{section["label"]}</h2><p><a href="{section_file}">Abrir sección</a></p>{imgs_html}</section>')
    html_content = f"""
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Sitio generado desde imágenes">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
  <title>{title}</title>
</head>
<body>
  <header class="site-header"><div class="container"><h1>{title}</h1></div></header>
  <main class="site-main"><div class="container">
    {''.join(sections_html)}
  </div></main>
  <footer class="site-footer"><div class="container">Generado con img2html</div></footer>
  <script type="application/json" id="img2html-plan">{plan}</script>
  <script type="application/json" id="img2html-info">{info_md}</script>
</body>
</html>
"""
    with open(html_path, 'w', encoding='utf-8') as hf:
        hf.write(html_content)
    css_content = """
:root { --bg: #0b0c0f; --fg: #ffffff; --muted: #a3a3a3; --primary: #4f46e5; }
* { box-sizing: border-box }
html, body { height: 100% }
body { margin: 0; background: var(--bg); color: var(--fg); font-family: 'Inter', system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif }
.container { width: min(1100px, 92%); margin: 0 auto; padding: 24px }
.site-header, .site-footer { background: #121318 }
h1 { font-size: 28px; margin: 0 }
h2 { font-size: 22px; margin: 24px 0 12px }
section { padding: 16px 0; border-top: 1px solid #1f2330 }
img { max-width: 100%; display: block; border-radius: 8px; margin: 8px 0 }
"""
    with open(css_path, 'w', encoding='utf-8') as cf:
        cf.write(css_content)
    wp_theme_dir = os.path.join(BASE_DIR, 'wp_theme')
    os.makedirs(wp_theme_dir, exist_ok=True)
    try:
        if google_api_key:
            os.environ['GOOGLE_API_KEY'] = google_api_key
            if save_env:
                _update_env_file(ENV_PATH, 'GOOGLE_API_KEY', google_api_key)
        if google_application_credentials:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_application_credentials
            if save_env:
                _update_env_file(ENV_PATH, 'GOOGLE_APPLICATION_CREDENTIALS', google_application_credentials)
        builder = ThemeBuilder(output_dir=wp_theme_dir, context=dna)
        builder.bootstrap()
        builder.run_prompt('01_theme_json_full.json')
        builder.run_prompt('52_template_parts_catalog.json')
        builder.run_prompt('51_templates_catalog.json')
        builder.run_prompt('53_patterns_catalog.json')
        
        # Obtener todos los datos del tema
        theme_name = request.form.get('theme_name', '').strip() or 'Img2HTML AI Theme'
        theme_slug = request.form.get('theme_slug', '').strip() or ''
        theme_description = request.form.get('theme_description', '').strip() or 'Tema de bloques generado y refinado con IA desde imágenes'
        theme_version = request.form.get('theme_version', '').strip() or '1.0.0'
        theme_author = request.form.get('theme_author', '').strip() or ''
        theme_uri = request.form.get('theme_uri', '').strip() or ''
        theme_textdomain = request.form.get('theme_textdomain', '').strip() or ''
        theme_tags = request.form.get('theme_tags', '').strip() or ''
        theme_license = request.form.get('theme_license', '').strip() or 'GPLv2 or later'
        css_framework = request.form.get('css_framework', 'tailwind')
        
        # Construcción mejorada del tema
        try:
            from theme_builder import build_complete_theme, generate_theme_screenshot
            from blocks_builder import setup_css_framework, create_custom_blocks
            build_complete_theme(
                wp_theme_dir,
                plan,
                dna,
                images,
                theme_name,
                theme_description,
                theme_slug,
                css_framework,
                theme_version=theme_version,
                theme_author=theme_author,
                theme_uri=theme_uri,
                theme_textdomain=theme_textdomain,
                theme_tags=theme_tags,
                theme_license=theme_license
            )
            # Configurar framework CSS
            setup_css_framework(wp_theme_dir, css_framework)
            try:
                from theme_builder import apply_typography_and_spacing, update_theme_json_colors
                apply_typography_and_spacing(wp_theme_dir, dna, plan)
                update_theme_json_colors(wp_theme_dir, dna)
            except Exception:
                pass
            # Crear bloques personalizados
            create_custom_blocks(wp_theme_dir, css_framework, plan, theme_slug)
            # Generar screenshot SVG
            generate_theme_screenshot(wp_theme_dir, plan, dna, theme_name, theme_description)
        except Exception as e:
            print(f"Error en construcción del tema: {e}")
            import traceback
            traceback.print_exc()
        
    result = refine_and_generate_wp(TEMP_OUT_DIR, info_md, plan, wp_theme_dir, images=images, dna=dna)
    used_ai = bool(result.get('used_ai')) if isinstance(result, dict) else False
    provider = (result.get('provider') if isinstance(result, dict) else '') or ''

    # SEO básico opcional
    if enable_seo:
        try:
            _enable_seo_meta(wp_theme_dir)
        except Exception:
            pass

        # Integrar fuentes personalizadas incluidas en el ZIP (si las hay)
        try:
            _integrate_fonts_into_theme(wp_theme_dir, fonts)
        except Exception:
            pass
    except Exception:
        used_ai = False
        provider = ''
    return render_template('done.html', output_dir='temp_out', theme_dir='wp_theme', used_ai=used_ai, saved_env=bool(save_env), provider=provider, ocr_provider=ocr_provider)

@app.route('/temp_out/<path:filename>')
def temp_out_files(filename):
    return send_from_directory(TEMP_OUT_DIR, filename)

@app.route('/wp_theme/<path:filename>')
def wp_theme_files(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'wp_theme'), filename)

@app.route('/download_theme', methods=['GET'])
def download_theme():
    theme_dir = os.path.join(BASE_DIR, 'wp_theme')
    zip_path = os.path.join(BASE_DIR, 'wp_theme.zip')
    import zipfile
    # Empaquetado limpio: sólo archivos necesarios para subir a wp-admin
    exclude_dirs = {
        'node_modules',
        '.git',
        '.github',
        '.vscode',
        'build',
        'dist',
        '.cache'
    }
    exclude_files = {
        'package.json',
        'package-lock.json',
        'yarn.lock',
        'pnpm-lock.yaml',
        'composer.json',
        'composer.lock',
        '.DS_Store'
    }
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(theme_dir):
            # Filtrar directorios de desarrollo
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for f in files:
                if f in exclude_files:
                    continue
                full = os.path.join(root, f)
                arc = os.path.relpath(full, theme_dir)
                zf.write(full, arc)
    return send_from_directory(BASE_DIR, 'wp_theme.zip', as_attachment=True)

@app.route('/download_static', methods=['GET'])
def download_static():
    out_dir = TEMP_OUT_DIR
    zip_path = os.path.join(BASE_DIR, 'static_site.zip')
    import zipfile
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(out_dir):
            for f in files:
                full = os.path.join(root, f)
                arc = os.path.relpath(full, out_dir)
                zf.write(full, arc)
    return send_from_directory(BASE_DIR, 'static_site.zip', as_attachment=True)

@app.route('/download_content', methods=['GET'])
def download_content():
    """
    Descarga el export WXR (contenido OCR/plan) generado en temp_out/content.xml
    para importarlo en WordPress (Herramientas > Importar > WordPress).
    """
    wxr_path = os.path.join(TEMP_OUT_DIR, 'content.xml')
    if not os.path.isfile(wxr_path):
        flash('No se encontró content.xml. Vuelve a generar el contenido.')
        return redirect(url_for('index'))
    return send_from_directory(TEMP_OUT_DIR, 'content.xml', as_attachment=True)

@app.route('/download_bundle', methods=['GET'])
def download_bundle():
    """
    Descarga un ZIP que contiene:
    - Carpeta 'html/' con todo el sitio estático generado
    - Carpeta 'theme/' con el tema WordPress listo para subir
    Esto permite ajustar primero el HTML y luego reutilizarlo para refinar el tema WP.
    """
    static_dir = TEMP_OUT_DIR
    theme_dir = os.path.join(BASE_DIR, 'wp_theme')
    bundle_name = 'img2html_bundle.zip'
    bundle_path = os.path.join(BASE_DIR, bundle_name)
    import zipfile

    exclude_dirs = {
        'node_modules',
        '.git',
        '.github',
        '.vscode',
        'build',
        'dist',
        '.cache'
    }
    exclude_files = {
        'package.json',
        'package-lock.json',
        'yarn.lock',
        'pnpm-lock.yaml',
        'composer.json',
        'composer.lock',
        '.DS_Store'
    }

    with zipfile.ZipFile(bundle_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Incluir HTML estático bajo html/
        if os.path.isdir(static_dir):
            for root, _, files in os.walk(static_dir):
                for f in files:
                    full = os.path.join(root, f)
                    rel = os.path.relpath(full, static_dir)
                    arc = os.path.join('html', rel)
                    zf.write(full, arc)

        # Incluir tema WordPress bajo theme/
        if os.path.isdir(theme_dir):
            for root, dirs, files in os.walk(theme_dir):
                # Filtrar directorios de desarrollo
                dirs[:] = [d for d in dirs if d not in exclude_dirs]
                for f in files:
                    if f in exclude_files:
                        continue
                    full = os.path.join(root, f)
                    rel = os.path.relpath(full, theme_dir)
                    arc = os.path.join('theme', rel)
                    zf.write(full, arc)

    return send_from_directory(BASE_DIR, bundle_name, as_attachment=True)

@app.route('/refine_theme_from_html', methods=['POST'])
def refine_theme_from_html():
    """
    Segunda fase opcional:
    - El usuario sube un ZIP con HTML/CSS ajustado (por ejemplo, el contenido de la carpeta html/ del bundle).
    - La app reemplaza el contenido de temp_out con ese HTML.
    - Se vuelve a generar/refinar el tema de WordPress usando ese HTML como fuente principal.
    """
    file = request.files.get('html_zip')
    if not file or file.filename == '':
        flash('Adjunta un archivo ZIP válido con el HTML refinado')
        return redirect(url_for('index'))

    import zipfile
    import shutil

    # Preparar carpeta temporal para extraer el ZIP
    batch_id = str(uuid.uuid4())
    html_batch_dir = os.path.join(UPLOAD_DIR, f'html_refined_{batch_id}')
    os.makedirs(html_batch_dir, exist_ok=True)
    zip_path = os.path.join(html_batch_dir, secure_filename(file.filename))
    file.save(zip_path)

    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(html_batch_dir)
    except Exception:
        flash('No se pudo descomprimir el ZIP de HTML/Tema refinado')
        return redirect(url_for('index'))

    # Soportar dos casos:
    # 1) ZIP con carpeta html/ y theme/ (bundle generado por la app)
    # 2) ZIP con un sitio estático "plano" que contenga index.html en cualquier carpeta
    html_root_candidate = os.path.join(html_batch_dir, 'html')
    theme_root_candidate = os.path.join(html_batch_dir, 'theme')

    new_temp_dir = None
    theme_source_dir = None

    # Preferir estructura html/ + theme/ si existe
    if os.path.isdir(html_root_candidate) and os.path.isfile(os.path.join(html_root_candidate, 'index.html')):
        new_temp_dir = html_root_candidate
        if os.path.isdir(theme_root_candidate):
            theme_source_dir = theme_root_candidate
    else:
        # Buscar index.html en cualquier parte del ZIP
        for root, _, files in os.walk(html_batch_dir):
            if 'index.html' in files:
                new_temp_dir = root
                break

    if not new_temp_dir:
        flash('El ZIP debe contener un index.html (sitio estático refinado)')
        return redirect(url_for('index'))

    # Sustituir el contenido de TEMP_OUT por el HTML refinado
    try:
        if os.path.isdir(TEMP_OUT_DIR):
            shutil.rmtree(TEMP_OUT_DIR)
        shutil.copytree(new_temp_dir, TEMP_OUT_DIR)
    except Exception:
        flash('No se pudo actualizar el HTML base con el contenido refinado')
        return redirect(url_for('index'))

    # Si el ZIP incluye una carpeta theme/, usarla como base del tema antes de refinar
    wp_theme_dir = os.path.join(BASE_DIR, 'wp_theme')
    try:
        if theme_source_dir and os.path.isdir(theme_source_dir):
            if os.path.isdir(wp_theme_dir):
                shutil.rmtree(wp_theme_dir)
            shutil.copytree(theme_source_dir, wp_theme_dir)
        else:
            os.makedirs(wp_theme_dir, exist_ok=True)
    except Exception:
        flash('No se pudo preparar la carpeta del tema a partir del ZIP proporcionado')
        return redirect(url_for('index'))

    # Construir un plan mínimo para que el refinador pueda trabajar
    minimal_plan = {
        "title": "Sitio refinado",
        "sections": [
            {
                "name": "refined",
                "label": "Refinado",
                "slug": "refinado",
                "images": []
            }
        ],
        "count": 1
    }

    # Volver a generar / refinar el tema a partir del nuevo HTML
    result = refine_and_generate_wp(
        TEMP_OUT_DIR,
        info_md='',
        plan=minimal_plan,
        theme_dir=wp_theme_dir,
        images=None,
        dna=None
    )
    used_ai = bool(result.get('used_ai')) if isinstance(result, dict) else False
    provider = (result.get('provider') if isinstance(result, dict) else '') or ''

    # Mostrar de nuevo la pantalla de resultado
    PROGRESS.setdefault(batch_id, {})
    PROGRESS[batch_id]['used_ai'] = used_ai
    PROGRESS[batch_id]['provider'] = provider
    PROGRESS[batch_id]['ocr_provider'] = ''
    PROGRESS[batch_id]['saved_env'] = False
    PROGRESS[batch_id]['ready'] = True

    return render_template(
        'done.html',
        output_dir='temp_out',
        theme_dir='wp_theme',
        used_ai=used_ai,
        saved_env=False,
        provider=provider,
        ocr_provider=''
    )

@app.route('/install_theme', methods=['POST'])
def install_theme():
    """Instala el tema generado en WordPress."""
    try:
        from theme_builder import install_theme_to_wordpress
        wordpress_dir = request.form.get('wordpress_dir', '')
        theme_slug = request.form.get('theme_slug', '')
        
        if not wordpress_dir:
            # Intentar detectar automáticamente
            possible_paths = [
                os.path.join(BASE_DIR, 'wordpress'),
                os.path.join(BASE_DIR, '..', 'wordpress'),
                os.path.join(os.path.dirname(BASE_DIR), 'wordpress'),
            ]
            for path in possible_paths:
                if os.path.isdir(path) and os.path.isdir(os.path.join(path, 'wp-content')):
                    wordpress_dir = path
                    break
        
        if not wordpress_dir or not os.path.isdir(wordpress_dir):
            flash('No se encontró la instalación de WordPress. Especifica la ruta manualmente.')
            return redirect(url_for('index'))
        
        theme_dir = os.path.join(BASE_DIR, 'wp_theme')
        success = install_theme_to_wordpress(theme_dir, wordpress_dir, theme_slug)
        
        if success:
            flash('Tema instalado exitosamente en WordPress')
        else:
            flash('Error al instalar el tema')
        
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error: {str(e)}')
        return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8001))
    app.run(host='0.0.0.0', port=port, debug=True)
def _update_env_file(path, key, value):
    try:
        if not value:
            return False
        lines = []
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
        found = False
        new_lines = []
        for ln in lines:
            if ln.strip().startswith(f"{key}="):
                new_lines.append(f"{key}={value}")
                found = True
            else:
                new_lines.append(ln)
        if not found:
            new_lines.append(f"{key}={value}")
        with open(path, 'w', encoding='utf-8') as f:
            f.write("\n".join(new_lines))
        return True
    except Exception:
        return False
def _is_valid_service_account_json(obj):
    try:
        if not isinstance(obj, dict):
            return False
        t = obj.get('type')
        pid = obj.get('project_id')
        pkid = obj.get('private_key_id')
        pk = obj.get('private_key')
        email = obj.get('client_email')
        return t == 'service_account' and bool(pid and pkid and pk and email)
    except Exception:
        return False

def _export_wxr(temp_out_dir: str, plan: Dict, ocr_texts: Dict):
    """
    Genera un archivo WXR (XML de exportación WP) básico con el contenido
    detectado (títulos por sección y texto OCR de las imágenes).
    """
    try:
        import datetime
        now = datetime.datetime.utcnow().isoformat() + "Z"
        items = []
        for idx, sec in enumerate(plan.get('sections', [])):
            title = sec.get('label') or sec.get('name') or f'Sección {idx+1}'
            slug = sec.get('slug') or f'section-{idx+1}'
            paragraphs = []
            for img in sec.get('images', []):
                txt = ocr_texts.get(img, '')
                if txt:
                    paragraphs.append(txt)
            content = '<br/><br/>'.join(paragraphs) if paragraphs else ''
            item = f"""
  <item>
    <title><![CDATA[{title}]]></title>
    <link>https://example.com/{slug}</link>
    <pubDate>{now}</pubDate>
    <dc:creator><![CDATA[img2html]]></dc:creator>
    <guid isPermaLink="false">img2html-{slug}</guid>
    <description></description>
    <content:encoded><![CDATA[{content}]]></content:encoded>
    <excerpt:encoded><![CDATA[]]></excerpt:encoded>
    <wp:post_name>{slug}</wp:post_name>
    <wp:post_type>page</wp:post_type>
    <wp:status>publish</wp:status>
  </item>"""
            items.append(item)

        wxr = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0"
    xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
    xmlns:content="http://purl.org/rss/1.0/modules/content/"
    xmlns:wfw="http://wellformedweb.org/CommentAPI/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:wp="http://wordpress.org/export/1.2/">
<channel>
  <title>Img2HTML Export</title>
  <link>https://example.com</link>
  <description>Contenido generado desde imágenes</description>
  <pubDate>{now}</pubDate>
  <wp:wxr_version>1.2</wp:wxr_version>
  {''.join(items)}
</channel>
</rss>"""
        with open(os.path.join(temp_out_dir, 'content.xml'), 'w', encoding='utf-8') as f:
            f.write(wxr)
    except Exception:
        pass

def _integrate_fonts_into_theme(theme_dir: str, font_paths):
    """
    Copia fuentes personalizadas al tema y las registra en theme.json
    usando la API de fuentes de theme.json (fontFamilies + fontFace).
    """
    try:
        if not font_paths:
            return
        theme_json_path = os.path.join(theme_dir, 'theme.json')
        if not os.path.isfile(theme_json_path):
            return

        import json as _json
        import shutil as _shutil

        with open(theme_json_path, 'r', encoding='utf-8') as f:
            data = _json.load(f)

        settings = data.setdefault('settings', {})
        typo = settings.setdefault('typography', {})
        families = typo.setdefault('fontFamilies', [])

        fonts_dir = os.path.join(theme_dir, 'assets', 'fonts')
        os.makedirs(fonts_dir, exist_ok=True)

        for src in font_paths:
            if not os.path.isfile(src):
                continue
            base = os.path.basename(src)
            name_root, _ext = os.path.splitext(base)
            if not name_root:
                continue
            slug = _sanitize_slug(name_root)

            # Evitar duplicar familias por slug
            if any(fam.get('slug') == slug for fam in families):
                # Asegurar que el archivo exista en assets/fonts
                dest_full_existing = os.path.join(fonts_dir, base)
                if not os.path.isfile(dest_full_existing):
                    _shutil.copy2(src, dest_full_existing)
                continue

            dest_full = os.path.join(fonts_dir, base)
            if not os.path.isfile(dest_full):
                _shutil.copy2(src, dest_full)

            dest_rel = f"assets/fonts/{base}"
            family_name = name_root.replace('-', ' ').replace('_', ' ').title()

            families.append({
                "fontFamily": f"\"{family_name}\", system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", sans-serif",
                "name": family_name,
                "slug": slug,
                "fontFace": [
                    {
                        "fontFamily": family_name,
                        "fontStyle": "normal",
                        "fontWeight": "400",
                        "src": [f"file:./{dest_rel}"]
                    }
                ]
            })

        with open(theme_json_path, 'w', encoding='utf-8') as f:
            _json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        # No romper el flujo si algo falla con las fuentes
        pass

def _enable_seo_meta(theme_dir: str):
    """
    Crea un archivo PHP que inyecta meta title/description básicos,
    Open Graph y asegura alt en imágenes si falta atributo.
    """
    try:
        php_dir = os.path.join(theme_dir, 'php')
        os.makedirs(php_dir, exist_ok=True)
        seo_php = os.path.join(php_dir, 'seo-meta.php')
        content = """<?php
/**
 * SEO básico para el tema generado.
 * Inyecta meta description y Open Graph, y asegura alt en imágenes.
 */
if (!function_exists('img2html_seo_meta_tags')) {
    function img2html_seo_meta_tags() {
        if (is_admin()) return;
        $title = wp_get_document_title();
        $desc  = get_bloginfo('description');
        $url   = home_url(add_query_arg(array(),$GLOBALS['wp']->request));
        $img   = get_theme_file_uri('screenshot.png');
        if (!$img) {
            $img = get_theme_file_uri('screenshot.jpg');
        }
        if (!$img) {
            $img = get_theme_file_uri('screenshot.webp');
        }
        echo '<meta name=\"description\" content=\"' . esc_attr($desc) . '\" />' . \"\\n\";
        echo '<meta property=\"og:title\" content=\"' . esc_attr($title) . '\" />' . \"\\n\";
        echo '<meta property=\"og:description\" content=\"' . esc_attr($desc) . '\" />' . \"\\n\";
        echo '<meta property=\"og:url\" content=\"' . esc_url($url) . '\" />' . \"\\n\";
        if ($img) {
            echo '<meta property=\"og:image\" content=\"' . esc_url($img) . '\" />' . \"\\n\";
        }
        echo '<meta name=\"twitter:card\" content=\"summary_large_image\" />' . \"\\n\";
    }
    add_action('wp_head', 'img2html_seo_meta_tags', 5);
}

// Filtro para asegurar alt en imágenes cuando falte (fallback con el título del post o del sitio)
if (!function_exists('img2html_filter_image_alt')) {
    function img2html_filter_image_alt($attr, $attachment = null) {
        if (empty($attr['alt'])) {
            if ($attachment) {
                $alt = trim(strip_tags(get_post_field('post_title', $attachment->ID)));
            }
            if (empty($alt)) {
                $alt = get_bloginfo('name');
            }
            $attr['alt'] = $alt;
        }
        return $attr;
    }
    add_filter('wp_get_attachment_image_attributes', 'img2html_filter_image_alt', 10, 2);
}
"""
        with open(seo_php, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception:
        pass
