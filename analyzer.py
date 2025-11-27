import os
import re
import unicodedata
from PIL import Image
try:
    import cv2
    import numpy as np
except Exception:
    cv2 = None
    np = None
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

def _is_grayscale(rgb, tolerance=10):
    r, g, b = rgb
    return abs(r-g) < tolerance and abs(g-b) < tolerance

def extract_design_dna(image_paths):
    default_palette = [{"slug":"background","color":"#ffffff"},{"slug":"text","color":"#111111"},{"slug":"primary","color":"#3b82f6"}]
    if not image_paths:
        return {"palette": default_palette, "typography": {"fontFamily": "Inter, system-ui, sans-serif"}}
    path = image_paths[0]
    palette = []
    if colorgram:
        try:
            colors = colorgram.extract(path, 12)
            rgb_colors = [(c.rgb.r, c.rgb.g, c.rgb.b) for c in colors]
            by_lum = sorted(rgb_colors, key=_luminance)
            bg_color = by_lum[-1] if by_lum else (255,255,255)
            text_color = by_lum[0] if by_lum else (17,17,17)
            primary_color = None
            max_sat = -1
            for rgb in rgb_colors:
                if _is_grayscale(rgb, 20):
                    continue
                sat = max(rgb) - min(rgb)
                if sat > max_sat:
                    max_sat = sat
                    primary_color = rgb
            if not primary_color:
                primary_color = (59,130,246)
            secondary_color = text_color
            if len(by_lum) > 1:
                secondary_color = by_lum[1]
            palette = [
                {"slug": "background", "color": _rgb_to_hex(bg_color)},
                {"slug": "text", "color": _rgb_to_hex(text_color)},
                {"slug": "primary", "color": _rgb_to_hex(primary_color)},
                {"slug": "secondary", "color": _rgb_to_hex(secondary_color)}
            ]
        except Exception:
            palette = []
    if not palette:
        try:
            img = Image.open(path).convert('RGB')
            small = img.resize((96, 96))
            pixels = list(small.getdata())
            by_lum = sorted(pixels, key=_luminance)
            bg_color = by_lum[-1] if by_lum else (255,255,255)
            text_color = by_lum[0] if by_lum else (17,17,17)
            primary_color = None
            max_sat = -1
            for rgb in pixels:
                if _is_grayscale(rgb, 20):
                    continue
                sat = max(rgb) - min(rgb)
                if sat > max_sat:
                    max_sat = sat
                    primary_color = rgb
            if not primary_color:
                primary_color = (59,130,246)
            secondary_color = text_color
            if len(by_lum) > 1:
                secondary_color = by_lum[1]
            palette = [
                {"slug": "background", "color": _rgb_to_hex(bg_color)},
                {"slug": "text", "color": _rgb_to_hex(text_color)},
                {"slug": "primary", "color": _rgb_to_hex(primary_color)},
                {"slug": "secondary", "color": _rgb_to_hex(secondary_color)}
            ]
        except Exception:
            palette = default_palette
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
    'cta': 'cta-banner',
    'hero-split': 'hero-split-screen'
}

def identify_pattern(section):
    label = section.get('label', '')
    slug = section.get('slug', '')
    text = (label + ' ' + slug).lower()
    rows = section.get('layout_rows') or []
    if rows:
        r0 = rows[0]
        cols = r0.get('columns') or []
        rp = r0.get('ratios_percent') or []
        if len(cols) == 2:
            if len(rp) >= 2 and isinstance(rp[0], (int, float)) and isinstance(rp[1], (int, float)):
                diff = abs(int(rp[0]) - int(rp[1]))
                if diff <= 10:
                    return 'hero-split-screen-balanced'
                else:
                    return 'hero-split-screen-asymmetric'
            return PATTERN_MAP.get('hero-split')
        if len(cols) >= 3:
            return 'features-grid-3-col'
    for key, pat in PATTERN_MAP.items():
        if key in text:
            return pat
    return 'features-with-media'

def identify_pattern_variant(section):
    rows = section.get('layout_rows') or []
    if not rows:
        return ''
    r0 = rows[0]
    rp = r0.get('ratios_percent') or []
    cols = r0.get('columns') or []
    if len(cols) == 2 and len(rp) >= 2 and isinstance(rp[0], (int, float)) and isinstance(rp[1], (int, float)):
        diff = abs(int(rp[0]) - int(rp[1]))
        return 'balanced' if diff <= 10 else 'asymmetric'
    return ''

def _row_energy(img):
    w, h = img.size
    px = img.convert('L').load()
    arr = []
    for y in range(h):
        s = 0
        last = px[0, y]
        for x in range(1, w):
            v = px[x, y]
            d = v - last
            if d < 0:
                d = -d
            s += d
            last = v
        arr.append(s)
    return arr

def _find_cuts(energy, min_gap):
    h = len(energy)
    if h == 0:
        return []
    avg = sum(energy) / float(h)
    thr = avg * 1.5
    cuts = []
    last = 0
    for i, e in enumerate(energy):
        if e > thr and (i - last) >= min_gap:
            cuts.append(i)
            last = i
    return cuts

def _col_energy(img):
    w, h = img.size
    px = img.convert('L').load()
    arr = []
    for x in range(w):
        s = 0
        last = px[x, 0]
        for y in range(1, h):
            v = px[x, y]
            d = v - last
            if d < 0:
                d = -d
            s += d
            last = v
        arr.append(s)
    return arr

def _find_vcuts(energy, min_gap):
    w = len(energy)
    if w == 0:
        return []
    avg = sum(energy) / float(w)
    thr = avg * 1.5
    cuts = []
    last = 0
    for i, e in enumerate(energy):
        if e > thr and (i - last) >= min_gap:
            cuts.append(i)
            last = i
    return cuts

def segment_columns(path, out_dir, min_width=160, precise=False):
    if cv2 is not None and np is not None:
        try:
            im = cv2.imread(path)
            if im is None:
                raise RuntimeError('cv2 failed to read')
            h, w = im.shape[:2]
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (5, 5), 0)
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            abs_x = np.abs(sobelx)
            col_energy = abs_x.sum(axis=0)
            col_energy = col_energy / (col_energy.max() + 1e-9)
            kernel = np.ones((15,), dtype=np.float64) / 15.0
            smooth = np.convolve(col_energy, kernel, mode='same')
            mu = smooth.mean(); sigma = smooth.std()
            thr = mu + (1.2 if precise else 1.5) * sigma
            cand_cuts = [i for i, e in enumerate(smooth) if e > thr]
            edges = cv2.Canny(gray, 50, 150)
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=(90 if precise else 120), minLineLength=int(0.55*h), maxLineGap=20)
            line_xs = []
            if lines is not None:
                for l in lines[:,0]:
                    x1,y1,x2,y2 = l
                    if abs(x1 - x2) <= 3:
                        line_xs.append(int((x1 + x2) // 2))
            hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
            avg_cols = hsv.mean(axis=0)
            Z = avg_cols.astype(np.float32)
            K = 3 if precise else 2
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.2)
            try:
                ret, labels, centers = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_PP_CENTERS)
                labels = labels.flatten().tolist()
            except Exception:
                labels = [0]*w
            trans = []
            last_label = labels[0]
            for i in range(1, w):
                if labels[i] != last_label:
                    trans.append(i)
                    last_label = labels[i]
            cuts = cand_cuts + line_xs + trans
            cuts = sorted(set([c for c in cuts if c >= 10 and c <= w-10]))
            merged = []
            last = -min_width
            for c in cuts:
                if c - last >= (min_width if not precise else int(min_width*0.8)):
                    merged.append(c)
                    last = c
            cuts = merged
            segments = []
            starts = [0] + cuts
            ends = cuts + [w]
            base = os.path.splitext(os.path.basename(path))[0]
            for i, (x0, x1) in enumerate(zip(starts, ends)):
                if (x1 - x0) < max(100, min_width // 2):
                    continue
                crop = im[0:h, x0:x1]
                name = f"{base}_col_{i+1}.png"
                p = os.path.join(out_dir, name)
                try:
                    cv2.imwrite(p, crop)
                    segments.append(p)
                except Exception:
                    continue
            return segments
        except Exception:
            pass
    try:
        img = Image.open(path).convert('RGB')
        w, h = img.size
        energy = _col_energy(img)
        cuts = _find_vcuts(energy, min_width)
        segments = []
        starts = [0] + cuts
        ends = cuts + [w]
        base = os.path.splitext(os.path.basename(path))[0]
        for i, (x0, x1) in enumerate(zip(starts, ends)):
            if (x1 - x0) < max(100, min_width // 2):
                continue
            crop = img.crop((x0, 0, x1, h))
            name = f"{base}_col_{i+1}.png"
            p = os.path.join(out_dir, name)
            try:
                crop.save(p)
                segments.append(p)
            except Exception:
                continue
        return segments
    except Exception:
        return []

def segment_image(path, out_dir, min_height=180, precise=False):
    if cv2 is not None and np is not None:
        try:
            im = cv2.imread(path)
            if im is None:
                raise RuntimeError('cv2 failed to read')
            h, w = im.shape[:2]
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (5, 5), 0)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            abs_y = np.abs(sobely)
            row_energy = abs_y.sum(axis=1)
            row_energy = row_energy / (row_energy.max() + 1e-9)
            kernel = np.ones((15,), dtype=np.float64) / 15.0
            smooth = np.convolve(row_energy, kernel, mode='same')
            mu = smooth.mean(); sigma = smooth.std()
            thr = mu + (1.2 if precise else 1.5) * sigma
            cand_cuts = [i for i, e in enumerate(smooth) if e > thr]
            edges = cv2.Canny(gray, 50, 150)
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=(90 if precise else 120), minLineLength=int(0.55*w), maxLineGap=20)
            line_ys = []
            if lines is not None:
                for l in lines[:,0]:
                    x1,y1,x2,y2 = l
                    if abs(y1 - y2) <= 3:
                        line_ys.append(int((y1 + y2) // 2))
            hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
            avg_rows = hsv.mean(axis=1)
            Z = avg_rows.astype(np.float32)
            K = 3 if precise else 2
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.2)
            try:
                ret, labels, centers = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_PP_CENTERS)
                labels = labels.flatten().tolist()
            except Exception:
                labels = [0]*h
            trans = []
            last_label = labels[0]
            for i in range(1, h):
                if labels[i] != last_label:
                    trans.append(i)
                    last_label = labels[i]
            cuts = cand_cuts + line_ys + trans
            cuts = sorted(set([c for c in cuts if c >= 10 and c <= h-10]))
            merged = []
            last = -min_height
            for c in cuts:
                if c - last >= (min_height if not precise else int(min_height*0.8)):
                    merged.append(c)
                    last = c
            cuts = merged
            segments = []
            starts = [0] + cuts
            ends = cuts + [h]
            base = os.path.splitext(os.path.basename(path))[0]
            for i, (y0, y1) in enumerate(zip(starts, ends)):
                if (y1 - y0) < max(120, min_height // 2):
                    continue
                crop = im[y0:y1, 0:w]
                name = f"{base}_seg_{i+1}.png"
                p = os.path.join(out_dir, name)
                try:
                    cv2.imwrite(p, crop)
                    segments.append(p)
                except Exception:
                    continue
            return segments
        except Exception:
            pass
    try:
        img = Image.open(path).convert('RGB')
        w, h = img.size
        energy = _row_energy(img)
        cuts = _find_cuts(energy, min_height)
        segments = []
        starts = [0] + cuts
        ends = cuts + [h]
        for i, (y0, y1) in enumerate(zip(starts, ends)):
            if (y1 - y0) < max(120, min_height // 2):
                continue
            crop = img.crop((0, y0, w, y1))
            base = os.path.splitext(os.path.basename(path))[0]
            name = f"{base}_seg_{i+1}.png"
            p = os.path.join(out_dir, name)
            try:
                crop.save(p)
                segments.append(p)
            except Exception:
                continue
        return segments
    except Exception:
        return []