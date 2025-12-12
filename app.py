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
load_dotenv()
try:
    if not os.path.isfile(os.path.join(BASE_DIR, '.env')):
        with open(os.path.join(BASE_DIR, '.env'), 'w', encoding='utf-8') as f:
            f.write('')
except Exception:
    pass

ALLOWED_EXTENSIONS = {'.zip'}
PROGRESS = {}

def allowed_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS

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
    theme_slug = request.form.get('theme_slug', '').strip() or ''
    theme_description = request.form.get('theme_description', '').strip() or 'Tema de bloques generado y refinado con IA desde imágenes'
    css_framework = request.form.get('css_framework', 'tailwind')  # tailwind, bootstrap, none
    google_api_key = request.form.get('google_api_key') or ''
    enable_slicing = request.form.get('enable_slicing') or ''
    precise_slicing = request.form.get('precise_slicing') or ''
    save_env = request.form.get('save_env') or ''
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
        zf.extractall(batch_dir)
    images = []
    for root, _, files in os.walk(batch_dir):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in {'.png', '.jpg', '.jpeg', '.webp', '.gif'}:
                images.append(os.path.join(root, f))
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
    request.environ['img2html_batch_dir'] = batch_dir
    request.environ['img2html_plan'] = plan
    request.environ['img2html_theme_name'] = theme_name
    request.environ['img2html_theme_slug'] = theme_slug
    request.environ['img2html_theme_description'] = theme_description
    request.environ['img2html_css_framework'] = css_framework
    request.environ['img2html_css_framework'] = css_framework
    return render_template('plan.html', plan=plan, batch_id=batch_id, theme_name=theme_name, theme_slug=theme_slug, theme_description=theme_description, css_framework=css_framework, google_api_key=google_api_key, enable_slicing=enable_slicing, precise_slicing=precise_slicing, save_env=save_env, google_application_credentials=google_application_credentials)

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
    css_framework = ctx.get('css_framework', 'tailwind')
    google_api_key = ctx.get('google_api_key') or ''
    enable_slicing = ctx.get('enable_slicing') or ''
    precise_slicing = ctx.get('precise_slicing') or ''
    save_env = ctx.get('save_env') or ''
    google_application_credentials = ctx.get('google_application_credentials') or ''
    _set_progress(batch_id, 5, 'Inicializando conversión')
    try:
        batch_dir = os.path.join(UPLOAD_DIR, batch_id)
        images = []
        for root, _, files in os.walk(batch_dir):
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in {'.png', '.jpg', '.jpeg', '.webp', '.gif'}:
                    images.append(os.path.join(root, f))
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
                build_complete_theme(wp_theme_dir, plan, dna, images, theme_name, theme_description, theme_slug, css_framework)
                # Configurar framework CSS
                setup_css_framework(wp_theme_dir, css_framework)
                # Crear bloques personalizados (con prefijo BEM desde theme_slug)
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
        'css_framework': request.form.get('css_framework', 'tailwind'),
        'google_api_key': request.form.get('google_api_key') or '',
        'enable_slicing': request.form.get('enable_slicing') or '',
        'precise_slicing': request.form.get('precise_slicing') or '',
        'save_env': request.form.get('save_env') or '',
        'google_application_credentials': request.form.get('google_application_credentials') or ''
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
    google_application_credentials = request.form.get('google_application_credentials') or ''
    if not batch_id:
        flash('Falta el identificador del lote')
        return redirect(url_for('index'))
    batch_dir = os.path.join(UPLOAD_DIR, batch_id)
    if not os.path.isdir(batch_dir):
        flash('El lote indicado no existe')
        return redirect(url_for('index'))
    images = []
    for root, _, files in os.walk(batch_dir):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in {'.png', '.jpg', '.jpeg', '.webp', '.gif'}:
                images.append(os.path.join(root, f))
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
        
        # Obtener nombre y descripción del tema
        theme_name = request.form.get('theme_name', '').strip() or 'Img2HTML AI Theme'
        theme_slug = request.form.get('theme_slug', '').strip() or ''
        theme_description = request.form.get('theme_description', '').strip() or 'Tema de bloques generado y refinado con IA desde imágenes'
        css_framework = request.form.get('css_framework', 'tailwind')
        
        # Construcción mejorada del tema
        try:
            from theme_builder import build_complete_theme, generate_theme_screenshot
            from blocks_builder import setup_css_framework, create_custom_blocks
            build_complete_theme(wp_theme_dir, plan, dna, images, theme_name, theme_description, theme_slug, css_framework)
            # Configurar framework CSS
            setup_css_framework(wp_theme_dir, css_framework)
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
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(theme_dir):
            for f in files:
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