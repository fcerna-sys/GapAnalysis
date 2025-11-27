import os
import re
import unicodedata
from PIL import Image
try:
    import colorgram
except Exception:
    colorgram = None

KEYWORDS = {
    'hero': 'Hero',
    'banner': 'Banner',
    'header': 'Header',
    'nav': 'Navegación',
    'about': 'Sobre Nosotros',
    'services': 'Servicios',
    'portfolio': 'Portafolio',
    'projects': 'Proyectos',
    'blog': 'Blog',
    'posts': 'Artículos',
    'contact': 'Contacto',
    'cta': 'CTA',
    'faq': 'FAQ',
    'testimonials': 'Testimonios',
    'features': 'Características',
    'pricing': 'Precios',
    'footer': 'Footer'
}

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^a-zA-Z0-9\-\_]+', '-', text)
    text = text.strip('-').lower()
    return text or 'section'

def infer_section_label(name):
    lower = name.lower()
    for k, label in KEYWORDS.items():
        if k in lower:
            return label
    return name.title()

def parse_order(name):
    m = re.match(r'^(\d{1,3})[\-_\s]', name)
    if m:
        return int(m.group(1))
    m2 = re.search(r'(\d{1,3})', name)
    if m2:
        return int(m2.group(1))
    return 9999

def analyze_images(paths):
    items = []
    for p in paths:
        base = os.path.basename(p)
        name, _ = os.path.splitext(base)
        order = parse_order(name)
        label = infer_section_label(name)
        slug = slugify(label)
        items.append({'path': p, 'name': name, 'order': order, 'label': label, 'slug': slug})
    items.sort(key=lambda x: (x['order'], x['name']))
    sections = []
    by_slug = {}
    for it in items:
        key = it['slug']
        if key in by_slug:
            idx = by_slug[key]
            sections[idx]['images'].append(it['path'])
        else:
            by_slug[key] = len(sections)
            sections.append({'name': it['name'], 'label': it['label'], 'slug': it['slug'], 'images': [it['path']]})
    title = items[0]['label'] if items else 'Sitio'
    return {'title': title, 'sections': sections, 'count': len(items)}

def _rgb_to_hex(rgb):
    r, g, b = rgb
    return '#%02x%02x%02x' % (r, g, b)

def _luminance(rgb):
    r, g, b = [c/255.0 for c in rgb]
    return 0.2126*r + 0.7152*g + 0.0722*b

def _most_saturated(colors):
    best = None
    score = -1
    for c in colors:
        if hasattr(c, 'rgb'): rgb = (c.rgb.r, c.rgb.g, c.rgb.b)
        else: rgb = c
        r, g, b = rgb
        maxc = max(r, g, b); minc = min(r, g, b)
        sat = (maxc - minc)
        if sat > score:
            score = sat; best = rgb
    return best or (0, 120, 255)

def extract_design_dna(image_paths):
    if not image_paths:
        return {"palette": [{"slug":"background","color":"#ffffff"},{"slug":"text","color":"#111111"},{"slug":"primary","color":"#3b82f6"}], "typography": {"fontFamily": "Inter, system-ui, sans-serif"}}
    path = image_paths[0]
    palette = []
    if colorgram:
        try:
            colors = colorgram.extract(path, 6)
            colors_sorted = sorted(colors, key=lambda c: _luminance((c.rgb.r, c.rgb.g, c.rgb.b)))
            bg = colors_sorted[-1]
            text = colors_sorted[0]
            primary = _most_saturated(colors)
            palette = [
                {"slug": "background", "color": _rgb_to_hex((bg.rgb.r, bg.rgb.g, bg.rgb.b))},
                {"slug": "text", "color": _rgb_to_hex((text.rgb.r, text.rgb.g, text.rgb.b))},
                {"slug": "primary", "color": _rgb_to_hex(primary)}
            ]
        except Exception:
            palette = []
    if not palette:
        try:
            img = Image.open(path).convert('RGB')
            small = img.resize((64, 64))
            pixels = list(small.getdata())
            pixels_sorted = sorted(pixels, key=_luminance)
            bg = pixels_sorted[-1]
            text = pixels_sorted[0]
            primary = _most_saturated(pixels)
            palette = [
                {"slug": "background", "color": _rgb_to_hex(bg)},
                {"slug": "text", "color": _rgb_to_hex(text)},
                {"slug": "primary", "color": _rgb_to_hex(primary)}
            ]
        except Exception:
            palette = [{"slug":"background","color":"#ffffff"},{"slug":"text","color":"#111111"},{"slug":"primary","color":"#3b82f6"}]
    return {"palette": palette, "typography": {"fontFamily": "Inter, system-ui, sans-serif"}}

PATTERN_MAP = {
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

def identify_pattern(section):
    label = section.get('label', '')
    slug = section.get('slug', '')
    text = (label + ' ' + slug).lower()
    for key, pat in PATTERN_MAP.items():
        if key in text:
            return pat
    return 'features-with-media'