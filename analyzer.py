import os
import re
import unicodedata

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