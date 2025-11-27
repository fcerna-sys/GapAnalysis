import os
import json
from typing import Dict
import base64
import urllib.request
import urllib.error
import ssl

def _read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return ''

def _write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def _read_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

def _write_json(path, obj):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
def _hex_to_rgb(hex_str):
    try:
        s = hex_str.strip().lstrip('#')
        if len(s) == 6:
            r = int(s[0:2], 16); g = int(s[2:4], 16); b = int(s[4:6], 16)
            return (r, g, b)
    except Exception:
        pass
    return (59,130,246)
def _lum(rgb):
    try:
        r, g, b = rgb
        return 0.2126*(r/255.0) + 0.7152*(g/255.0) + 0.0722*(b/255.0)
    except Exception:
        return 0.5
def _strip_fences(text):
    t = text.strip()
    if t.startswith('```'):
        idx = t.find('\n')
        if idx != -1:
            t = t[idx+1:]
    if t.endswith('```'):
        t = t[:-3]
    return t.strip()
def _extract_json(text):
    t = _strip_fences(text)
    try:
        return json.loads(t)
    except Exception:
        pass
    start_obj = t.find('{'); end_obj = t.rfind('}')
    start_arr = t.find('['); end_arr = t.rfind(']')
    cands = []
    if start_obj != -1 and end_obj != -1 and end_obj > start_obj:
        cands.append(t[start_obj:end_obj+1])
    if start_arr != -1 and end_arr != -1 and end_arr > start_arr:
        cands.append(t[start_arr:end_arr+1])
    for c in cands:
        try:
            return json.loads(c)
        except Exception:
            continue
    return None

def _fallback_wp(theme_dir, refined_html, css, plan):
    os.makedirs(theme_dir, exist_ok=True)
    os.makedirs(os.path.join(theme_dir, 'parts'), exist_ok=True)
    os.makedirs(os.path.join(theme_dir, 'templates'), exist_ok=True)
    style_css = """
/*
Theme Name: Img2HTML AI Theme
Version: 0.1.0
Author: img2html
Description: Tema de bloques generado y refinado con IA
Requires at least: 6.7
*/
"""
    _write_file(os.path.join(theme_dir, 'style.css'), style_css)
    parts_header = """
<!-- wp:group {"tagName":"header","className":"site-header"} -->
<header class="site-header">
  <!-- wp:columns {"verticalAlignment":"center"} -->
  <div class="wp-block-columns are-vertically-aligned-center">
    <!-- wp:column {"verticalAlignment":"center","width":"33.33%"} -->
    <div class="wp-block-column is-vertically-aligned-center">
      <!-- wp:site-logo {"width":48} /-->
    </div>
    <!-- /wp:column -->
    <!-- wp:column {"verticalAlignment":"center","width":"33.33%"} -->
    <div class="wp-block-column is-vertically-aligned-center">
      <!-- wp:site-title /-->
      <!-- wp:site-tagline /-->
    </div>
    <!-- /wp:column -->
    <!-- wp:column {"verticalAlignment":"center","width":"33.33%"} -->
    <div class="wp-block-column is-vertically-aligned-center">
      <!-- wp:navigation {"layout":{"type":"flex","justifyContent":"right"}} /-->
    </div>
    <!-- /wp:column -->
  </div>
  <!-- /wp:columns -->
</header>
<!-- /wp:group -->
"""
    _write_file(os.path.join(theme_dir, 'parts', 'header.html'), parts_header)
    parts_footer = """
<!-- wp:group {"tagName":"footer","className":"site-footer"} -->
<footer class="site-footer">
  <!-- wp:paragraph -->
  <p>© <span class="wp-block-site-title"></span></p>
  <!-- /wp:paragraph -->
  <!-- wp:social-links {"layout":{"type":"flex"}} /-->
</footer>
<!-- /wp:group -->
"""
    _write_file(os.path.join(theme_dir, 'parts', 'footer.html'), parts_footer)
    templates_index = """
<!-- wp:template-part {"slug":"header"} /-->
<!-- wp:group {"tagName":"main"} -->
<main>
  <!-- wp:query {"queryId":1,"query":{"perPage":10,"pages":0,"offset":0,"postType":"post","order":"desc","orderby":"date"}} -->
  <div class="wp-block-query">
    <!-- wp:post-template -->
    <!-- wp:post-title {"isLink":true} /-->
    <!-- wp:post-featured-image {"isLink":true} /-->
    <!-- wp:post-excerpt /-->
    <!-- /wp:post-template -->
    <!-- wp:query-pagination {"paginationArrow":"chevron","layout":{"type":"flex","justifyContent":"space-between"}} /-->
  </div>
  <!-- /wp:query -->
</main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer"} /-->
"""
    _write_file(os.path.join(theme_dir, 'templates', 'index.html'), templates_index)
    # front-page template
    site_title = plan.get('title', 'Inicio')
    first_label = plan['sections'][0]['label'] if plan.get('sections') else 'Hero'
    templates_front = f"""
<!-- wp:template-part {"slug":"header"} /-->
<!-- wp:group {"tagName":"main"} -->
<main>
  <!-- wp:cover {"dimRatio":30,"overlayColor":"primary","minHeight":480,"isDark":false} -->
  <div class="wp-block-cover" style="min-height:480px">
    <span aria-hidden="true" class="wp-block-cover__background has-primary-background-color has-background-dim"></span>
    <div class="wp-block-cover__inner-container">
      <!-- wp:heading {"textAlign":"center","level":1} -->
      <h1 class="has-text-align-center">{first_label}</h1>
      <!-- /wp:heading -->
      <!-- wp:buttons {"layout":{"type":"flex","justifyContent":"center"}} -->
      <div class="wp-block-buttons">
        <!-- wp:button {"className":"is-style-fill"} -->
        <div class="wp-block-button is-style-fill"><a class="wp-block-button__link">Comenzar</a></div>
        <!-- /wp:button -->
      </div>
      <!-- /wp:buttons -->
    </div>
  </div>
  <!-- /wp:cover -->
  <!-- wp:query {"queryId":2,"query":{"perPage":6,"pages":0,"offset":0,"postType":"post","order":"desc","orderby":"date"}} -->
  <div class="wp-block-query">
    <!-- wp:heading {"level":2} -->
    <h2>Últimas entradas</h2>
    <!-- /wp:heading -->
    <!-- wp:post-template -->
    <!-- wp:group {"layout":{"type":"constrained"}} -->
    <div class="wp-block-group">
      <!-- wp:post-title {"isLink":true} /-->
      <!-- wp:post-excerpt /-->
    </div>
    <!-- /wp:group -->
    <!-- /wp:post-template -->
    <!-- wp:query-pagination {"paginationArrow":"chevron","layout":{"type":"flex","justifyContent":"space-between"}} /-->
  </div>
  <!-- /wp:query -->
</main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer"} /-->
"""
    _write_file(os.path.join(theme_dir, 'templates', 'front-page.html'), templates_front)
    # archive template
    templates_archive = """
<!-- wp:template-part {"slug":"header"} /-->
<!-- wp:group {"tagName":"main"} -->
<main>
  <!-- wp:heading {"level":1} -->
  <h1>Archivo</h1>
  <!-- /wp:heading -->
  <!-- wp:query {"queryId":3} -->
  <div class="wp-block-query">
    <!-- wp:post-template -->
    <!-- wp:post-title {"isLink":true} /-->
    <!-- wp:post-excerpt /-->
    <!-- /wp:post-template -->
    <!-- wp:query-pagination {"paginationArrow":"chevron","layout":{"type":"flex","justifyContent":"space-between"}} /-->
  </div>
  <!-- /wp:query -->
</main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer"} /-->
"""
    _write_file(os.path.join(theme_dir, 'templates', 'archive.html'), templates_archive)
    templates_single = """
<!-- wp:template-part {"slug":"header"} /-->
<!-- wp:group {"tagName":"main"} -->
<main>
  <!-- wp:post-title /-->
  <!-- wp:post-featured-image /-->
  <!-- wp:post-date /-->
  <!-- wp:post-author /-->
  <!-- wp:post-content /-->
  <!-- wp:post-navigation /-->
</main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer"} /-->
"""
    _write_file(os.path.join(theme_dir, 'templates', 'single.html'), templates_single)
    templates_page = """
<!-- wp:template-part {"slug":"header"} /-->
<!-- wp:group {"tagName":"main"} -->
<main>
  <!-- wp:post-title /-->
  <!-- wp:post-content /-->
</main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer"} /-->
"""
    _write_file(os.path.join(theme_dir, 'templates', 'page.html'), templates_page)
    templates_404 = """
<!-- wp:template-part {"slug":"header"} /-->
<!-- wp:group {"tagName":"main"} -->
<main>
  <!-- wp:heading {"level":1} -->
  <h1>Página no encontrada</h1>
  <!-- /wp:heading -->
  <!-- wp:paragraph -->
  <p>Lo sentimos, no encontramos lo que buscas.</p>
  <!-- /wp:paragraph -->
  <!-- wp:search {"showLabel":false,"placeholder":"Buscar..."} /-->
</main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer"} /-->
"""
    _write_file(os.path.join(theme_dir, 'templates', '404.html'), templates_404)
    blocks_css = """
input[type=text],input[type=email],input[type=url],input[type=password],textarea,select{background:var(--wp--preset--color--surface);color:var(--wp--preset--color--text);border:1px solid var(--wp--preset--color--primary);border-radius:8px;padding:10px 12px;width:100%}
button,input[type=submit]{background:var(--wp--preset--color--primary);color:var(--wp--preset--color--text);border:none;border-radius:8px;padding:10px 14px}
button:hover,input[type=submit]:hover{filter:brightness(1.1)}
.wp-block-gallery .blocks-gallery-item img{border-radius:8px}
.wp-block-comments{background:var(--wp--preset--color--surface);padding:16px;border-radius:12px}
"""
    _write_file(os.path.join(theme_dir, 'blocks.css'), blocks_css)
    functions_php = """
<?php
add_theme_support('title-tag');
add_theme_support('post-thumbnails');
function img2html_assets(){
  wp_enqueue_style('img2html-blocks', get_theme_file_uri('blocks.css'), [], null);
}
add_action('wp_enqueue_scripts','img2html_assets');
function img2html_register_patterns(){
  register_block_pattern_category('img2html', ['label'=>'Img2HTML']);
  register_block_pattern('img2html/hero',[
    'title'=>'Hero',
    'description'=>'Sección Hero con cover',
    'content'=>file_get_contents(get_theme_file_path('patterns/hero.html'))
  ]);
  register_block_pattern('img2html/form',[
    'title'=>'Formulario',
    'description'=>'Formulario de contacto',
    'content'=>file_get_contents(get_theme_file_path('patterns/form.html'))
  ]);
  register_block_pattern('img2html/gallery',[
    'title'=>'Galería',
    'description'=>'Galería de imágenes',
    'content'=>file_get_contents(get_theme_file_path('patterns/gallery.html'))
  ]);
  register_block_pattern('img2html/comments',[
    'title'=>'Comentarios',
    'description'=>'Sección de comentarios',
    'content'=>file_get_contents(get_theme_file_path('patterns/comments.html'))
  ]);
  $dir = get_theme_file_path('patterns');
  if (is_dir($dir)){
    foreach (glob($dir . DIRECTORY_SEPARATOR . 'auto_*.html') as $file){
      $base = basename($file, '.html');
      register_block_pattern('img2html/' . $base,[
        'title'=>$base,
        'description'=>'Patrón generado automáticamente',
        'content'=>file_get_contents($file)
      ]);
    }
  }
}
add_action('init','img2html_register_patterns');
?>
"""
    _write_file(os.path.join(theme_dir, 'functions.php'), functions_php)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    base_theme = _read_json(os.path.join(base_dir, 'theme.json'))
    if base_theme is None:
        base_theme = {
            "version": 3,
            "settings": {
                "layout": {"contentSize": "800px", "wideSize": "1200px"},
                "color": {"palette": [
                    {"name":"Text","slug":"text","color":"#1e293b"},
                    {"name":"Background","slug":"background","color":"#ffffff"},
                    {"name":"Primary","slug":"primary","color":"#3b82f6"},
                    {"name":"Secondary","slug":"secondary","color":"#64748b"},
                    {"name":"Surface","slug":"surface","color":"#f1f5f9"},
                    {"name":"Accent","slug":"accent","color":"#ef4444"}
                ]},
                "typography": {"fluid": True, "fontFamilies": [
                    {"fontFamily":"Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif","slug":"inter","name":"Inter"}
                ]}
            }
        }
    _write_json(os.path.join(theme_dir, 'theme.json'), base_theme)
    styles_dir = os.path.join(theme_dir, 'styles')
    os.makedirs(styles_dir, exist_ok=True)
    light = {
        "title": "Light",
        "styles": {
            "color": {"background": "var(--wp--preset--color--background)", "text": "var(--wp--preset--color--text)"}
        }
    }
    dark = {
        "title": "Dark",
        "styles": {
            "color": {"background": "#0b0c0f", "text": "#ffffff"},
            "elements": {"link": {"color": {"text": "#a3a3a3"}}}
        }
    }
    high_contrast = {
        "title": "High Contrast",
        "styles": {
            "color": {"background": "#000000", "text": "#ffffff"},
            "elements": {"button": {"color": {"background": "#ffff00", "text": "#000000"}}}
        }
    }
    _write_json(os.path.join(styles_dir, 'light.json'), light)
    _write_json(os.path.join(styles_dir, 'dark.json'), dark)
    _write_json(os.path.join(styles_dir, 'high-contrast.json'), high_contrast)
    os.makedirs(os.path.join(theme_dir, 'patterns'), exist_ok=True)
    pattern_form = """
<!-- wp:group -->
<div class="wp-block-group">
  <!-- wp:heading {"level":2} -->
  <h2>Contáctanos</h2>
  <!-- /wp:heading -->
  <!-- wp:html -->
  <form>
    <p><input type="text" placeholder="Nombre" /></p>
    <p><input type="email" placeholder="Email" /></p>
    <p><textarea rows="5" placeholder="Mensaje"></textarea></p>
    <p><input type="submit" value="Enviar" /></p>
  </form>
  <!-- /wp:html -->
</div>
<!-- /wp:group -->
"""
    _write_file(os.path.join(theme_dir, 'patterns', 'form.html'), pattern_form)
    hero_title = first_label
    pattern_hero = f"""
<!-- wp:cover {"dimRatio":20,"overlayColor":"primary","isDark":false} -->
<div class="wp-block-cover">
  <span aria-hidden="true" class="wp-block-cover__background has-primary-background-color has-background-dim"></span>
  <div class="wp-block-cover__inner-container">
    <!-- wp:heading {"textAlign":"center","level":1} -->
    <h1 class="has-text-align-center">{hero_title}</h1>
    <!-- /wp:heading -->
    <!-- wp:paragraph {"align":"center"} -->
    <p class="has-text-align-center">Construido con Img2HTML + IA</p>
    <!-- /wp:paragraph -->
    <!-- wp:buttons {"layout":{"type":"flex","justifyContent":"center"}} -->
    <div class="wp-block-buttons">
      <!-- wp:button {"className":"is-style-fill"} -->
      <div class="wp-block-button is-style-fill"><a class="wp-block-button__link">Explorar</a></div>
      <!-- /wp:button -->
    </div>
    <!-- /wp:buttons -->
  </div>
</div>
<!-- /wp:cover -->
"""
    _write_file(os.path.join(theme_dir, 'patterns', 'hero.html'), pattern_hero)
    pattern_gallery = """
<!-- wp:gallery {"columns":3} -->
<figure class="wp-block-gallery columns-3 is-cropped"></figure>
<!-- /wp:gallery -->
"""
    _write_file(os.path.join(theme_dir, 'patterns', 'gallery.html'), pattern_gallery)
    pattern_comments = """
<!-- wp:comments -->
<div class="wp-block-comments">
  <!-- wp:comments-title /-->
  <!-- wp:comment-template -->
  <!-- wp:columns -->
  <div class="wp-block-columns">
    <!-- wp:column {"width":"40px"} -->
    <div class="wp-block-column" style="flex-basis:40px">
      <!-- wp:avatar {"size":40} /-->
    </div>
    <!-- /wp:column -->
    <!-- wp:column -->
    <div class="wp-block-column">
      <!-- wp:comment-author-name /-->
      <!-- wp:comment-date /-->
      <!-- wp:comment-content /-->
      <!-- wp:comment-reply-link /-->
    </div>
    <!-- /wp:column -->
  </div>
  <!-- /wp:columns -->
  <!-- /wp:comment-template -->
  <!-- wp:comments-pagination /-->
  <!-- wp:post-comments-form /-->
</div>
<!-- /wp:comments -->
"""
    _write_file(os.path.join(theme_dir, 'patterns', 'comments.html'), pattern_comments)

def _encode_image(image_path):
    try:
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    except Exception:
        return ''

def _pattern_slug_for_type(t):
    m = {
        'hero': 'hero-section',
        'banner': 'hero-standard',
        'features': 'features-grid-3-col',
        'services': 'features-two-col',
        'gallery': 'gallery-masonry',
        'faq': 'faq-accordion',
        'testimonials': 'testimonials-grid',
        'pricing': 'pricing-table-basic',
        'contact': 'contact-simple',
        'newsletter': 'newsletter-wide',
        'team': 'team-members-grid',
        'portfolio': 'portfolio-grid',
        'cta': 'cta-banner'
    }
    for k, v in m.items():
        if k in t:
            return v
    return ''

def _mapping_to_fse(theme_dir, mapping):
    try:
        parts_dir = os.path.join(theme_dir, 'parts')
        templates_dir = os.path.join(theme_dir, 'templates')
        os.makedirs(parts_dir, exist_ok=True)
        os.makedirs(templates_dir, exist_ok=True)
        regions = []
        if isinstance(mapping, dict):
            regions = mapping.get('regions') or mapping.get('sections') or []
        elif isinstance(mapping, list):
            regions = mapping
        blocks = []
        for i, r in enumerate(regions):
            t = ''
            if isinstance(r, dict):
                t = (r.get('type') or r.get('name') or r.get('label') or '').lower()
            elif isinstance(r, str):
                t = r.lower()
            slug = _pattern_slug_for_type(t)
            if slug:
                blocks.append(f'<!-- wp:pattern {{"slug":"img2html/{slug}"}} /-->')
            else:
                content_html = ''
                title = ''
                if isinstance(r, dict):
                    content_html = r.get('pattern_content') or r.get('html') or ''
                    title = r.get('title') or r.get('label') or ''
                if content_html:
                    blocks.append(content_html)
                    try:
                        patterns_dir = os.path.join(theme_dir, 'patterns')
                        os.makedirs(patterns_dir, exist_ok=True)
                        fname = f"auto_{i+1}.html"
                        _write_file(os.path.join(patterns_dir, fname), content_html)
                    except Exception:
                        pass
                else:
                    if not title:
                        title = 'Sección'
                    blocks.append(f'<!-- wp:group {"layout":{"type":"constrained"}} -->\n<div class="wp-block-group">\n<!-- wp:heading {"textAlign":"center"} -->\n<h2 class="has-text-align-center">{title}</h2>\n<!-- /wp:heading -->\n</div>\n<!-- /wp:group -->')
        content = "\n".join(blocks)
        fp = f"""<!-- wp:template-part {{"slug":"header"}} /-->
<!-- wp:group {{"tagName":"main","layout":{{"type":"constrained"}}}} -->
<main id="main-content">
{content}
</main>
<!-- /wp:group -->
<!-- wp:template-part {{"slug":"footer"}} /-->
"""
        _write_file(os.path.join(templates_dir, 'front-page-mapped.html'), fp)
    except Exception:
        pass

def _plan_to_fse(theme_dir, plan, dna=None):
    try:
        templates_dir = os.path.join(theme_dir, 'templates')
        os.makedirs(templates_dir, exist_ok=True)
        blocks = []
        palette = []
        if isinstance(dna, dict):
            palette = dna.get('palette') or []
        slug_to_hex = {}
        for p in palette:
            s = p.get('slug'); c = p.get('color')
            if s and c:
                slug_to_hex[s] = c
        for sec in (plan.get('sections') or []):
            label = sec.get('label') or 'Sección'
            pat = (sec.get('pattern') or '').lower()
            rows = sec.get('layout_rows') or []
            use_cover = ('hero' in pat)
            overlay_slug = 'primary'
            is_dark = False
            if slug_to_hex.get('primary'):
                lum = _lum(_hex_to_rgb(slug_to_hex['primary']))
                if lum < 0.25 and slug_to_hex.get('secondary'):
                    overlay_slug = 'secondary'
                is_dark = lum < 0.5
            if use_cover:
                blocks.append(f'<!-- wp:cover {{"dimRatio":20,"overlayColor":"{overlay_slug}","isDark":{str(is_dark).lower()}}} -->')
                blocks.append('<div class="wp-block-cover">')
                blocks.append(f'<span aria-hidden="true" class="wp-block-cover__background has-{overlay_slug}-background-color has-background-dim"></span>')
                blocks.append('<div class="wp-block-cover__inner-container">')
                if is_dark:
                    blocks.append('<!-- wp:heading {"textAlign":"center","level":2,"textColor":"background"} -->')
                    blocks.append(f'<h2 class="has-text-align-center has-background-color has-text-color">{label}</h2>')
                else:
                    blocks.append('<!-- wp:heading {"textAlign":"center","level":2,"textColor":"text"} -->')
                    blocks.append(f'<h2 class="has-text-align-center has-text-color">{label}</h2>')
                blocks.append('<!-- /wp:heading -->')
            else:
                group_meta = '"layout":{"type":"constrained"}'
                if slug_to_hex.get('surface'):
                    group_meta = group_meta + ',"backgroundColor":"surface"'
                elif slug_to_hex.get('background'):
                    group_meta = group_meta + ',"backgroundColor":"background"'
                blocks.append(f'<!-- wp:group {{{group_meta}}} -->')
                blocks.append('<div class="wp-block-group">')
                blocks.append('<!-- wp:heading {"level":2,"textColor":"text"} -->')
                blocks.append(f'<h2 class="has-text-color">{label}</h2>')
                blocks.append('<!-- /wp:heading -->')
            for row in rows:
                cols = row.get('columns') or []
                ratios = row.get('ratios_percent') or []
                if not cols:
                    continue
                blocks.append('<!-- wp:columns {"align":"wide","style":{"spacing":{"blockGap":"16px"}}} -->')
                blocks.append('<div class="wp-block-columns alignwide">')
                n = len(cols)
                for i, _ in enumerate(cols):
                    pct = '0%'
                    if i < len(ratios) and isinstance(ratios[i], (int, float)):
                        pct = f"{int(ratios[i])}%"
                    elif n > 0:
                        pct = f"{int(round(100/n))}%"
                    blocks.append('<!-- wp:column {"width":"%s","style":{"spacing":{"padding":{"top":"12px","bottom":"12px"}}}} -->' % pct)
                    blocks.append(f'<div class="wp-block-column" style="flex-basis:{pct};padding-top:12px;padding-bottom:12px">')
                    blocks.append('<!-- wp:group {"layout":{"type":"constrained"},"style":{"spacing":{"blockGap":"8px"}}} -->')
                    blocks.append('<div class="wp-block-group"></div>')
                    blocks.append('<!-- /wp:group -->')
                    blocks.append('</div>')
                    blocks.append('<!-- /wp:column -->')
                blocks.append('</div>')
                blocks.append('<!-- /wp:columns -->')
            if use_cover:
                blocks.append('</div>')
                blocks.append('</div>')
                blocks.append('<!-- /wp:cover -->')
            else:
                blocks.append('</div>')
                blocks.append('<!-- /wp:group -->')
        content = "\n".join(blocks)
        layout = f"""<!-- wp:template-part {{"slug":"header"}} /-->
<!-- wp:group {{"tagName":"main","layout":{{"type":"constrained"}}}} -->
<main>
{content}
</main>
<!-- /wp:group -->
<!-- wp:template-part {{"slug":"footer"}} /-->
"""
        _write_file(os.path.join(templates_dir, 'front-page-layout.html'), layout)
    except Exception:
        pass

def refine_and_generate_wp(temp_out_dir: str, info_md: str, plan: Dict, theme_dir: str, images=None, dna=None):
    html = _read_file(os.path.join(temp_out_dir, 'index.html'))
    css = _read_file(os.path.join(temp_out_dir, 'styles.css'))
    used_ai = False
    provider_used = ''
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        runtime_path = os.path.join(base_dir, 'wp_theme', 'prompts', 'runtime.json')
        runtime = _read_json(runtime_path) or {}
        selection = runtime.get('selection') or {}
        temp = 0.1
        top_p = selection.get('top_p')
        strategy = (selection.get('strategy') or '').lower()
        provider = ''
        model_name = ''
        api_key = ''
        endpoint = ''
        chosen_local = None
        for lm in (runtime.get('local_models') or []):
            if lm.get('enabled') and (lm.get('runner') or '') == 'ollama':
                chosen_local = lm
                break
        chosen_remote_google = None
        chosen_remote_openai = None
        for rm in (runtime.get('remote_models') or []):
            if rm.get('enabled') and rm.get('provider') == 'google':
                chosen_remote_google = rm
            if rm.get('enabled') and rm.get('provider') == 'openai':
                chosen_remote_openai = rm
        if 'prefer_local' in strategy and chosen_local:
            provider = 'ollama'
            model_name = chosen_local.get('id') or chosen_local.get('name') or 'llama3.1:8b'
            endpoint = os.environ.get('OLLAMA_ENDPOINT') or 'http://localhost:11434/api/generate'
        elif chosen_remote_google:
            provider = 'google'
            model_name = chosen_remote_google.get('name') or 'gemini-1.5-pro-latest'
            for name in (chosen_remote_google.get('tokens') or []):
                val = os.environ.get(name)
                if val:
                    api_key = val
                    break
            if not api_key:
                api_key = os.environ.get('GOOGLE_API_KEY') or ''
        elif chosen_remote_openai:
            provider = 'openai'
            model_name = chosen_remote_openai.get('name') or 'gpt-4.1'
            endpoint = chosen_remote_openai.get('endpoint') or 'https://api.openai.com/v1/chat/completions'
            for name in (chosen_remote_openai.get('tokens') or []):
                val = os.environ.get(name)
                if val:
                    api_key = val
                    break
            if not api_key:
                api_key = os.environ.get('OPENAI_API_KEY') or ''
        else:
            provider = 'google'
            model_name = 'gemini-1.5-pro-latest'
            api_key = os.environ.get('GOOGLE_API_KEY') or ''
        prompt_md = _read_file(os.path.join(base_dir, 'docs', 'prompt.md'))
        prompt = (
            "MODO ESTRICTO: Clonación visual estricta del diseño. Prioriza REFERENCIAS VISUALES sobre HTML base y sobre OCR. "
            "Replica márgenes y micro-espaciados exactos usando style=\"margin-top/bottom/left/right\" cuando sea necesario. "
            "Infiera tipografía real (Serif/Sans y peso aparente Bold/Light) y ajuste heading/paragraph acorde. "
            "Si el OCR alucina, corrige usando visión. "
            "Genera un tema de bloques (FSE) con theme.json v3 y plantillas. "
            "Archivos esperados en JSON: style.css, functions.php, theme.json, "
            "parts/header.html, parts/footer.html, templates/index.html, templates/single.html, "
            "templates/page.html, templates/404.html. "
            "Para core/columns: NO USES anchos automáticos si el diseño es asimétrico; usa porcentajes exactos. "
        )
        strict = (
            "Rol: Maquetador Web Senior Experto en WordPress FSE. "
            "Entrega SOLO JSON válido. Usa REFERENCIAS VISUALES como fuente de verdad. "
        )
        selected = []
        if images:
            selected = images[:5]
        elif plan.get('sections'):
            for sec in plan['sections'][:3]:
                if sec.get('images'):
                    selected.append(sec['images'][0])
        response_text = ''
        provider_used = provider
        if provider == 'google' and api_key:
            import google.generativeai as genai
            gcfg = {"response_mime_type": "application/json", "temperature": 0.1}
            if isinstance(top_p, (int, float)):
                gcfg["top_p"] = float(top_p)
            config = genai.GenerationConfig(**gcfg)
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_name, generation_config=config)
            content = [
                {"role":"user","parts":[{"text":prompt}]},
                {"role":"user","parts":[{"text":"SISTEMA"},{"text":strict}]},
                {"role":"user","parts":[{"text":"PROMPT_MD"},{"text":prompt_md}]},
                {"role":"user","parts":[{"text":"HTML"},{"text":html}]},
                {"role":"user","parts":[{"text":"CSS"},{"text":css}]},
                {"role":"user","parts":[{"text":"INFO"},{"text":info_md}]},
                {"role":"user","parts":[{"text":"PLAN"},{"text":json.dumps(plan, ensure_ascii=False)}]},
            ]
            content.append({"role":"user","parts":[{"text":"Si el PLAN incluye 'layout_rows' con columnas detectadas, replica esas columnas usando core/columns y grupos. Usa 'ratios_percent' para asignar 'width' en cada columna (porcentaje)."}]})
            if selected:
                content.append({"role":"user","parts":[{"text":"Referencias visuales"}]})
                for p in selected:
                    b64 = _encode_image(p)
                    if b64:
                        content.append({"role":"user","parts":[{"inline_data":{"mime_type":"image/jpeg","data": b64}}]})
            content.append({"role":"user","parts":[{"text":"Primero entrega JSON 'mapping' con regiones visuales → bloques FSE (core/cover, core/columns, core/group, core/heading, core/paragraph, core/image, core/navigation, core/query). Si la imagen es diseño complejo, replica con columns/group/heading/paragraph; si es foto simple, usa image/cover. Luego entrega el JSON con archivos esperados."}]})
            resp = model.generate_content(content)
            response_text = getattr(resp, 'text', '') or ''
            if not response_text:
                try:
                    if getattr(resp, 'candidates', None):
                        parts = resp.candidates[0].content.parts
                        if parts and hasattr(parts[0], 'text'):
                            response_text = parts[0].text or ''
                except Exception:
                    response_text = ''
        elif provider == 'openai' and api_key and endpoint:
            msgs = []
            msgs.append({"role":"system","content":"Eres un Maquetador Web Senior Experto en WordPress FSE. Debes responder SOLO con un objeto JSON válido. Prioriza REFERENCIAS VISUALES sobre HTML y OCR. Genera clonación visual estricta con micro-espaciados y tipografía inferida."})
            ucontent = [{"type":"text","text":prompt}, {"type":"text","text":"PROMPT_MD"}, {"type":"text","text":prompt_md}, {"type":"text","text":"HTML"}, {"type":"text","text":html}, {"type":"text","text":"CSS"}, {"type":"text","text":css}, {"type":"text","text":"INFO"}, {"type":"text","text":info_md}, {"type":"text","text":"PLAN"}, {"type":"text","text":json.dumps(plan, ensure_ascii=False)}]
            ucontent.append({"type":"text","text":"Si el PLAN incluye 'layout_rows' con columnas detectadas, replica esas columnas usando core/columns y grupos. Usa 'ratios_percent' para asignar 'width' en cada columna (porcentaje)."})
            if selected:
                ucontent.append({"type":"text","text":"Referencias visuales (PRIORIDAD MÁXIMA)"})
                for p in selected:
                    b64 = _encode_image(p)
                    if b64:
                        ucontent.append({"type":"input_image","image_url":{"url":"data:image/jpeg;base64,"+b64}})
            ucontent.append({"type":"text","text":"Primero entrega JSON 'mapping' con regiones visuales → bloques FSE (core/cover, core/columns, core/group, core/heading, core/paragraph, core/image, core/navigation, core/query). Si la imagen es diseño complejo, replica con columns/group/heading/paragraph; si es foto simple, usa image/cover. Luego entrega el JSON con archivos esperados."})
            msgs.append({"role":"user","content":ucontent})
            body = {
                "model": model_name,
                "messages": msgs,
                "response_format": {"type": "json_object"}
            }
            body["temperature"] = 0.1
            if isinstance(top_p, (int, float)):
                body["top_p"] = float(top_p)
            req = urllib.request.Request(endpoint, data=json.dumps(body).encode('utf-8'), headers={"Authorization": "Bearer "+api_key, "Content-Type": "application/json"})
            ctx = ssl.create_default_context()
            with urllib.request.urlopen(req, context=ctx) as resp:
                raw = resp.read()
                obj = json.loads(raw.decode('utf-8'))
                response_text = obj.get('choices', [{}])[0].get('message', {}).get('content', '') or ''
        elif provider == 'ollama' and model_name:
            prompt_text = (
                prompt + "\nPROMPT_MD\n" + prompt_md + "\nHTML\n" + html + "\nCSS\n" + css + "\nINFO\n" + info_md + "\nPLAN\n" + json.dumps(plan, ensure_ascii=False) + "\nSi el PLAN incluye 'layout_rows' con columnas detectadas, replica esas columnas usando core/columns y grupos. Usa 'ratios_percent' para asignar 'width' en cada columna (porcentaje).\nENTREGA SOLO JSON."
            )
            body = {"model": model_name, "prompt": prompt_text, "format": "json", "stream": False}
            opts = {"temperature": 0.1}
            if isinstance(top_p, (int, float)):
                opts["top_p"] = float(top_p)
            if opts:
                body["options"] = opts
            req = urllib.request.Request(endpoint, data=json.dumps(body).encode('utf-8'), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req) as resp:
                raw = resp.read()
                obj = json.loads(raw.decode('utf-8'))
                response_text = obj.get('response', '') or ''
        else:
            _fallback_wp(theme_dir, html, css, plan)
            return {"used_ai": used_ai, "provider": provider_used}
        data = _extract_json(response_text)
        if not isinstance(data, dict):
            _fallback_wp(theme_dir, html, css, plan)
            return {"used_ai": used_ai, "provider": provider_used}
        os.makedirs(os.path.join(theme_dir, 'parts'), exist_ok=True)
        os.makedirs(os.path.join(theme_dir, 'templates'), exist_ok=True)
        mapping = data.pop('mapping', None)
        if mapping:
            _mapping_to_fse(theme_dir, mapping)
        if plan and isinstance(plan, dict):
            _plan_to_fse(theme_dir, plan, dna)
        for name, value in data.items():
            _write_file(os.path.join(theme_dir, name), value)
        used_ai = True
        return {"used_ai": used_ai, "provider": provider_used}
    except Exception:
        _fallback_wp(theme_dir, html, css, plan)
        return {"used_ai": used_ai, "provider": provider_used}