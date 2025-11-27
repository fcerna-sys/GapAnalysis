from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import os
import zipfile
import uuid
from analyzer import analyze_images
from ocr import extract_texts
from ai_refine import refine_and_generate_wp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
TEMP_OUT_DIR = os.path.join(BASE_DIR, 'temp_out')
DOC_INFO_PATH = os.path.join(BASE_DIR, 'docs', 'info.md')

app = Flask(__name__)
app.secret_key = 'img2html-secret'

ALLOWED_EXTENSIONS = {'.zip'}

def allowed_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS

@app.template_filter('basename')
def basename_filter(p):
    return os.path.basename(p)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('zipfile')
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
    request.environ['img2html_batch_dir'] = batch_dir
    request.environ['img2html_plan'] = plan
    return render_template('plan.html', plan=plan, batch_id=batch_id)

@app.route('/convert', methods=['POST'])
def convert():
    batch_id = request.form.get('batch_id')
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
    try:
        ocr_texts = extract_texts(images)
    except Exception:
        ocr_texts = {}
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
        refine_and_generate_wp(TEMP_OUT_DIR, info_md, plan, wp_theme_dir)
    except Exception:
        pass
    return render_template('done.html', output_dir='temp_out', theme_dir='wp_theme')

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)