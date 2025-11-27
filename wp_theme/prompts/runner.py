import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
PROMPTS_DIR = Path(__file__).resolve().parent

def load_json(p):
    try:
        with open(p, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

def write_file(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def read_text(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return ''

def merge_theme_styles(theme_obj, styles_obj):
    theme_obj = theme_obj or {}
    styles_obj = styles_obj or {}
    theme_styles = theme_obj.get('styles') or {}
    styles_styles = styles_obj.get('styles') or {}
    for k, v in styles_styles.items():
        if k not in theme_styles:
            theme_styles[k] = v
        else:
            if isinstance(v, dict):
                theme_styles[k].update(v)
            else:
                theme_styles[k] = v
    settings = theme_obj.get('settings') or {}
    styles_settings = styles_obj.get('settings') or {}
    if styles_settings:
        colors = styles_settings.get('color')
        if colors:
            pal = colors.get('palette')
            if pal:
                settings.setdefault('color', {}).setdefault('palette', pal)
        typo = styles_settings.get('typography')
        if typo:
            fam = typo.get('fontFamilies')
            if fam:
                settings.setdefault('typography', {}).setdefault('fontFamilies', fam)
    theme_obj['styles'] = theme_styles
    theme_obj['settings'] = settings
    return theme_obj

def stub_pattern(title):
    return f"""<!-- wp:group -->\n<div class=\"wp-block-group\">\n<!-- wp:heading {{\"level\":2}} -->\n<h2>{title}</h2>\n<!-- /wp:heading -->\n<!-- wp:paragraph -->\n<p>Contenido de patrón {title}</p>\n<!-- /wp:paragraph -->\n</div>\n<!-- /wp:group -->\n"""

def build_templates_from_catalog(catalog_path, target_dir):
    data = load_json(catalog_path) or {}
    items = data.get('customTemplates') or []
    for t in items:
        name = t.get('name')
        if not name:
            continue
        fn = Path(target_dir) / 'templates' / f'{name}.html'
        if name == 'blank':
            content = """<!-- wp:group {\"tagName\":\"main\"} -->\n<main></main>\n<!-- /wp:group -->\n"""
        elif name == 'page-no-title':
            content = """<!-- wp:template-part {\"slug\":\"header\"} /-->\n<!-- wp:post-content /-->\n<!-- wp:template-part {\"slug\":\"footer\"} /-->\n"""
        elif name == 'landing-page':
            content = """<!-- wp:template-part {\"slug\":\"header\"} /-->\n<!-- wp:cover {\"dimRatio\":20} -->\n<div class=\"wp-block-cover\"><span aria-hidden=\"true\" class=\"wp-block-cover__background has-background-dim-20 has-background-dim\"></span><div class=\"wp-block-cover__inner-container\"><!-- wp:heading {\"textAlign\":\"center\"} --><h2 class=\"has-text-align-center\">Bienvenido</h2><!-- /wp:heading --></div></div>\n<!-- /wp:cover -->\n<!-- wp:template-part {\"slug\":\"footer\"} /-->\n"""
        elif name in ('sidebar-left', 'sidebar-right'):
            left = name == 'sidebar-left'
            col1 = '<!-- wp:template-part {\"slug\":\"sidebar\"} /-->' if left else '<!-- wp:post-content /-->'
            col2 = '<!-- wp:post-content /-->' if left else '<!-- wp:template-part {\"slug\":\"sidebar\"} /-->'
            content = f"""<!-- wp:template-part {{\"slug\":\"header\"}} /-->\n<!-- wp:columns -->\n<div class=\"wp-block-columns\"><!-- wp:column --><div class=\"wp-block-column\">{col1}</div><!-- /wp:column --><!-- wp:column --><div class=\"wp-block-column\">{col2}</div><!-- /wp:column --></div>\n<!-- /wp:columns -->\n<!-- wp:template-part {{\"slug\":\"footer\"}} /-->\n"""
        elif name == 'full-width':
            content = """<!-- wp:template-part {\"slug\":\"header\"} /-->\n<!-- wp:group {\"layout\":{\"type\":\"constrained\",\"contentSize\":\"1200px\"}} -->\n<div class=\"wp-block-group\"><!-- wp:post-content /--></div>\n<!-- /wp:group -->\n<!-- wp:template-part {\"slug\":\"footer\"} /-->\n"""
        elif name == 'blog-grid':
            content = """<!-- wp:template-part {\"slug\":\"header\"} /-->\n<!-- wp:query {\"query\":{\"perPage\":9}} -->\n<div class=\"wp-block-query\"><!-- wp:post-template --><!-- wp:group {\"layout\":{\"type\":\"constrained\"}} --><div class=\"wp-block-group\"><!-- wp:post-featured-image /--><!-- wp:post-title {\"isLink\":true} /--></div><!-- /wp:group --><!-- /wp:post-template --><!-- wp:query-pagination /--></div>\n<!-- /wp:query -->\n<!-- wp:template-part {\"slug\":\"footer\"} /-->\n"""
        else:
            content = """<!-- wp:template-part {\"slug\":\"header\"} /-->\n<!-- wp:post-content /-->\n<!-- wp:template-part {\"slug\":\"footer\"} /-->\n"""
        write_file(fn, content)

def build_parts_from_catalog(catalog_path, target_dir):
    data = load_json(catalog_path) or {}
    tps = data.get('templateParts') or []
    for tp in tps:
        name = tp.get('name')
        if not name:
            continue
        if name == 'header-centered':
            content = """<!-- wp:group {\"tagName\":\"header\",\"layout\":{\"type\":\"flex\",\"justifyContent\":\"center\"}} --><header class=\"wp-block-group\"><!-- wp:site-logo /--><!-- wp:site-title /--><!-- wp:navigation /--></header><!-- /wp:group -->\n"""
            write_file(Path(target_dir) / 'parts' / 'header-centered.html', content)
        elif name == 'sidebar':
            content = """<!-- wp:group {\"tagName\":\"aside\"} --><aside class=\"wp-block-group\"><!-- wp:search /--><!-- wp:categories /--><!-- wp:latest-posts /--><!-- wp:tag-cloud /--></aside><!-- /wp:group -->\n"""
            write_file(Path(target_dir) / 'parts' / 'sidebar.html', content)
        elif name == 'comments':
            content = """<!-- wp:comments -->\n<div class=\"wp-block-comments\"><!-- wp:comments-title /--><!-- wp:comment-template -->\n<!-- wp:avatar /--><!-- wp:comment-author-name /--><!-- wp:comment-date /--><!-- wp:comment-content /--><!-- wp:comment-reply-link /-->\n<!-- /wp:comment-template --><!-- wp:comments-pagination /--></div>\n<!-- /wp:comments -->\n"""
            write_file(Path(target_dir) / 'parts' / 'comments.html', content)

def build_patterns_from_catalog(catalog_path, target_dir):
    data = load_json(catalog_path) or {}
    slugs = data.get('patterns') or []
    for slug in slugs:
        name = slug.split('/')[-1]
        fn = Path(target_dir) / 'patterns' / f'{name}.html'
        title = name.replace('-', ' ').title()
        write_file(fn, stub_pattern(title))

def run_offline_steps(overview):
    target_dir = (PROMPTS_DIR / '..').resolve()
    seeds = overview.get('seeds') or {}
    ct = seeds.get('customTemplates')
    tp = seeds.get('templateParts')
    pat = seeds.get('patterns')
    styles = seeds.get('styles')
    theme = seeds.get('theme')
    if ct:
        build_templates_from_catalog((PROMPTS_DIR / ct).resolve(), target_dir)
    if tp:
        build_parts_from_catalog((PROMPTS_DIR / tp).resolve(), target_dir)
    if pat:
        build_patterns_from_catalog((PROMPTS_DIR / pat).resolve(), target_dir)
    if styles and theme:
        styles_obj = load_json((PROMPTS_DIR / styles).resolve())
        theme_obj = load_json((PROMPTS_DIR / theme).resolve())
        merged = merge_theme_styles(theme_obj, styles_obj)
        with open(target_dir / 'theme.json', 'w', encoding='utf-8') as f:
            json.dump(merged, f, ensure_ascii=False, indent=2)

class ThemeBuilder:
    def __init__(self, output_dir: str, context: dict = None):
        self.output_dir = Path(output_dir)
        self.context = context or {}
        self.overview = load_json(PROMPTS_DIR / '00_overview.json') or {}
        self.runtime = load_json(PROMPTS_DIR / 'runtime.json') or {}
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def bootstrap(self):
        run_offline_steps(self.overview)
        if self.context.get('palette'):
            tpath = self.output_dir / 'theme.json'
            theme = load_json(tpath) or {"version":3, "settings":{}}
            settings = theme.get('settings') or {}
            color = settings.get('color') or {}
            color['palette'] = [
                {"name":"Background","slug":"background","color": self.context['palette'][0]['color']},
                {"name":"Text","slug":"text","color": self.context['palette'][1]['color']},
                {"name":"Primary","slug":"primary","color": self.context['palette'][2]['color']}
            ]
            settings['color'] = color
            typo = settings.get('typography') or {}
            ff = self.context.get('typography', {}).get('fontFamily')
            if ff:
                typo['fontFamilies'] = [{"fontFamily": ff, "slug": "system", "name": "System"}]
            settings['typography'] = typo
            theme['settings'] = settings
            with open(tpath, 'w', encoding='utf-8') as f:
                json.dump(theme, f, ensure_ascii=False, indent=2)

    def run_prompt(self, name: str, context: dict = None):
        p = (PROMPTS_DIR / name).resolve()
        if not p.exists():
            return False
        data = load_json(p) or {}
        out = self.output_dir
        if 'styles' in data or 'settings' in data:
            tpath = out / 'theme.json'
            theme = load_json(tpath) or {}
            merged = merge_theme_styles(theme, data)
            with open(tpath, 'w', encoding='utf-8') as f:
                json.dump(merged, f, ensure_ascii=False, indent=2)
            return True
        if 'customTemplates' in data:
            build_templates_from_catalog(p, out)
            return True
        if 'templateParts' in data:
            build_parts_from_catalog(p, out)
            return True
        if 'patterns' in data:
            build_patterns_from_catalog(p, out)
            return True
        return False

def main():
    overview = load_json(PROMPTS_DIR / '00_overview.json') or {}
    runtime = load_json(PROMPTS_DIR / 'runtime.json') or {}
    use_llm = False
    run_offline_steps(overview)
    print('Pipeline completado en modo offline')

if __name__ == '__main__':
    main()