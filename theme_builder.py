"""
Módulo mejorado para construcción de temas WordPress FSE
Integra mejor el plan, DNA y análisis visual con Qwen2-VL
"""
import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Importar funciones de bloques
try:
    from blocks_builder import setup_css_framework, create_custom_blocks
except ImportError:
    def setup_css_framework(theme_dir: str, framework: str):
        pass
    def create_custom_blocks(theme_dir: str, css_framework: str, plan: Dict):
        pass

def generate_style_css(
    theme_dir: str, 
    dna: Optional[Dict] = None, 
    theme_name: str = "Img2HTML AI Theme", 
    theme_description: str = "Tema de bloques generado y refinado con IA desde imágenes",
    theme_version: str = "1.0.0",
    theme_author: str = "",
    theme_uri: str = "",
    theme_textdomain: str = "",
    theme_tags: str = "",
    theme_license: str = "GPLv2 or later"
) -> str:
    """
    Genera un style.css completo para el tema WordPress con todos los metadatos.
    """
    palette = []
    if isinstance(dna, dict):
        palette = dna.get('palette', [])
    
    # Extraer colores
    bg_color = "#ffffff"
    text_color = "#111111"
    primary_color = "#3b82f6"
    secondary_color = "#64748b"
    
    for p in palette:
        slug = p.get('slug', '')
        color = p.get('color', '')
        if slug == 'background':
            bg_color = color
        elif slug == 'text':
            text_color = color
        elif slug == 'primary':
            primary_color = color
        elif slug == 'secondary':
            secondary_color = color
    
    # Generar textdomain desde slug si no se proporciona
    if not theme_textdomain:
        import re
        theme_textdomain = re.sub(r'[^a-z0-9-]', '', theme_name.lower().replace(' ', '-'))
        if not theme_textdomain:
            theme_textdomain = 'img2html'
    
    # Tags por defecto si no se proporcionan
    default_tags = "full-site-editing, block-theme, custom-colors, custom-menu, editor-style, featured-images, threaded-comments, translation-ready"
    if theme_tags:
        tags = theme_tags
    else:
        tags = default_tags
    
    # Autor por defecto
    author = theme_author if theme_author else "img2html"
    
    # License URI
    license_uri = ""
    if theme_license == "GPLv2 or later":
        license_uri = "http://www.gnu.org/licenses/gpl-2.0.html"
    elif theme_license == "GPLv3 or later":
        license_uri = "http://www.gnu.org/licenses/gpl-3.0.html"
    elif theme_license == "MIT":
        license_uri = "https://opensource.org/licenses/MIT"
    
    # Construir header del style.css
    header_lines = [
        f"Theme Name: {theme_name}",
        f"Version: {theme_version}",
        f"Author: {author}",
        f"Description: {theme_description}",
        "Requires at least: 6.7",
        "Tested up to: 6.7",
        "Requires PHP: 8.0",
        f"License: {theme_license}",
    ]
    
    if license_uri:
        header_lines.append(f"License URI: {license_uri}")
    
    if theme_uri:
        header_lines.append(f"Theme URI: {theme_uri}")
    
    header_lines.append(f"Text Domain: {theme_textdomain}")
    header_lines.append(f"Tags: {tags}")
    
    header = "/*\n" + "\n".join(header_lines) + "\n*/\n"
    
    style_css = f"""{header}

:root {{
    --wp--preset--color--background: {bg_color};
    --wp--preset--color--text: {text_color};
    --wp--preset--color--primary: {primary_color};
    --wp--preset--color--secondary: {secondary_color};
}}

/* Estilos base del tema */
* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
    background-color: var(--wp--preset--color--background);
    color: var(--wp--preset--color--text);
    line-height: 1.6;
}}

/* Mejoras de accesibilidad */
:focus-visible {{
    outline: 2px solid var(--wp--preset--color--primary);
    outline-offset: 2px;
}}

/* Responsive images */
img {{
    max-width: 100%;
    height: auto;
}}

/* Mejoras de tipografía */
h1, h2, h3, h4, h5, h6 {{
    line-height: 1.2;
    margin-top: 0;
}}

p {{
    margin-top: 0;
}}
"""
    return style_css

def enhance_theme_with_plan(theme_dir: str, plan: Dict, dna: Optional[Dict] = None):
    """
    Enriquece el tema con información del plan y DNA.
    Genera patterns personalizados basados en las secciones detectadas.
    """
    try:
        patterns_dir = os.path.join(theme_dir, 'patterns')
        os.makedirs(patterns_dir, exist_ok=True)
        
        sections = plan.get('sections', [])
        for idx, section in enumerate(sections):
            label = section.get('label', f'Sección {idx + 1}')
            slug = section.get('slug', f'section-{idx + 1}')
            pattern_type = section.get('pattern', '').lower()

            # Enriquecer con variantes de imagen si existen
            imgs = section.get('images', [])
            if imgs:
                first = imgs[0]
                if isinstance(first, dict):
                    section.setdefault('imageUrl', first.get('url') or first.get('original', ''))
                    section.setdefault('imageWebp', first.get('webp', ''))
                    section.setdefault('imageThumb', first.get('thumb', ''))
            
            # Enriquecer cards internas si existen
            cards = section.get('cards', [])
            new_cards = []
            for card in cards:
                if isinstance(card, dict):
                    img = card.get('image') or card.get('imageUrl')
                    if isinstance(img, dict):
                        card['imageUrl'] = img.get('url') or img.get('original', '')
                        card['imageWebp'] = img.get('webp', '')
                        card['imageThumb'] = img.get('thumb', '')
                    new_cards.append(card)
            if new_cards:
                section['cards'] = new_cards

            # Enriquecer slides si existen (para slider)
            slides = section.get('slides', [])
            new_slides = []
            for slide in slides:
                if isinstance(slide, dict):
                    img = slide.get('image') or slide.get('imageUrl')
                    if isinstance(img, dict):
                        slide['imageUrl'] = img.get('url') or img.get('original', '')
                        slide['imageWebp'] = img.get('webp', '')
                        slide['imageThumb'] = img.get('thumb', '')
                    # Textos/CTA por slide
                    if 'title' not in slide and section.get('title'):
                        slide['title'] = section.get('title')
                    if 'subtitle' not in slide and section.get('subtitle'):
                        slide['subtitle'] = section.get('subtitle')
                    if 'buttonText' not in slide and section.get('button_text'):
                        slide['buttonText'] = section.get('button_text')
                    if 'buttonUrl' not in slide and section.get('button_url'):
                        slide['buttonUrl'] = section.get('button_url')
                    new_slides.append(slide)
            if new_slides:
                section['slides'] = new_slides
            
            # Generar pattern basado en el tipo
            pattern_content = generate_pattern_from_section(section, dna)
            
            pattern_file = os.path.join(patterns_dir, f'{slug}.html')
            with open(pattern_file, 'w', encoding='utf-8') as f:
                f.write(pattern_content)
        
        # Actualizar patterns.json
        update_patterns_json(theme_dir, sections)
        
    except Exception as e:
        print(f"Error en enhance_theme_with_plan: {e}")

def generate_pattern_from_section(section: Dict, dna: Optional[Dict] = None) -> str:
    """
    Genera un pattern HTML de WordPress FSE basado en una sección.
    """
    label = section.get('label', 'Sección')
    pattern_type = section.get('pattern', '').lower()
    rows = section.get('layout_rows', [])
    # Si no hay layout_rows, intentar derivar de columns/ratios en section
    if not rows and section.get('columns'):
        cols = max(1, min(4, int(section.get('columns', 2))))
        ratios = section.get('ratios_percent', []) or [int(100/cols)] * cols
        rows = [{
            'columns': ['col'] * cols,
            'ratios_percent': ratios
        }]

    # Textos y CTA (si existen en el plan)
    title = section.get('title', label)
    subtitle = section.get('subtitle', section.get('description', ''))
    button_text = section.get('button_text', section.get('cta_text', ''))
    button_url = section.get('button_url', section.get('cta_url', '#'))
    show_button = bool(button_text)
    
    palette = []
    if isinstance(dna, dict):
        palette = dna.get('palette', [])
    
    slug_to_hex = {}
    for p in palette:
        s = p.get('slug')
        c = p.get('color')
        if s and c:
            slug_to_hex[s] = c
    
    blocks = []
    
    # Determinar si es hero
    is_hero = 'hero' in pattern_type or 'banner' in pattern_type

    # Capturar imágenes optimizadas si existen
    image_url = section.get('imageUrl', '')
    image_webp = section.get('imageWebp', '')
    image_thumb = section.get('imageThumb', '')
    
    if is_hero:
        overlay_color = 'primary'
        if slug_to_hex.get('primary'):
            # Calcular luminancia
            try:
                hex_color = slug_to_hex['primary'].lstrip('#')
                r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                lum = 0.2126 * (r/255.0) + 0.7152 * (g/255.0) + 0.0722 * (b/255.0)
                is_dark = lum < 0.5
            except Exception:
                is_dark = False
            if image_url:
                blocks.append('<!-- wp:group {"align":"full"} -->')
                blocks.append('<div class="wp-block-group alignfull">')
                blocks.append('<!-- wp:img2html/hero ')
                hero_attrs = {
                    "imageUrl": image_url,
                    "imageWebp": image_webp,
                    "imageThumb": image_thumb,
                    "showOverlay": True,
                    "title": title,
                    "subtitle": subtitle,
                    "buttonText": button_text,
                    "buttonUrl": button_url,
                    "showButton": show_button
                }
                import json as _json
                blocks.append(_json.dumps(hero_attrs, ensure_ascii=False))
                blocks.append(' /-->')
                blocks.append('</div>')
                blocks.append('<!-- /wp:group -->')
            else:
                blocks.append(f'<!-- wp:cover {{"dimRatio":20,"overlayColor":"{overlay_color}","isDark":{str(is_dark).lower()}}} -->')
                blocks.append('<div class="wp-block-cover">')
                blocks.append(f'<span aria-hidden="true" class="wp-block-cover__background has-{overlay_color}-background-color has-background-dim"></span>')
                blocks.append('<div class="wp-block-cover__inner-container">')
                blocks.append(f'<!-- wp:heading {{"textAlign":"center","level":1}} -->')
                blocks.append(f'<h1 class="has-text-align-center">{label}</h1>')
                blocks.append('<!-- /wp:heading -->')
                blocks.append('<!-- wp:paragraph {"align":"center"} -->')
                blocks.append('<p class="has-text-align-center">Descripción de la sección</p>')
                blocks.append('<!-- /wp:paragraph -->')
                blocks.append('</div>')
                blocks.append('</div>')
                blocks.append('<!-- /wp:cover -->')
    else:
        # Sección normal con grupo
        blocks.append('<!-- wp:group {"layout":{"type":"constrained"}} -->')
        blocks.append('<div class="wp-block-group">')
        blocks.append(f'<!-- wp:heading {{"level":2}} -->')
        blocks.append(f'<h2>{title}</h2>')
        blocks.append('<!-- /wp:heading -->')
        if subtitle:
            blocks.append('<!-- wp:paragraph -->')
            blocks.append(f'<p>{subtitle}</p>')
            blocks.append('<!-- /wp:paragraph -->')
        if show_button and button_text:
            blocks.append(f'<!-- wp:button {{"url":"{button_url}"}} -->')
            blocks.append(f'<div class="wp-block-button"><a class="wp-block-button__link">{button_text}</a></div>')
            blocks.append('<!-- /wp:button -->')
        
        # Agregar columnas si hay layout_rows
        for row in rows:
            cols = row.get('columns', [])
            ratios = row.get('ratios_percent', [])
            if cols:
                blocks.append('<!-- wp:columns {"align":"wide"} -->')
                blocks.append('<div class="wp-block-columns alignwide">')
                for i, _ in enumerate(cols):
                    pct = f"{int(ratios[i])}%" if i < len(ratios) and ratios[i] else "50%"
                    blocks.append(f'<!-- wp:column {{"width":"{pct}"}} -->')
                    blocks.append(f'<div class="wp-block-column" style="flex-basis:{pct}">')
                    blocks.append('<!-- wp:img2html/section /-->')
                    blocks.append('</div>')
                    blocks.append('<!-- /wp:column -->')
                blocks.append('</div>')
                blocks.append('<!-- /wp:columns -->')
        
        blocks.append('</div>')
        blocks.append('<!-- /wp:group -->')
    
    return '\n'.join(blocks)

def update_patterns_json(theme_dir: str, sections: List[Dict]):
    """
    Actualiza el archivo patterns.json con los patterns generados.
    """
    try:
        patterns_json_path = os.path.join(theme_dir, 'patterns.json')
        patterns_data = {"$schema": "https://schemas.wp.org/trunk/theme.json"}
        
        patterns_list = []
        for section in sections:
            slug = section.get('slug', '')
            label = section.get('label', '')
            if slug:
                patterns_list.append(f"img2html/{slug}")
        
        patterns_data['patterns'] = patterns_list
        
        with open(patterns_json_path, 'w', encoding='utf-8') as f:
            json.dump(patterns_data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def install_theme_to_wordpress(theme_dir: str, wordpress_dir: str, theme_slug: str = None):
    """
    Copia el tema generado a la carpeta de temas de WordPress.
    """
    try:
        wp_themes_dir = os.path.join(wordpress_dir, 'wp-content', 'themes')
        
        if not os.path.isdir(wp_themes_dir):
            print(f"Error: No se encontró la carpeta de temas en {wp_themes_dir}")
            return False
        
        # Determinar el nombre del tema
        if not theme_slug:
            # Leer el nombre del tema desde style.css
            style_css_path = os.path.join(theme_dir, 'style.css')
            if os.path.isfile(style_css_path):
                with open(style_css_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for line in content.split('\n'):
                        if line.startswith('Theme Name:'):
                            theme_name = line.split(':', 1)[1].strip()
                            theme_slug = theme_name.lower().replace(' ', '-').replace('_', '-')
                            break
        
        if not theme_slug:
            theme_slug = 'img2html-theme'
        
        target_dir = os.path.join(wp_themes_dir, theme_slug)
        
        # Eliminar tema existente si existe
        if os.path.isdir(target_dir):
            shutil.rmtree(target_dir)
        
        # Copiar tema
        shutil.copytree(theme_dir, target_dir)
        
        print(f"Tema instalado exitosamente en: {target_dir}")
        return True
        
    except Exception as e:
        print(f"Error al instalar el tema: {e}")
        return False

def ensure_theme_structure(theme_dir: str):
    """
    Asegura que el tema tenga toda la estructura necesaria.
    """
    required_dirs = [
        'templates',
        'parts',
        'patterns',
        'php',
        'assets'
    ]
    
    for dir_name in required_dirs:
        dir_path = os.path.join(theme_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)
    
    # Asegurar archivos básicos
    theme_name = "Img2HTML AI Theme"
    
    # Leer style.css existente o generar nuevo
    style_css_path = os.path.join(theme_dir, 'style.css')
    if os.path.isfile(style_css_path):
        # Leer nombre del tema desde style.css
        try:
            with open(style_css_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('Theme Name:'):
                        theme_name = line.split(':', 1)[1].strip()
                        break
        except Exception:
            pass
    else:
        style_css_content = generate_style_css(theme_dir, None, theme_name)
        with open(style_css_path, 'w', encoding='utf-8') as f:
            f.write(style_css_content)
    
    # functions.php mejorado
    functions_php = """<?php
/**
 * Functions and definitions
 * 
 * @package img2html
 */

// Cargar archivos PHP adicionales
$dir = get_theme_file_path('php');
if (is_dir($dir)){
  foreach (glob($dir.'/*.php') as $file){
    require_once $file;
  }
}

// Registrar bloques personalizados
function img2html_register_blocks() {
    $blocks = [
        'slider',
        'hero',
        'section',
        'cards',
        'gallery',
        'text-image',
        'sidebar',
        'search-extended',
        'pagination',
        'header',
        'footer',
        'form',
        'menu'
    ];
    
    foreach ($blocks as $block) {
        $block_path = get_template_directory() . '/blocks/' . $block;
        if (file_exists($block_path . '/block.json')) {
            register_block_type($block_path);
        }
    }
}
add_action('init', 'img2html_register_blocks');

// Registrar Custom Post Types opcionales
function img2html_register_cpts() {
    $cpts = [
        'portfolio' => 'Portfolio',
        'testimonial' => 'Testimonio',
        'service' => 'Servicio',
    ];
    foreach ($cpts as $slug => $label) {
        if (!post_type_exists($slug)) {
            register_post_type($slug, [
                'label' => $label,
                'public' => true,
                'show_in_rest' => true,
                'has_archive' => true,
                'supports' => ['title','editor','thumbnail','excerpt'],
                'rewrite' => ['slug' => $slug],
            ]);
        }
    }
}
add_action('init', 'img2html_register_cpts');

// Registrar patterns del tema
function img2html_register_patterns() {
    register_block_pattern_category('img2html', array('label' => 'Img2HTML'));
    
    $patterns_dir = get_theme_file_path('patterns');
    if (is_dir($patterns_dir)) {
        $pattern_files = glob($patterns_dir . '/*.html');
        foreach ($pattern_files as $file) {
            $slug = basename($file, '.html');
            $content = file_get_contents($file);
            if ($content) {
                register_block_pattern(
                    'img2html/' . $slug,
                    array(
                        'title' => ucwords(str_replace('-', ' ', $slug)),
                        'description' => 'Patrón generado desde imágenes',
                        'content' => $content,
                        'categories' => array('img2html'),
                    )
                );
            }
        }
    }
}
add_action('init', 'img2html_register_patterns');
"""
    
    required_files = {
        'functions.php': functions_php,
        'index.php': """<?php
/**
 * Silence is golden.
 */
""",
    }
    
    for filename, content in required_files.items():
        file_path = os.path.join(theme_dir, filename)
        # Siempre actualizar functions.php con la versión mejorada
        if filename == 'functions.php':
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        elif not os.path.isfile(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

def build_complete_theme(theme_dir: str, plan: Dict, dna: Optional[Dict] = None, images: List[str] = None, theme_name: str = None, theme_description: str = None, theme_slug: str = None, css_framework: str = 'none'):
    """
    Construye un tema completo de WordPress FSE desde el plan y DNA.
    """
    # Asegurar estructura
    ensure_theme_structure(theme_dir)
    
    # Usar nombre del tema proporcionado o del plan
    if not theme_name:
        theme_name = plan.get('title', 'Img2HTML AI Theme')
    if not theme_description:
        theme_description = 'Tema de bloques generado y refinado con IA desde imágenes'
    
    # Generar style.css
    style_css = generate_style_css(theme_dir, dna, theme_name, theme_description)
    style_path = os.path.join(theme_dir, 'style.css')
    with open(style_path, 'w', encoding='utf-8') as f:
        f.write(style_css)
    
    # Generar theme.json avanzado y completo
    generate_advanced_theme_json(theme_dir, dna, plan, theme_slug)

    # Asegurar template parts básicos usando bloques globales
    ensure_template_parts(theme_dir)

    # Templates FSE esenciales y biblioteca de patterns
    ensure_fse_templates(theme_dir, plan)
    ensure_pattern_library(theme_dir)
    # Generar patrones globales (Synced Patterns) y reutilizables
    ensure_global_patterns(theme_dir, theme_slug, plan, dna)

    # Generar archivo php para CPT y WooCommerce opcional
    ensure_cpt_php(theme_dir, plan)
    
    # Generar documentación automática del tema
    try:
        generate_theme_documentation(theme_dir, theme_name, theme_description, theme_slug, plan, dna)
    except Exception as e:
        print(f"Advertencia: Error al generar documentación: {e}")
    
    # Configurar pipeline de optimización de rendimiento
    try:
        from build_optimizer import setup_build_pipeline
        from blocks_builder import get_bem_prefix
        bem_prefix = get_bem_prefix(theme_slug)
        setup_build_pipeline(theme_dir, css_framework, bem_prefix)
    except Exception as e:
        print(f"Advertencia: Error al configurar optimizaciones: {e}")
        import traceback
        traceback.print_exc()
    
    # Configurar sistema de gestión de versiones
    try:
        from version_manager import setup_version_management
        initial_changes = [
            'Tema generado automáticamente desde imágenes',
            'Estructura Atomic Design implementada',
            'Sistema de bloques personalizados completo',
            'Optimizaciones de rendimiento configuradas'
        ]
        setup_version_management(theme_dir, theme_slug, initial_changes)
    except Exception as e:
        print(f"Advertencia: Error al configurar versiones: {e}")
        import traceback
        traceback.print_exc()

    # Optimizar imágenes de entrada (WebP y tamaños)
    try:
        assets_img = os.path.join(theme_dir, 'assets', 'img')
        img_map = optimize_images(images or [], assets_img)
        # Enriquecer plan con rutas optimizadas si hay coincidencias
        if isinstance(plan, dict) and img_map:
            for section in plan.get('sections', []):
                new_imgs = []
                for img in section.get('images', []):
                    entry = img_map.get(img)
                    if entry:
                        new_imgs.append({
                            "original": img,
                            "thumb": entry.get('thumb', {}).get('jpg') or entry.get('thumb', {}).get('webp', ''),
                            "webp": entry.get('large', {}).get('webp') or entry.get('medium', {}).get('webp') or '',
                            "url": entry.get('large', {}).get('jpg') or img,
                        })
                    else:
                        new_imgs.append(img)
                if new_imgs:
                    section['images'] = new_imgs
    except Exception as e:
        print(f"Error al optimizar imágenes: {e}")

    # Mejorar tema con plan (después de enriquecer imágenes)
    enhance_theme_with_plan(theme_dir, plan, dna)
    
    print(f"Tema construido exitosamente en: {theme_dir}")

def update_theme_json_colors(theme_dir: str, dna: Optional[Dict] = None):
    """
    Actualiza theme.json con la paleta de colores del DNA.
    """
    try:
        theme_json_path = os.path.join(theme_dir, 'theme.json')
        
        if os.path.isfile(theme_json_path):
            with open(theme_json_path, 'r', encoding='utf-8') as f:
                theme_data = json.load(f)
        else:
            theme_data = {
                "$schema": "https://schemas.wp.org/trunk/theme.json",
                "version": 3,
                "settings": {}
            }
        
        if isinstance(dna, dict):
            palette = dna.get('palette', [])
            if palette:
                settings = theme_data.setdefault('settings', {})
                color_settings = settings.setdefault('color', {})
                
                color_palette = []
                # Añadir acento si existe en el DNA
                accent = None
                for p in palette:
                    if p.get('slug') == 'accent':
                        accent = p
                        break
                for p in palette:
                    slug = p.get('slug', '')
                    color = p.get('color', '')
                    name = p.get('slug', '').title()
                    if slug and color:
                        color_palette.append({
                            "name": name,
                            "slug": slug,
                            "color": color
                        })
                if accent and accent not in color_palette:
                    color_palette.append({
                        "name": "Accent",
                        "slug": "accent",
                        "color": accent.get('color')
                    })
                
                if color_palette:
                    color_settings['palette'] = color_palette
        
        with open(theme_json_path, 'w', encoding='utf-8') as f:
            json.dump(theme_data, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Error al actualizar theme.json: {e}")


def apply_typography_and_spacing(theme_dir: str, dna: Optional[Dict] = None, design: Optional[Dict] = None):
    """
    Mapea tipografías, tamaños de texto, espaciados y radius al theme.json.
    Usa dna (palette, typography) y opcionalmente 'design' con pistas del plan.
    """
    try:
        theme_json_path = os.path.join(theme_dir, 'theme.json')
        if os.path.isfile(theme_json_path):
            with open(theme_json_path, 'r', encoding='utf-8') as f:
                theme_data = json.load(f)
        else:
            theme_data = {"$schema": "https://schemas.wp.org/trunk/theme.json", "version": 3, "settings": {}, "styles": {}}

        settings = theme_data.setdefault('settings', {})
        styles = theme_data.setdefault('styles', {})

        # Tipografías globales
        # Si hay fontFamily en dna, usarlo
        if isinstance(dna, dict):
            ff = dna.get('typography', {}).get('fontFamily')
            if ff:
                settings.setdefault('typography', {}).setdefault('fontFamilies', [])
                families = settings['typography']['fontFamilies']
                # evitar duplicados
                if not any(f.get('fontFamily') == ff for f in families):
                    families.append({"fontFamily": ff, "name": "Primary", "slug": "primary"})

        # Tamaños de fuente dinámicos desde DNA/plan
        font_sizes = settings.setdefault('typography', {}).setdefault('fontSizes', [])
        def ensure_size(slug, name, size):
            if not any(fs.get('slug') == slug for fs in font_sizes):
                font_sizes.append({"slug": slug, "name": name, "size": size})
        
        # Extraer escala tipográfica desde DNA o plan
        typo_scale = None
        if isinstance(dna, dict):
            typo_scale = dna.get('typography', {}).get('fontSizes')
        if not typo_scale and isinstance(design, dict):
            typo_scale = design.get('typography_hints', {}).get('fontSizes')
        
        if typo_scale and isinstance(typo_scale, list):
            # Usar escala detectada
            for item in typo_scale:
                if isinstance(item, dict) and 'slug' in item and 'size' in item:
                    ensure_size(item['slug'], item.get('name', item['slug'].title()), item['size'])
        else:
            # Fallback: escala base profesional
            ensure_size('xs', 'Extra Small', '0.75rem')
            ensure_size('sm', 'Small', '0.875rem')
            ensure_size('base', 'Base', '1rem')
            ensure_size('lg', 'Large', '1.125rem')
            ensure_size('xl', 'XLarge', '1.25rem')
            ensure_size('2xl', '2XLarge', '1.5rem')
            ensure_size('3xl', '3XLarge', '1.875rem')
            ensure_size('4xl', '4XLarge', '2.25rem')

        # Espaciados dinámicos desde DNA/plan
        spacing = settings.setdefault('spacing', {})
        spacing.setdefault('units', ['px', 'em', 'rem', '%', 'vh', 'vw'])
        preset_spacing = spacing.setdefault('spacingSizes', [])
        def ensure_space(slug, name, size):
            if not any(s.get('slug') == slug for s in preset_spacing):
                preset_spacing.append({"slug": slug, "name": name, "size": size})
        
        # Extraer espaciados desde DNA o plan
        spacing_hints = None
        if isinstance(dna, dict):
            spacing_hints = dna.get('spacing', {})
        if not spacing_hints and isinstance(design, dict):
            spacing_hints = design.get('spacing_hints', {})
        
        if spacing_hints and isinstance(spacing_hints, dict):
            # Mapear hints a valores concretos
            tight = spacing_hints.get('margins') == 'tight' or spacing_hints.get('padding') == 'tight'
            spacious = spacing_hints.get('margins') == 'spacious' or spacing_hints.get('padding') == 'spacious'
            base = 8 if tight else (16 if spacious else 12)
            ensure_space('xs', 'Extra Small', f'{base}px')
            ensure_space('sm', 'Small', f'{base * 1.5}px')
            ensure_space('md', 'Medium', f'{base * 2}px')
            ensure_space('lg', 'Large', f'{base * 3}px')
            ensure_space('xl', 'XLarge', f'{base * 4}px')
            ensure_space('2xl', '2XLarge', f'{base * 6}px')
        else:
            # Fallback: escala base profesional
            ensure_space('xs', 'Extra Small', '4px')
            ensure_space('sm', 'Small', '8px')
            ensure_space('md', 'Medium', '16px')
            ensure_space('lg', 'Large', '24px')
            ensure_space('xl', 'XLarge', '32px')
            ensure_space('2xl', '2XLarge', '48px')
            ensure_space('3xl', '3XLarge', '64px')

        # Border radius dinámico desde DNA/plan
        borders = settings.setdefault('border', {})
        radius = borders.setdefault('radius', {})
        
        # Extraer radius desde DNA o plan
        radius_hint = None
        if isinstance(dna, dict):
            radius_hint = dna.get('borderRadius')
        if not radius_hint and isinstance(design, dict):
            radius_hint = design.get('border_radius')
        
        if radius_hint:
            # Mapear hint a valores
            if isinstance(radius_hint, (int, float)):
                base_radius = f'{radius_hint}px'
            elif isinstance(radius_hint, str):
                base_radius = radius_hint
            else:
                base_radius = '8px'
            radius['small'] = f'calc({base_radius} * 0.5)'
            radius['medium'] = base_radius
            radius['large'] = f'calc({base_radius} * 2)'
        else:
            # Fallback: valores base
            radius['small'] = '4px'
            radius['medium'] = '8px'
            radius['large'] = '16px'
            radius['full'] = '9999px'

        # Styles globales (body)
        styles.setdefault('typography', {})
        body_typo = styles['typography']
        if 'fontFamily' not in body_typo:
            body_typo['fontFamily'] = 'var(--wp--preset--font-family--primary)' if settings.get('typography', {}).get('fontFamilies') else 'system-ui, sans-serif'

        # Presets base de botones y textos
        presets = theme_data.setdefault('styles', {}).setdefault('blocks', {})
        # Botón: usa color primario si existe
        btn_style = {
            "color": {
                "text": "var(--wp--preset--color--background)",
                "background": "var(--wp--preset--color--primary)"
            },
            "border": {
                "radius": "var(--wp--preset--border-radius--medium)"
            },
            "typography": {
                "fontFamily": "var(--wp--preset--font-family--primary)",
                "fontWeight": "600"
            },
            "spacing": {
                "padding": {
                    "top": "0.75rem",
                    "right": "1.25rem",
                    "bottom": "0.75rem",
                    "left": "1.25rem"
                }
            }
        }
        presets['core/button'] = btn_style

        # Heading y párrafo base
        presets['core/heading'] = {
            "typography": {
                "fontFamily": "var(--wp--preset--font-family--primary)"
            }
        }
        presets['core/paragraph'] = {
            "typography": {
                "fontFamily": "var(--wp--preset--font-family--primary)"
            }
        }

        # Layout responsivo base
        layout = settings.setdefault('layout', {})
        layout.setdefault('contentSize', '720px')
        layout.setdefault('wideSize', '1200px')

        with open(theme_json_path, 'w', encoding='utf-8') as f:
            json.dump(theme_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error aplicando tipografías/espaciados: {e}")


def _hex_to_rgb(hex_str: str) -> tuple:
    """Convierte color hex a RGB."""
    try:
        hex_str = hex_str.strip().lstrip('#')
        if len(hex_str) == 6:
            return (int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16))
    except Exception:
        pass
    return (59, 130, 246)  # Default blue

def _rgb_to_hex(rgb: tuple) -> str:
    """Convierte RGB a hex."""
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'

def _lighten_color(hex_str: str, factor: float = 0.2) -> str:
    """Aclara un color."""
    rgb = _hex_to_rgb(hex_str)
    r, g, b = rgb
    r = min(255, int(r + (255 - r) * factor))
    g = min(255, int(g + (255 - g) * factor))
    b = min(255, int(b + (255 - b) * factor))
    return _rgb_to_hex((r, g, b))

def _darken_color(hex_str: str, factor: float = 0.2) -> str:
    """Oscurece un color."""
    rgb = _hex_to_rgb(hex_str)
    r, g, b = rgb
    r = max(0, int(r * (1 - factor)))
    g = max(0, int(g * (1 - factor)))
    b = max(0, int(b * (1 - factor)))
    return _rgb_to_hex((r, g, b))

def _get_color_variations(base_color: str) -> Dict[str, str]:
    """Genera variaciones de un color (light, dark, accent)."""
    return {
        'base': base_color,
        'light': _lighten_color(base_color, 0.3),
        'lighter': _lighten_color(base_color, 0.5),
        'dark': _darken_color(base_color, 0.2),
        'darker': _darken_color(base_color, 0.4),
    }

def generate_advanced_theme_json(theme_dir: str, dna: Optional[Dict] = None, plan: Optional[Dict] = None, theme_slug: Optional[str] = None):
    """
    Genera un theme.json avanzado y completamente dinámico basado en el DNA y plan:
    - Paleta generada de la imagen con variaciones (primario/oscuro/acento/etc.)
    - Escalas tipográficas inteligentes
    - Presets de espaciado
    - Estilos de bloques core (core/heading, core/paragraph, etc.)
    - Layout global (anchos, contenedores)
    - Controles del editor habilitados/deshabilitados para mejor UX
    """
    try:
        theme_json_path = os.path.join(theme_dir, 'theme.json')
        
        # Cargar theme.json existente o crear uno nuevo
        if os.path.isfile(theme_json_path):
            with open(theme_json_path, 'r', encoding='utf-8') as f:
                theme_data = json.load(f)
        else:
            theme_data = {
                "$schema": "https://schemas.wp.org/trunk/theme.json",
                "version": 3,
                "settings": {},
                "styles": {},
                "customTemplates": {},
                "templateParts": {}
            }
        
        settings = theme_data.setdefault('settings', {})
        styles = theme_data.setdefault('styles', {})
        
        # ========================================
        # 1. SPACING SYSTEM AVANZADO
        # ========================================
        spacing = settings.setdefault('spacing', {})
        spacing['units'] = ['px', 'em', 'rem', '%', 'vh', 'vw', 'ch']
        
        # Sistema de espaciado basado en escala 8px
        spacing_sizes = spacing.setdefault('spacingSizes', [])
        spacing_sizes.clear()  # Limpiar para evitar duplicados
        
        base_spacing = 8  # Base de 8px
        spacing_scale = [
            ('0', 'None', '0'),
            ('xxs', 'XX Small', f'{base_spacing * 0.25}px'),  # 2px
            ('xs', 'Extra Small', f'{base_spacing * 0.5}px'),  # 4px
            ('sm', 'Small', f'{base_spacing}px'),  # 8px
            ('md', 'Medium', f'{base_spacing * 2}px'),  # 16px
            ('lg', 'Large', f'{base_spacing * 3}px'),  # 24px
            ('xl', 'Extra Large', f'{base_spacing * 4}px'),  # 32px
            ('2xl', '2X Large', f'{base_spacing * 6}px'),  # 48px
            ('3xl', '3X Large', f'{base_spacing * 8}px'),  # 64px
            ('4xl', '4X Large', f'{base_spacing * 12}px'),  # 96px
            ('5xl', '5X Large', f'{base_spacing * 16}px'),  # 128px
        ]
        
        for slug, name, size in spacing_scale:
            if not any(s.get('slug') == slug for s in spacing_sizes):
                spacing_sizes.append({"slug": slug, "name": name, "size": size})
        
        # ========================================
        # 2. PRESETS TIPOGRÁFICOS POR ROLES
        # ========================================
        typography = settings.setdefault('typography', {})
        
        # Font Families
        font_families = typography.setdefault('fontFamilies', [])
        if isinstance(dna, dict):
            ff = dna.get('typography', {}).get('fontFamily')
            if ff and not any(f.get('fontFamily') == ff for f in font_families):
                font_families.append({
                    "fontFamily": ff,
                    "name": "Primary",
                    "slug": "primary"
                })
        
        # Agregar fuente secundaria si no existe
        if not any(f.get('slug') == 'secondary' for f in font_families):
            font_families.append({
                "fontFamily": "Georgia, serif",
                "name": "Secondary",
                "slug": "secondary"
            })
        
        # Font Sizes - Escala tipográfica completa
        font_sizes = typography.setdefault('fontSizes', [])
        existing_sizes = {fs.get('slug') for fs in font_sizes}
        
        # Escala tipográfica modular (1.125 ratio)
        typo_scale = [
            ('xs', 'Extra Small', '0.75rem'),
            ('sm', 'Small', '0.875rem'),
            ('base', 'Base', '1rem'),
            ('lg', 'Large', '1.125rem'),
            ('xl', 'Extra Large', '1.25rem'),
            ('2xl', '2X Large', '1.5rem'),
            ('3xl', '3X Large', '1.875rem'),
            ('4xl', '4X Large', '2.25rem'),
            ('5xl', '5X Large', '3rem'),
            ('6xl', '6X Large', '3.75rem'),
        ]
        
        for slug, name, size in typo_scale:
            if slug not in existing_sizes:
                font_sizes.append({"slug": slug, "name": name, "size": size})
        
        # Font Weights
        font_weights = typography.setdefault('fontWeights', [])
        if not font_weights:
            font_weights.extend([
                {"slug": "light", "name": "Light", "weight": "300"},
                {"slug": "normal", "name": "Normal", "weight": "400"},
                {"slug": "medium", "name": "Medium", "weight": "500"},
                {"slug": "semibold", "name": "Semibold", "weight": "600"},
                {"slug": "bold", "name": "Bold", "weight": "700"},
                {"slug": "extrabold", "name": "Extrabold", "weight": "800"}
            ])
        
        # Line Heights
        line_heights = typography.setdefault('lineHeights', [])
        if not line_heights:
            line_heights.extend([
                {"slug": "none", "name": "None", "lineHeight": "1"},
                {"slug": "tight", "name": "Tight", "lineHeight": "1.25"},
                {"slug": "snug", "name": "Snug", "lineHeight": "1.375"},
                {"slug": "normal", "name": "Normal", "lineHeight": "1.5"},
                {"slug": "relaxed", "name": "Relaxed", "lineHeight": "1.625"},
                {"slug": "loose", "name": "Loose", "lineHeight": "2"}
            ])
        
        # ========================================
        # 3. PALETA EXTENDIDA DINÁMICA (CON VARIACIONES)
        # ========================================
        color_settings = settings.setdefault('color', {})
        
        # Paleta base desde DNA con variaciones automáticas
        palette = []
        primary_color = None
        secondary_color = None
        background_color = None
        text_color = None
        
        if isinstance(dna, dict):
            dna_palette = dna.get('palette', [])
            for p in dna_palette:
                slug = p.get('slug', '')
                color = p.get('color', '')
                if slug and color:
                    # Agregar color base
                    palette.append({
                        "name": slug.title(),
                        "slug": slug,
                        "color": color
                    })
                    
                    # Guardar referencias para variaciones
                    if slug == 'primary':
                        primary_color = color
                    elif slug == 'secondary':
                        secondary_color = color
                    elif slug == 'background':
                        background_color = color
                    elif slug == 'text':
                        text_color = color
        
        # Generar variaciones automáticas de colores principales
        if primary_color:
            primary_vars = _get_color_variations(primary_color)
            palette.extend([
                {"name": "Primary Light", "slug": "primary-light", "color": primary_vars['light']},
                {"name": "Primary Lighter", "slug": "primary-lighter", "color": primary_vars['lighter']},
                {"name": "Primary Dark", "slug": "primary-dark", "color": primary_vars['dark']},
                {"name": "Primary Darker", "slug": "primary-darker", "color": primary_vars['darker']},
            ])
        
        if secondary_color:
            secondary_vars = _get_color_variations(secondary_color)
            palette.extend([
                {"name": "Secondary Light", "slug": "secondary-light", "color": secondary_vars['light']},
                {"name": "Secondary Dark", "slug": "secondary-dark", "color": secondary_vars['dark']},
            ])
        
        # Colores semánticos inteligentes basados en la paleta
        semantic_colors = []
        
        # Success: verde o variación del primary si es verde
        if primary_color and primary_color.startswith('#') and _hex_to_rgb(primary_color)[1] > _hex_to_rgb(primary_color)[0]:
            # Si el primary es más verde que rojo, usar variación
            success_color = _lighten_color(primary_color, 0.1) if primary_color else "#10b981"
        else:
            success_color = "#10b981"
        
        # Error: rojo o variación si el primary es rojizo
        if primary_color and primary_color.startswith('#') and _hex_to_rgb(primary_color)[0] > _hex_to_rgb(primary_color)[1]:
            error_color = _darken_color(primary_color, 0.2) if primary_color else "#ef4444"
        else:
            error_color = "#ef4444"
        
        semantic_colors = [
            {"name": "Success", "slug": "success", "color": success_color},
            {"name": "Warning", "slug": "warning", "color": "#f59e0b"},
            {"name": "Error", "slug": "error", "color": error_color},
            {"name": "Info", "slug": "info", "color": primary_color or "#3b82f6"},
        ]
        
        # Colores de UI basados en background y text
        if background_color and text_color:
            # Border: versión más clara del text o más oscura del background
            border_rgb = _hex_to_rgb(background_color)
            text_rgb = _hex_to_rgb(text_color)
            # Promedio con ligera oscuridad
            border_color = _rgb_to_hex((
                max(0, min(255, (border_rgb[0] + text_rgb[0]) // 2 - 20)),
                max(0, min(255, (border_rgb[1] + text_rgb[1]) // 2 - 20)),
                max(0, min(255, (border_rgb[2] + text_rgb[2]) // 2 - 20))
            ))
            
            # Surface: versión ligeramente más oscura del background
            surface_color = _darken_color(background_color, 0.02) if background_color != "#ffffff" else "#f9fafb"
            
            # Muted: versión más clara del text
            muted_color = _lighten_color(text_color, 0.4) if text_color != "#111111" else "#6b7280"
            
            semantic_colors.extend([
                {"name": "Muted", "slug": "muted", "color": muted_color},
                {"name": "Border", "slug": "border", "color": border_color},
                {"name": "Surface", "slug": "surface", "color": surface_color},
            ])
        else:
            semantic_colors.extend([
                {"name": "Muted", "slug": "muted", "color": "#6b7280"},
                {"name": "Border", "slug": "border", "color": "#e5e7eb"},
                {"name": "Surface", "slug": "surface", "color": "#f9fafb"},
            ])
        
        # Agregar colores semánticos si no existen
        existing_slugs = {p.get('slug') for p in palette}
        for sem_color in semantic_colors:
            if sem_color['slug'] not in existing_slugs:
                palette.append(sem_color)
        
        if palette:
            color_settings['palette'] = palette
        
        # Gradientes dinámicos basados en la paleta
        gradients = color_settings.setdefault('gradients', [])
        if not gradients:
            gradient_list = []
            
            if primary_color and secondary_color:
                gradient_list.append({
                    "name": "Primary to Secondary",
                    "slug": "primary-to-secondary",
                    "gradient": f"linear-gradient(135deg, {primary_color} 0%, {secondary_color} 100%)"
                })
                gradient_list.append({
                    "name": "Primary Light to Dark",
                    "slug": "primary-light-dark",
                    "gradient": f"linear-gradient(180deg, {_lighten_color(primary_color, 0.3)} 0%, {_darken_color(primary_color, 0.2)} 100%)"
                })
            
            if text_color and background_color:
                gradient_list.append({
                    "name": "Text to Background",
                    "slug": "text-to-background",
                    "gradient": f"linear-gradient(180deg, {text_color} 0%, {background_color} 100%)"
                })
            
            # Gradiente oscuro universal
            gradient_list.append({
                "name": "Dark Overlay",
                "slug": "dark-overlay",
                "gradient": "linear-gradient(180deg, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0) 100%)"
            })
            
            # Gradiente claro universal
            gradient_list.append({
                "name": "Light Overlay",
                "slug": "light-overlay",
                "gradient": "linear-gradient(180deg, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0) 100%)"
            })
            
            gradients.extend(gradient_list)
        
        # ========================================
        # 4. LAYOUT GLOBAL
        # ========================================
        layout = settings.setdefault('layout', {})
        layout.update({
            "contentSize": "720px",
            "wideSize": "1200px",
            "padding": {
                "left": "var(--wp--preset--spacing--md)",
                "right": "var(--wp--preset--spacing--md)"
            }
        })
        
        # ========================================
        # 5. CUSTOM TEMPLATES
        # ========================================
        custom_templates = theme_data.setdefault('customTemplates', {})
        if not custom_templates:
            custom_templates.update({
                "page-full-width": {
                    "title": "Full Width",
                    "postTypes": ["page"]
                },
                "page-with-sidebar": {
                    "title": "Page with Sidebar",
                    "postTypes": ["page"]
                },
                "page-landing": {
                    "title": "Landing Page",
                    "postTypes": ["page"]
                }
            })
        
        # ========================================
        # 6. BLOCK-LEVEL SETTINGS
        # ========================================
        blocks = settings.setdefault('blocks', {})
        
        # core/group
        blocks.setdefault('core/group', {
            "spacing": {
                "padding": True,
                "margin": True
            },
            "layout": {
                "allowSwitching": False,
                "allowInheriting": True,
                "default": {
                    "type": "constrained"
                }
            },
            "color": {
                "background": True,
                "text": True,
                "gradients": True
            },
            "border": {
                "color": True,
                "radius": True,
                "style": True,
                "width": True
            }
        })
        
        # core/heading - Limitado para mejor UX
        blocks.setdefault('core/heading', {
            "typography": {
                "fontSize": True,  # Solo tamaños predefinidos
                "fontFamily": False,  # Usar familia global del tema
                "fontWeight": True,  # Solo pesos permitidos
                "fontStyle": False,  # Deshabilitado para simplificar
                "lineHeight": True,
                "textTransform": False,  # Deshabilitado para simplificar
                "letterSpacing": False,  # Deshabilitado para simplificar
                "textDecoration": False  # Deshabilitado para simplificar
            },
            "color": {
                "text": True,  # Solo colores de la paleta
                "background": False,  # Deshabilitado para simplificar
                "link": True,
                "gradients": False  # Deshabilitado para simplificar
            },
            "spacing": {
                "margin": True,
                "padding": False  # Deshabilitado para simplificar
            },
            "dimensions": {
                "minHeight": False
            }
        })
        
        # core/paragraph - Limitado para mejor UX
        blocks.setdefault('core/paragraph', {
            "typography": {
                "fontSize": True,  # Solo tamaños predefinidos
                "fontFamily": False,  # Usar familia global del tema
                "fontWeight": False,  # Usar peso normal por defecto
                "fontStyle": False,  # Deshabilitado
                "lineHeight": True,
                "textTransform": False,  # Deshabilitado
                "letterSpacing": False,  # Deshabilitado
                "textDecoration": False,  # Deshabilitado
                "dropCap": False  # Deshabilitado para simplificar
            },
            "color": {
                "text": True,  # Solo colores de la paleta
                "background": False,  # Deshabilitado para simplificar
                "link": True,
                "gradients": False  # Deshabilitado
                "link": True
            },
            "spacing": {
                "margin": True,
                "padding": False  # Deshabilitado para simplificar
            }
        })
        
        # core/button - Limitado para mejor UX
        blocks.setdefault('core/button', {
            "color": {
                "text": True,  # Solo colores de la paleta
                "background": True,  # Solo colores de la paleta
                "gradients": False  # Deshabilitado para simplificar (usar colores sólidos)
            },
            "typography": {
                "fontSize": True,  # Solo tamaños predefinidos
                "fontFamily": False,  # Usar familia global
                "fontWeight": True,  # Solo pesos permitidos
                "fontStyle": False,  # Deshabilitado
                "textTransform": False,  # Deshabilitado
                "letterSpacing": False  # Deshabilitado
            },
            "border": {
                "radius": True,  # Solo radios predefinidos
                "color": False,  # Deshabilitado
                "style": False,  # Deshabilitado
                "width": False  # Deshabilitado
            },
            "spacing": {
                "padding": True,
                "margin": True
            }
        })
        
        # core/columns - Limitado para mejor UX
        blocks.setdefault('core/columns', {
            "spacing": {
                "blockGap": True,  # Solo espaciados predefinidos
                "padding": True,
                "margin": True
            },
            "layout": {
                "allowSwitching": False,  # Deshabilitado para evitar cambios inesperados
                "allowInheriting": True
            },
            "align": ["wide", "full"],  # Solo estas alineaciones
            "color": False  # Deshabilitado (usar en columnas individuales)
        })
        
        # core/image - Limitado para mejor UX
        blocks.setdefault('core/image', {
            "border": {
                "color": False,  # Deshabilitado
                "radius": True,  # Solo radios predefinidos
                "style": False,  # Deshabilitado
                "width": False  # Deshabilitado
            },
            "spacing": {
                "margin": True,
                "padding": False  # Deshabilitado
            },
            "dimensions": {
                "aspectRatio": True,
                "minHeight": False  # Deshabilitado
            },
            "align": ["left", "center", "right", "wide", "full"],  # Todas las alineaciones permitidas
            "color": False  # Deshabilitado
        })
        
        # core/cover - Limitado para mejor UX
        blocks.setdefault('core/cover', {
            "color": {
                "text": True,  # Solo colores de la paleta
                "background": True,  # Solo colores de la paleta
                "gradients": False  # Deshabilitado para simplificar
            },
            "align": ["wide", "full"],  # Solo estas alineaciones
            "spacing": {
                "padding": True,
                "margin": False  # Deshabilitado
            },
            "spacing": {
                "padding": True,
                "margin": True
            },
            "dimensions": {
                "minHeight": True
            }
        })
        
        # core/list
        blocks.setdefault('core/list', {
            "typography": {
                "fontSize": True,
                "fontFamily": True,
                "fontWeight": True,
                "lineHeight": True
            },
            "color": {
                "text": True,
                "link": True
            },
            "spacing": {
                "margin": True,
                "padding": True
            }
        })
        
        # core/quote
        blocks.setdefault('core/quote', {
            "typography": {
                "fontSize": True,
                "fontFamily": True,
                "fontStyle": True,
                "lineHeight": True
            },
            "color": {
                "text": True,
                "background": True
            },
            "border": {
                "color": True,
                "style": True,
                "width": True
            },
            "spacing": {
                "margin": True,
                "padding": True
            }
        })
        
        # core/pullquote
        blocks.setdefault('core/pullquote', {
            "typography": {
                "fontSize": True,
                "fontFamily": True,
                "fontStyle": True,
                "lineHeight": True
            },
            "color": {
                "text": True,
                "background": True
            },
            "border": {
                "color": True,
                "style": True,
                "width": True
            }
        })
        
        # core/separator
        blocks.setdefault('core/separator', {
            "color": {
                "text": True
            },
            "spacing": {
                "margin": True
            }
        })
        
        # core/spacer
        blocks.setdefault('core/spacer', {
            "spacing": {
                "height": True
            }
        })
        
        # core/table
        blocks.setdefault('core/table', {
            "typography": {
                "fontSize": True,
                "fontFamily": True
            },
            "color": {
                "text": True,
                "background": True
            },
            "border": {
                "color": True,
                "style": True,
                "width": True
            },
            "spacing": {
                "margin": True,
                "padding": True
            }
        })
        
        # ========================================
        # 7. STYLES GLOBALES Y POR BLOQUE
        # ========================================
        # Estilos globales dinámicos basados en DNA
        styles.setdefault('typography', {})
        if 'fontFamily' not in styles['typography']:
            styles['typography']['fontFamily'] = 'var(--wp--preset--font-family--primary)'
        if 'fontSize' not in styles['typography']:
            styles['typography']['fontSize'] = 'var(--wp--preset--font-size--base)'
        if 'lineHeight' not in styles['typography']:
            styles['typography']['lineHeight'] = 'var(--wp--preset--line-height--normal)'
        
        # Colores globales desde DNA
        if background_color:
            styles.setdefault('color', {})['background'] = background_color
        if text_color:
            styles.setdefault('color', {})['text'] = text_color
        
        # Estilos por bloque
        block_styles = styles.setdefault('blocks', {})
        
        # core/button styles
        block_styles.setdefault('core/button', {
            "color": {
                "background": "var(--wp--preset--color--primary)",
                "text": "var(--wp--preset--color--background)"
            },
            "typography": {
                "fontFamily": "var(--wp--preset--font-family--primary)",
                "fontWeight": "600",
                "fontSize": "var(--wp--preset--font-size--base)"
            },
            "border": {
                "radius": "var(--wp--preset--border-radius--medium)"
            },
            "spacing": {
                "padding": {
                    "top": "var(--wp--preset--spacing--sm)",
                    "right": "var(--wp--preset--spacing--lg)",
                    "bottom": "var(--wp--preset--spacing--sm)",
                    "left": "var(--wp--preset--spacing--lg)"
                }
            }
        })
        
        # core/heading styles
        block_styles.setdefault('core/heading', {
            "typography": {
                "fontFamily": "var(--wp--preset--font-family--primary)",
                "fontWeight": "700"
            },
            "spacing": {
                "margin": {
                    "top": "0",
                    "bottom": "var(--wp--preset--spacing--md)"
                }
            }
        })
        
        # core/paragraph styles
        block_styles.setdefault('core/paragraph', {
            "typography": {
                "fontFamily": "var(--wp--preset--font-family--primary)",
                "lineHeight": "var(--wp--preset--line-height--normal)"
            },
            "spacing": {
                "margin": {
                    "top": "0",
                    "bottom": "var(--wp--preset--spacing--md)"
                }
            }
        })
        
        # ========================================
        # 8. BORDER RADIUS
        # ========================================
        border = settings.setdefault('border', {})
        radius = border.setdefault('radius', {})
        if not radius:
            radius.update({
                "small": "4px",
                "medium": "8px",
                "large": "12px",
                "xlarge": "16px",
                "full": "9999px"
            })
        
        # ========================================
        # GUARDAR theme.json
        # ========================================
        with open(theme_json_path, 'w', encoding='utf-8') as f:
            json.dump(theme_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ theme.json avanzado generado exitosamente")
        
    except Exception as e:
        print(f"Error al generar theme.json avanzado: {e}")
        import traceback
        traceback.print_exc()


def ensure_template_parts(theme_dir: str):
    """Crea parts/header.html, parts/footer.html y parts/sidebar.html usando bloques personalizados."""
    try:
        parts_dir = os.path.join(theme_dir, 'parts')
        os.makedirs(parts_dir, exist_ok=True)
        header_path = os.path.join(parts_dir, 'header.html')
        footer_path = os.path.join(parts_dir, 'footer.html')
        sidebar_path = os.path.join(parts_dir, 'sidebar.html')

        header_content = """<!-- wp:img2html/header /-->"""
        footer_content = """<!-- wp:img2html/footer /-->"""
        sidebar_content = """<!-- wp:img2html/sidebar /-->"""

        for path, content in (
            (header_path, header_content),
            (footer_path, footer_content),
            (sidebar_path, sidebar_content),
        ):
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
    except Exception as e:
        print(f"Error al crear template parts: {e}")


def ensure_fse_templates(theme_dir: str, plan: Optional[Dict] = None):
    """Genera plantillas FSE básicas y opcionales (CPT/Woo) si no existen."""
    try:
        tpl_dir = os.path.join(theme_dir, 'templates')
        os.makedirs(tpl_dir, exist_ok=True)

        base_templates = {
            'home.html': """<!-- wp:template-part {"slug":"header"} /-->
<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main>
<!-- wp:pattern {"slug":"img2html/hero"} /-->
<!-- wp:query {"query":{"perPage":6,"pages":0,"offset":0,"postType":"post","order":"desc","orderby":"date"}} -->
<div class="wp-block-query">
  <!-- wp:post-template -->
    <!-- wp:post-featured-image /-->
    <!-- wp:post-title {"isLink":true} /-->
    <!-- wp:post-excerpt /-->
  <!-- /wp:post-template -->
  <!-- wp:img2html/pagination /-->
</div>
<!-- /wp:query -->
</main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer"} /-->""",
            'index.html': """<!-- wp:template-part {"slug":"header"} /-->
<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main>
<!-- wp:query {"query":{"perPage":10,"pages":0,"offset":0,"postType":"post","order":"desc","orderby":"date"}} -->
<div class="wp-block-query">
  <!-- wp:post-template -->
    <!-- wp:post-title {"isLink":true} /-->
    <!-- wp:post-excerpt /-->
  <!-- /wp:post-template -->
  <!-- wp:img2html/pagination /-->
</div>
<!-- /wp:query -->
</main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer"} /-->""",
            'single.html': """<!-- wp:template-part {"slug":"header"} /-->
<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main>
  <!-- wp:post-title /-->
  <!-- wp:post-featured-image /-->
  <!-- wp:post-content /-->
  <!-- wp:img2html/pagination /-->
</main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer"} /-->""",
            'page.html': """<!-- wp:template-part {"slug":"header"} /-->
<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main>
  <!-- wp:post-title /-->
  <!-- wp:post-content /-->
</main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer"} /-->""",
            'archive.html': """<!-- wp:template-part {"slug":"header"} /-->
<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main>
  <!-- wp:query {"query":{"perPage":10,"pages":0,"offset":0,"postType":"post"}} -->
  <div class="wp-block-query">
    <!-- wp:post-template -->
      <!-- wp:post-title {"isLink":true} /-->
      <!-- wp:post-excerpt /-->
    <!-- /wp:post-template -->
    <!-- wp:img2html/pagination /-->
  </div>
  <!-- /wp:query -->
</main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer"} /-->""",
            'search.html': """<!-- wp:template-part {"slug":"header"} /-->
<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main>
  <!-- wp:img2html/search-extended /-->
  <!-- wp:query {"query":{"perPage":10,"pages":0,"offset":0,"postType":"any","search":""}} -->
  <div class="wp-block-query">
    <!-- wp:post-template -->
      <!-- wp:post-title {"isLink":true} /-->
      <!-- wp:post-excerpt /-->
    <!-- /wp:post-template -->
    <!-- wp:img2html/pagination /-->
  </div>
  <!-- /wp:query -->
</main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer"} /-->""",
            '404.html': """<!-- wp:template-part {"slug":"header"} /-->
<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main>
  <!-- wp:heading {"textAlign":"center","level":1} --><h1 class="has-text-align-center">404</h1><!-- /wp:heading -->
  <!-- wp:paragraph {"align":"center"} --><p class="has-text-align-center">La página no existe.</p><!-- /wp:paragraph -->
  <!-- wp:img2html/search-extended /-->
</main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer"} /-->""",
            'category.html': """<!-- wp:template-part {"slug":"header"} /-->
<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main>
  <!-- wp:query {"query":{"perPage":10,"pages":0,"offset":0,"postType":"post"}} -->
  <div class="wp-block-query">
    <!-- wp:post-template -->
      <!-- wp:post-title {"isLink":true} /-->
      <!-- wp:post-excerpt /-->
    <!-- /wp:post-template -->
    <!-- wp:img2html/pagination /-->
  </div>
  <!-- /wp:query -->
</main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer"} /-->"""
        }

        for name, content in base_templates.items():
            path = os.path.join(tpl_dir, name)
            if not os.path.isfile(path):
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)

        # Plantillas CPT opcionales (se escriben siempre; se usan si se registran los CPT)
        cpt_templates = {
            'single-portfolio.html': """<!-- wp:template-part {"slug":"header"} /-->
<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main>
  <!-- wp:post-title /-->
  <!-- wp:post-featured-image /-->
  <!-- wp:post-content /-->
</main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer"} /-->""",
            'archive-portfolio.html': """<!-- wp:template-part {"slug":"header"} /-->
<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main>
  <!-- wp:query {"query":{"perPage":9,"pages":0,"offset":0,"postType":"portfolio","order":"desc","orderby":"date"}} -->
  <div class="wp-block-query">
    <!-- wp:post-template -->
      <!-- wp:post-featured-image {"isLink":true} /-->
      <!-- wp:post-title {"isLink":true} /-->
    <!-- /wp:post-template -->
    <!-- wp:img2html/pagination /-->
  </div>
  <!-- /wp:query -->
</main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer"} /-->""",
            'single-testimonial.html': """<!-- wp:template-part {"slug":"header"} /-->
<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main>
  <!-- wp:post-title /-->
  <!-- wp:post-content /-->
</main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer"} /-->""",
            'archive-testimonial.html': """<!-- wp:template-part {"slug":"header"} /-->
<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main>
  <!-- wp:query {"query":{"perPage":9,"pages":0,"offset":0,"postType":"testimonial","order":"desc","orderby":"date"}} -->
  <div class="wp-block-query">
    <!-- wp:post-template -->
      <!-- wp:post-title {"isLink":true} /-->
      <!-- wp:post-excerpt /-->
    <!-- /wp:post-template -->
    <!-- wp:img2html/pagination /-->
  </div>
  <!-- /wp:query -->
</main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer"} /-->""",
            'single-service.html': """<!-- wp:template-part {"slug":"header"} /-->
<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main>
  <!-- wp:post-title /-->
  <!-- wp:post-content /-->
</main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer"} /-->""",
            'archive-service.html': """<!-- wp:template-part {"slug":"header"} /-->
<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main>
  <!-- wp:query {"query":{"perPage":9,"pages":0,"offset":0,"postType":"service","order":"desc","orderby":"date"}} -->
  <div class="wp-block-query">
    <!-- wp:post-template -->
      <!-- wp:post-title {"isLink":true} /-->
      <!-- wp:post-excerpt /-->
    <!-- /wp:post-template -->
    <!-- wp:img2html/pagination /-->
  </div>
  <!-- /wp:query -->
</main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer"} /-->"""
        }
        for name, content in cpt_templates.items():
            path = os.path.join(tpl_dir, name)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

        # Plantillas WooCommerce básicas (solo si el plan sugiere tienda/productos)
        has_shop = False
        if isinstance(plan, dict):
            for s in plan.get('sections', []):
                name = (s.get('name') or s.get('label') or '').lower()
                if any(k in name for k in ['shop', 'tienda', 'product', 'producto', 'store']):
                    has_shop = True
                    break
        woo_templates = {
            'archive-product.html': """<!-- wp:template-part {"slug":"header"} /-->
<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main>
  <!-- wp:woocommerce/product-collection {"query":{"perPage":12}} /-->
</main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer"} /-->""",
            'single-product.html': """<!-- wp:template-part {"slug":"header"} /-->
<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main>
  <!-- wp:woocommerce/product-image-gallery /-->
  <!-- wp:post-title /-->
  <!-- wp:woocommerce/product-price /-->
  <!-- wp:post-content /-->
  <!-- wp:woocommerce/product-button /-->
</main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer"} /-->""",
            'cart.html': """<!-- wp:template-part {"slug":"header"} /-->
<!-- wp:woocommerce/cart /-->
<!-- wp:template-part {"slug":"footer"} /-->""",
            'checkout.html': """<!-- wp:template-part {"slug":"header"} /-->
<!-- wp:woocommerce/checkout /-->
<!-- wp:template-part {"slug":"footer"} /-->"""
        }
        if has_shop:
            for name, content in woo_templates.items():
                path = os.path.join(tpl_dir, name)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
    except Exception as e:
        print(f"Error al crear templates FSE: {e}")


def ensure_pattern_library(theme_dir: str):
    """Crea una biblioteca mínima de patterns reutilizables."""
    try:
        patterns_dir = os.path.join(theme_dir, 'patterns')
        os.makedirs(patterns_dir, exist_ok=True)

        patterns = {
            'hero.html': """<!-- wp:cover {"dimRatio":30,"overlayColor":"primary","minHeight":420} -->
<div class="wp-block-cover"><span aria-hidden="true" class="wp-block-cover__background has-primary-background-color has-background-dim"></span><div class="wp-block-cover__inner-container">
<!-- wp:heading {"textAlign":"center","level":1} --><h1 class="has-text-align-center">Título Hero</h1><!-- /wp:heading -->
<!-- wp:paragraph {"align":"center"} --><p class="has-text-align-center">Subtítulo opcional</p><!-- /wp:paragraph -->
<!-- wp:buttons {"layout":{"type":"flex","justifyContent":"center"}} -->
<div class="wp-block-buttons"><!-- wp:button {"className":"is-style-fill"} --><div class="wp-block-button is-style-fill"><a class="wp-block-button__link">Llamada a la acción</a></div><!-- /wp:button --></div>
<!-- /wp:buttons -->
</div></div>
<!-- /wp:cover -->""",
            'services.html': """<!-- wp:group {"layout":{"type":"constrained"}} -->
<div class="wp-block-group"><!-- wp:heading {"textAlign":"center","level":2} --><h2 class="has-text-align-center">Servicios</h2><!-- /wp:heading -->
<!-- wp:columns {"align":"wide"} -->
<div class="wp-block-columns alignwide"><!-- wp:column --><div class="wp-block-column"><!-- wp:heading {"level":3} --><h3>Servicio 1</h3><!-- /wp:heading --><!-- wp:paragraph --><p>Descripción breve.</p><!-- /wp:paragraph --></div><!-- /wp:column --><!-- wp:column --><div class="wp-block-column"><!-- wp:heading {"level":3} --><h3>Servicio 2</h3><!-- /wp:heading --><!-- wp:paragraph --><p>Descripción breve.</p><!-- /wp:paragraph --></div><!-- /wp:column --><!-- wp:column --><div class="wp-block-column"><!-- wp:heading {"level":3} --><h3>Servicio 3</h3><!-- /wp:heading --><!-- wp:paragraph --><p>Descripción breve.</p><!-- /wp:paragraph --></div><!-- /wp:column --></div>
<!-- /wp:columns --></div>
<!-- /wp:group -->""",
            'portfolio.html': """<!-- wp:group {"layout":{"type":"constrained"}} -->
<div class="wp-block-group"><!-- wp:heading {"textAlign":"center","level":2} --><h2 class="has-text-align-center">Portfolio</h2><!-- /wp:heading -->
<!-- wp:query {"query":{"perPage":6,"pages":0,"offset":0,"postType":"post","order":"desc","orderby":"date"}} -->
<div class="wp-block-query"><!-- wp:post-template -->
<!-- wp:group {"layout":{"type":"constrained"}} -->
<div class="wp-block-group"><!-- wp:post-featured-image {"isLink":true} /--><!-- wp:post-title {"isLink":true} /--></div>
<!-- /wp:group -->
<!-- /wp:post-template -->
<!-- wp:img2html/pagination /-->
</div>
<!-- /wp:query --></div>
<!-- /wp:group -->""",
            'contact.html': """<!-- wp:group {"layout":{"type":"constrained"}} -->
<div class="wp-block-group"><!-- wp:heading {"textAlign":"center","level":2} --><h2 class="has-text-align-center">Contacto</h2><!-- /wp:heading -->
<!-- wp:paragraph {"align":"center"} --><p class="has-text-align-center">Déjanos tu mensaje</p><!-- /wp:paragraph -->
<!-- wp:img2html/text-image /-->
</div>
<!-- /wp:group -->""",
            'cta.html': """<!-- wp:group {"layout":{"type":"constrained","justifyContent":"center"}} -->
<div class="wp-block-group has-background" style="background-color:#111827;padding:32px;border-radius:12px">
<!-- wp:heading {"textAlign":"center","level":2,"textColor":"background"} --><h2 class="has-text-align-center has-background-color has-text-color">Listo para empezar</h2><!-- /wp:heading -->
<!-- wp:buttons {"layout":{"type":"flex","justifyContent":"center"}} -->
<div class="wp-block-buttons"><!-- wp:button {"backgroundColor":"primary","textColor":"background","className":"is-style-fill"} --><div class="wp-block-button is-style-fill"><a class="wp-block-button__link has-primary-background-color has-background-color has-text-color">Call to action</a></div><!-- /wp:button --></div>
<!-- /wp:buttons -->
</div>
<!-- /wp:group -->""",
            'testimonials.html': """<!-- wp:group {"layout":{"type":"constrained"}} -->
<div class="wp-block-group"><!-- wp:heading {"textAlign":"center","level":2} --><h2 class="has-text-align-center">Testimonios</h2><!-- /wp:heading -->
<!-- wp:columns {"align":"wide"} -->
<div class="wp-block-columns alignwide"><!-- wp:column --><div class="wp-block-column"><!-- wp:quote --><blockquote class="wp-block-quote"><p>Comentario de cliente.</p><cite>Cliente</cite></blockquote><!-- /wp:quote --></div><!-- /wp:column --><div class="wp-block-column"><!-- wp:quote --><blockquote class="wp-block-quote"><p>Otro testimonio.</p><cite>Cliente</cite></blockquote><!-- /wp:quote --></div><!-- /wp:column --></div>
<!-- /wp:columns --></div>
<!-- /wp:group -->""",
            'faq.html': """<!-- wp:group {"layout":{"type":"constrained"}} -->
<div class="wp-block-group"><!-- wp:heading {"textAlign":"center","level":2} --><h2 class="has-text-align-center">FAQ</h2><!-- /wp:heading -->
<!-- wp:details --><details><summary>Pregunta frecuente 1</summary><p>Respuesta breve.</p></details><!-- /wp:details -->
<!-- wp:details --><details><summary>Pregunta frecuente 2</summary><p>Respuesta breve.</p></details><!-- /wp:details -->
</div>
<!-- /wp:group -->"""
        }

        for name, content in patterns.items():
            path = os.path.join(patterns_dir, name)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

        # Actualizar patterns.json para incluirlos
        patterns_json = os.path.join(theme_dir, 'patterns.json')
        try:
            with open(patterns_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            data = {"$schema": "https://schemas.wp.org/trunk/theme.json"}
        existing = set(data.get('patterns', []))
        for name in patterns.keys():
            slug = f"img2html/{os.path.splitext(name)[0]}"
            existing.add(slug)
        # Incluir patterns especiales para CPT si se usan
        for slug in ["img2html/portfolio", "img2html/services", "img2html/testimonials", "img2html/contact"]:
            existing.add(slug)
        data['patterns'] = sorted(existing)
        with open(patterns_json, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    except Exception as e:
        print(f"Error al crear patterns: {e}")


def ensure_global_patterns(theme_dir: str, theme_slug: Optional[str] = None, plan: Optional[Dict] = None, dna: Optional[Dict] = None):
    """
    Genera patrones globales (Synced Patterns) y bloques reutilizables.
    Crea archivos .php en /patterns/ con metadata completa.
    También genera patterns_meta.json con información de cada patrón.
    """
    try:
        from blocks_builder import get_bem_prefix
        bem_prefix = get_bem_prefix(theme_slug)
        
        patterns_dir = os.path.join(theme_dir, 'patterns')
        os.makedirs(patterns_dir, exist_ok=True)
        
        # Patrones sincronizados (Synced Patterns) - se actualizan globalmente
        # Usar bloques personalizados del tema cuando estén disponibles
        synced_patterns = {
            f'{bem_prefix}-header-global.php': {
                'title': f'Header Global ({bem_prefix})',
                'description': 'Header sincronizado que se actualiza en todas las páginas. Usa el bloque personalizado del tema.',
                'categories': [f'{bem_prefix}-header', 'header'],
                'content': f"""<!-- wp:{bem_prefix}/organism-header {{"sticky":true,"transparent":false,"showButton":true,"buttonText":"Contáctanos"}} -->
<div class="wp-block-{bem_prefix}-organism-header {bem_prefix}-organism-header--sticky">
<!-- wp:site-logo {{"width":48}} /-->
<!-- wp:{bem_prefix}/organism-menu {{"menuStyle":"horizontal"}} /-->
<!-- wp:buttons {{"layout":{{"type":"flex","justifyContent":"right"}}}} -->
<div class="wp-block-buttons">
<!-- wp:button {{"backgroundColor":"primary","textColor":"background"}} -->
<div class="wp-block-button"><a class="wp-block-button__link has-primary-background-color has-background-color has-text-color wp-element-button">Contáctanos</a></div>
<!-- /wp:button -->
</div>
<!-- /wp:buttons -->
</div>
<!-- /wp:{bem_prefix}/organism-header -->""",
                'syncStatus': 'synced',
                'keywords': ['header', 'navigation', 'menu', 'global']
            },
            f'{bem_prefix}-footer-global.php': {
                'title': f'Footer Global ({bem_prefix})',
                'description': 'Footer sincronizado que se actualiza en todas las páginas. Usa el bloque personalizado del tema.',
                'categories': [f'{bem_prefix}-footer', 'footer'],
                'content': f"""<!-- wp:{bem_prefix}/organism-footer {{"columns":3,"showSocial":true,"darkBackground":true}} -->
<footer class="wp-block-{bem_prefix}-organism-footer {bem_prefix}-organism-footer--dark">
<!-- wp:columns {{"align":"wide"}} -->
<div class="wp-block-columns alignwide">
<!-- wp:column -->
<div class="wp-block-column">
<!-- wp:site-logo {{"width":48}} /-->
<!-- wp:paragraph -->
<p>© 2025. Todos los derechos reservados.</p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:column -->
<!-- wp:column -->
<div class="wp-block-column">
<!-- wp:heading {{"level":4}} -->
<h4>Enlaces</h4>
<!-- /wp:heading -->
<!-- wp:navigation {{"layout":{{"type":"flex","orientation":"vertical"}}}} /-->
</div>
<!-- /wp:column -->
<!-- wp:column -->
<div class="wp-block-column">
<!-- wp:heading {{"level":4}} -->
<h4>Redes Sociales</h4>
<!-- /wp:heading -->
<!-- wp:social-links /-->
</div>
<!-- /wp:column -->
</div>
<!-- /wp:columns -->
</footer>
<!-- /wp:group -->""",
                'syncStatus': 'synced'
            },
            f'{bem_prefix}-cta-primary.php': {
                'title': f'CTA Principal ({bem_prefix})',
                'description': 'Call to Action reutilizable usando el bloque CTA personalizado del tema',
                'categories': [f'{bem_prefix}-call-to-action', 'call-to-action'],
                'content': f"""<!-- wp:{bem_prefix}/organism-cta {{"title":"¿Listo para empezar?","description":"Únete a nosotros hoy mismo","primaryButtonText":"Comenzar ahora","secondaryButtonText":"Saber más","showSecondaryButton":true,"backgroundStyle":"primary","alignment":"center"}} -->
<div class="wp-block-{bem_prefix}-organism-cta {bem_prefix}-organism-cta--primary {bem_prefix}-organism-cta--align-center">
<div class="{bem_prefix}-organism-cta__content">
<h2 class="{bem_prefix}-organism-cta__title">¿Listo para empezar?</h2>
<p class="{bem_prefix}-organism-cta__description">Únete a nosotros hoy mismo</p>
<div class="{bem_prefix}-organism-cta__actions">
<a href="#" class="{bem_prefix}-organism-cta__button {bem_prefix}-organism-cta__button--primary">Comenzar ahora</a>
<a href="#" class="{bem_prefix}-organism-cta__button {bem_prefix}-organism-cta__button--secondary">Saber más</a>
</div>
</div>
</div>
<!-- /wp:{bem_prefix}/organism-cta -->""",
                'syncStatus': 'unsynced'
            },
            f'{bem_prefix}-hero-section.php': {
                'title': f'Hero Section ({bem_prefix})',
                'description': 'Hero section reutilizable usando el bloque Hero personalizado del tema',
                'categories': [f'{bem_prefix}-hero', 'hero'],
                'content': f"""<!-- wp:{bem_prefix}/organism-hero {{"title":"Título Principal","subtitle":"Subtítulo descriptivo que captura la atención","buttonText":"Llamada a la acción","buttonUrl":"#","fullHeight":true,"showOverlay":true,"overlayOpacity":40}} -->
<div class="wp-block-{bem_prefix}-organism-hero {bem_prefix}-organism-hero--full-height">
<div class="{bem_prefix}-organism-hero__overlay" style="opacity:0.4"></div>
<div class="{bem_prefix}-organism-hero__content">
<h1 class="{bem_prefix}-organism-hero__title">Título Principal</h1>
<p class="{bem_prefix}-organism-hero__subtitle">Subtítulo descriptivo que captura la atención</p>
<a href="#" class="{bem_prefix}-organism-hero__button">Llamada a la acción</a>
</div>
</div>
<!-- /wp:{bem_prefix}/organism-hero -->""",
                'syncStatus': 'unsynced'
            },
            f'{bem_prefix}-cards-grid.php': {
                'title': f'Grid de Tarjetas ({bem_prefix})',
                'description': 'Grid reutilizable de tarjetas usando el bloque Cards personalizado del tema',
                'categories': [f'{bem_prefix}-cards', 'cards'],
                'content': f"""<!-- wp:{bem_prefix}/organism-cards-grid {{"title":"Nuestros Servicios","columns":3,"showButton":true,"buttonText":"Saber más"}} -->
<div class="wp-block-{bem_prefix}-organism-cards-grid">
<h2 class="{bem_prefix}-organism-cards-grid__title">Nuestros Servicios</h2>
<div class="{bem_prefix}-organism-cards-grid__container {bem_prefix}-organism-cards-grid__container--3-cols">
<!-- wp:{bem_prefix}/molecule-card {{"title":"Servicio 1","text":"Descripción breve del servicio.","buttonText":"Saber más"}} /-->
<!-- wp:{bem_prefix}/molecule-card {{"title":"Servicio 2","text":"Descripción breve del servicio.","buttonText":"Saber más"}} /-->
<!-- wp:{bem_prefix}/molecule-card {{"title":"Servicio 3","text":"Descripción breve del servicio.","buttonText":"Saber más"}} /-->
</div>
</div>
<!-- /wp:{bem_prefix}/organism-cards-grid -->""",
                'syncStatus': 'unsynced'
            },
            f'{bem_prefix}-testimonials-section.php': {
                'title': f'Sección de Testimonios ({bem_prefix})',
                'description': 'Testimonios usando el bloque Testimonial personalizado del tema',
                'categories': [f'{bem_prefix}-testimonials', 'testimonials'],
                'content': f"""<!-- wp:group {{"align":"wide","layout":{{"type":"constrained"}}}} -->
<div class="wp-block-group alignwide">
<!-- wp:heading {{"textAlign":"center","level":2}} -->
<h2 class="has-text-align-center">Lo que dicen nuestros clientes</h2>
<!-- /wp:heading -->
<!-- wp:columns {{"align":"wide"}} -->
<div class="wp-block-columns alignwide">
<!-- wp:column -->
<div class="wp-block-column">
<!-- wp:{bem_prefix}/molecule-testimonial {{"quote":"Excelente servicio y atención al cliente. Muy recomendado.","author":"Cliente Satisfecho"}} /-->
</div>
<!-- /wp:column -->
<!-- wp:column -->
<div class="wp-block-column">
<!-- wp:{bem_prefix}/molecule-testimonial {{"quote":"Profesionalismo y calidad en cada proyecto.","author":"Otro Cliente"}} /-->
</div>
<!-- /wp:column -->
</div>
<!-- /wp:columns -->
</div>
<!-- /wp:group -->""",
                'syncStatus': 'unsynced'
            }
        }
        
        # Generar archivos .php para cada patrón
        patterns_meta = []
        for filename, pattern_data in synced_patterns.items():
            slug = os.path.splitext(filename)[0]
            pattern_path = os.path.join(patterns_dir, filename)
            
            # Crear archivo PHP con metadata completa
            keywords_str = ', '.join(pattern_data.get('keywords', pattern_data.get('categories', [])))
            categories_str = ', '.join(pattern_data['categories'])
            block_types_str = ', '.join(pattern_data.get('blockTypes', ['core/post-content']))
            inserter_str = 'yes' if pattern_data.get('inserter', True) else 'no'
            viewport_width = pattern_data.get('viewportWidth', 1200)
            
            php_content = f"""<?php
/**
 * Title: {pattern_data['title']}
 * Slug: {bem_prefix}/{slug}
 * Description: {pattern_data['description']}
 * Categories: {categories_str}
 * Keywords: {keywords_str}
 * Viewport Width: {viewport_width}
 * Block Types: {block_types_str}
 * Inserter: {inserter_str}
 * Sync Status: {pattern_data.get('syncStatus', 'unsynced')}
 */
?>
{pattern_data['content']}
"""
            
            with open(pattern_path, 'w', encoding='utf-8') as f:
                f.write(php_content)
            
            # Agregar a metadata
            patterns_meta.append({
                'slug': f"{bem_prefix}/{slug}",
                'title': pattern_data['title'],
                'description': pattern_data['description'],
                'categories': pattern_data['categories'],
                'syncStatus': pattern_data.get('syncStatus', 'unsynced'),
                'filename': filename,
                'blockTypes': pattern_data.get('blockTypes', ['core/post-content']),
                'inserter': pattern_data.get('inserter', True),
                'viewportWidth': pattern_data.get('viewportWidth', 1200),
                'keywords': pattern_data.get('keywords', pattern_data.get('categories', [])),
                'version': '1.0.0',  # Versión inicial
                'created': datetime.now().isoformat(),
                'updated': datetime.now().isoformat()
            })
        
        # Guardar patterns_meta.json inicial
        meta_path = os.path.join(patterns_dir, 'patterns_meta.json')
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump({
                'patterns': patterns_meta,
                'generated': True,
                'bemPrefix': bem_prefix,
                'version': '1.0.0'
            }, f, ensure_ascii=False, indent=2)
        
        # Mejorar patterns_meta.json con versiones y metadatos
        try:
            from blocks_builder.versioning import enhance_patterns_meta_with_versions
            enhance_patterns_meta_with_versions(theme_dir, bem_prefix, plan, dna)
        except Exception as e:
            print(f"Advertencia: Error al mejorar versiones de patterns: {e}")
        
        # Actualizar functions.php para registrar patrones sincronizados
        functions_path = os.path.join(theme_dir, 'functions.php')
        if os.path.isfile(functions_path):
            with open(functions_path, 'r', encoding='utf-8') as f:
                functions_content = f.read()
            
            # Verificar si ya existe el registro de patrones sincronizados
            sync_function_name = f"{bem_prefix}_register_synced_patterns"
            if sync_function_name not in functions_content:
                # Agregar función para registrar patrones sincronizados
                sync_registration = f"""
// Registrar patrones sincronizados (Synced Patterns)
function {sync_function_name}() {{
    $patterns_dir = get_theme_file_path('patterns');
    if (!is_dir($patterns_dir)) return;
    
    // Registrar categorías de patrones
    register_block_pattern_category('{bem_prefix}-header', array('label' => 'Header'));
    register_block_pattern_category('{bem_prefix}-footer', array('label' => 'Footer'));
    register_block_pattern_category('{bem_prefix}-call-to-action', array('label' => 'Call to Action'));
    register_block_pattern_category('{bem_prefix}-hero', array('label' => 'Hero'));
    register_block_pattern_category('{bem_prefix}-cards', array('label' => 'Cards'));
    register_block_pattern_category('{bem_prefix}-testimonials', array('label' => 'Testimonials'));
    register_block_pattern_category('{bem_prefix}-sections', array('label' => 'Sections'));
    
    $pattern_files = glob($patterns_dir . '/*.php');
    foreach ($pattern_files as $file) {{
        $slug = basename($file, '.php');
        $content = file_get_contents($file);
        
        // Extraer metadata del header del archivo PHP
        if (preg_match('/Sync Status: (synced|unsynced)/i', $content, $matches)) {{
            $is_synced = strtolower($matches[1]) === 'synced';
            
            // Extraer título y descripción
            preg_match('/Title: (.+)/', $content, $title_match);
            preg_match('/Description: (.+)/', $content, $desc_match);
            preg_match('/Categories: (.+)/', $content, $cat_match);
            
            // Extraer solo el contenido HTML (después de ?>)
            $html_content = preg_replace('/.*?\\?>/s', '', $content);
            
            $title = isset($title_match[1]) ? trim($title_match[1]) : ucwords(str_replace('-', ' ', $slug));
            $description = isset($desc_match[1]) ? trim($desc_match[1]) : 'Patrón reutilizable';
            $cat_string = isset($cat_match[1]) ? trim($cat_match[1]) : '{bem_prefix}';
            $categories = array_map('trim', explode(',', $cat_string));
            
            // Registrar patrón con syncStatus
            register_block_pattern(
                '{bem_prefix}/' . $slug,
                array(
                    'title' => $title,
                    'description' => $description,
                    'content' => trim($html_content),
                    'categories' => $categories,
                    'syncStatus' => $is_synced ? 'synced' : 'unsynced',
                )
            );
        }}
    }}
}}
add_action('init', '{sync_function_name}', 20);
"""
                # Insertar antes del cierre del archivo o después de otros registros
                if 'add_action' in functions_content:
                    # Insertar después del último add_action
                    last_action = functions_content.rfind('add_action')
                    if last_action != -1:
                        last_action_end = functions_content.find('\n', last_action) + 1
                        functions_content = functions_content[:last_action_end] + sync_registration + functions_content[last_action_end:]
                    else:
                        functions_content += sync_registration
                else:
                    functions_content += sync_registration
                
                with open(functions_path, 'w', encoding='utf-8') as f:
                    f.write(functions_content)
        
        print(f"✓ Patrones globales generados: {len(synced_patterns)} patrones ({bem_prefix})")
        
    except Exception as e:
        print(f"Error al generar patrones globales: {e}")
        import traceback
        traceback.print_exc()


def generate_theme_documentation(theme_dir: str, theme_name: str, theme_description: str, theme_slug: Optional[str] = None, plan: Optional[Dict] = None, dna: Optional[Dict] = None):
    """
    Genera documentación automática completa del tema:
    - README.md del tema
    - Guía de estilos (styleguide.html)
    - Catálogo de componentes
    - Preview de patrones
    - Documentación de bloques
    """
    try:
        from blocks_builder import get_bem_prefix
        bem_prefix = get_bem_prefix(theme_slug)
        
        docs_dir = os.path.join(theme_dir, 'docs')
        os.makedirs(docs_dir, exist_ok=True)
        
        # 1. README.md del tema
        generate_theme_readme(theme_dir, theme_name, theme_description, theme_slug, plan, dna, bem_prefix)
        
        # 2. Guía de estilos (styleguide.html)
        generate_styleguide_html(theme_dir, theme_name, dna, bem_prefix)
        
        # 3. Catálogo de componentes
        generate_components_catalog(theme_dir, bem_prefix)
        
        # 4. Documentación completa de bloques (nueva versión mejorada)
        from blocks_builder.documentation import generate_comprehensive_block_docs, generate_patterns_documentation
        generate_comprehensive_block_docs(theme_dir, bem_prefix)
        
        # 5. Documentación de patterns
        generate_patterns_documentation(theme_dir, bem_prefix)
        
        # 6. Preview de patrones (legacy, mantener compatibilidad)
        generate_patterns_preview(theme_dir, bem_prefix)
        
        print(f"✓ Documentación del tema generada en {docs_dir}/")
        
    except Exception as e:
        print(f"Error al generar documentación: {e}")
        import traceback
        traceback.print_exc()


def generate_theme_readme(theme_dir: str, theme_name: str, theme_description: str, theme_slug: Optional[str], plan: Optional[Dict], dna: Optional[Dict], bem_prefix: str):
    """Genera README.md completo del tema."""
    readme_path = os.path.join(theme_dir, 'README.md')
    
    # Extraer información del plan
    sections_info = ""
    if isinstance(plan, dict):
        sections = plan.get('sections', [])
        if sections:
            sections_info = "\n## Secciones del Tema\n\n"
            for i, section in enumerate(sections, 1):
                label = section.get('label', f'Sección {i}')
                slug = section.get('slug', '')
                sections_info += f"- **{label}** (`{slug}`)\n"
    
    # Información de colores
    colors_info = ""
    if isinstance(dna, dict):
        palette = dna.get('palette', [])
        if palette:
            colors_info = "\n## Paleta de Colores\n\n"
            for color in palette:
                slug = color.get('slug', '')
                hex_color = color.get('color', '')
                colors_info += f"- **{slug.title()}**: `{hex_color}`\n"
    
    readme_content = f"""# {theme_name}

{theme_description}

## Información del Tema

- **Nombre**: {theme_name}
- **Slug**: {theme_slug or 'img2html'}
- **Prefijo BEM**: `{bem_prefix}`
- **Versión**: 1.0.0
- **Framework CSS**: Configurable (Tailwind CSS / Bootstrap 5 / CSS Propio)

## Estructura del Tema

Este tema sigue la metodología **Atomic Design**:

```
blocks/
  atoms/          # Componentes básicos reutilizables
  molecules/      # Combinaciones de átomos
  organisms/      # Componentes complejos
patterns/         # Patrones sincronizados y reutilizables
templates/        # Plantillas FSE
parts/            # Template parts
assets/           # Imágenes, CSS, JS
```

## Bloques Disponibles

### Átomos
Componentes básicos reutilizables:
- `{bem_prefix}/atom-button` - Botón básico
- `{bem_prefix}/atom-heading` - Título
- `{bem_prefix}/atom-input` - Campo de entrada
- `{bem_prefix}/atom-icon` - Icono
- `{bem_prefix}/atom-badge` - Badge/Etiqueta
- `{bem_prefix}/atom-link` - Enlace

### Moléculas
Combinaciones de átomos:
- `{bem_prefix}/molecule-card` - Tarjeta
- `{bem_prefix}/molecule-form-field` - Campo de formulario
- `{bem_prefix}/molecule-nav-item` - Item de navegación
- `{bem_prefix}/molecule-testimonial` - Testimonio
- `{bem_prefix}/molecule-pricing-item` - Item de precio

### Organismos
Componentes complejos:
- `{bem_prefix}/organism-slider` - Slider de imágenes
- `{bem_prefix}/organism-hero` - Sección Hero
- `{bem_prefix}/organism-section` - Sección multipropósito
- `{bem_prefix}/organism-cards-grid` - Grid de tarjetas
- `{bem_prefix}/organism-gallery` - Galería
- `{bem_prefix}/organism-header` - Header
- `{bem_prefix}/organism-footer` - Footer
- `{bem_prefix}/organism-form` - Formulario
- `{bem_prefix}/organism-menu` - Menú
- `{bem_prefix}/organism-sidebar` - Sidebar
- `{bem_prefix}/organism-search` - Buscador
- `{bem_prefix}/organism-pagination` - Paginación

## Patrones Sincronizados

Los patrones sincronizados se actualizan globalmente:
- `{bem_prefix}/header-global` - Header global
- `{bem_prefix}/footer-global` - Footer global

## Patrones Reutilizables

- `{bem_prefix}/cta-primary` - Call to Action
- `{bem_prefix}/hero-section` - Sección Hero
- `{bem_prefix}/cards-grid` - Grid de tarjetas
- `{bem_prefix}/testimonials-section` - Sección de testimonios

## Documentación

- **Guía de Estilos**: Ver `docs/styleguide.html`
- **Catálogo de Componentes**: Ver `docs/components-catalog.md`
- **Documentación de Bloques**: Ver `docs/blocks/`
- **Preview de Patrones**: Ver `docs/patterns-preview.html`

## Instalación

1. Sube el tema a `wp-content/themes/{theme_slug or 'img2html'}/`
2. Activa el tema desde WordPress Admin → Apariencia → Temas
3. Ve a Editor del Sitio para personalizar

## Personalización

Todos los bloques son editables desde el Editor de Bloques de WordPress.
Los colores y tipografías se pueden ajustar desde Editor del Sitio → Estilos.

{sections_info}
{colors_info}

## Soporte

Este tema fue generado automáticamente con Img2HTML.
Para más información, consulta la documentación en `docs/`.
"""
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)


def generate_styleguide_html(theme_dir: str, theme_name: str, dna: Optional[Dict], bem_prefix: str):
    """Genera styleguide.html con guía visual de estilos."""
    docs_dir = os.path.join(theme_dir, 'docs')
    styleguide_path = os.path.join(docs_dir, 'styleguide.html')
    
    # Extraer colores
    colors_html = ""
    if isinstance(dna, dict):
        palette = dna.get('palette', [])
        for color in palette:
            slug = color.get('slug', '')
            hex_color = color.get('color', '')
            colors_html += f"""
        <div class="color-swatch">
            <div class="color-box" style="background-color: {hex_color};"></div>
            <div class="color-info">
                <strong>{slug.title()}</strong>
                <code>{hex_color}</code>
            </div>
        </div>"""
    
    styleguide_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guía de Estilos - {theme_name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: system-ui, -apple-system, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        header {{
            background: #fff;
            padding: 2rem;
            margin-bottom: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{ font-size: 2.5rem; margin-bottom: 0.5rem; }}
        h2 {{ font-size: 2rem; margin: 2rem 0 1rem; border-bottom: 2px solid #ddd; padding-bottom: 0.5rem; }}
        h3 {{ font-size: 1.5rem; margin: 1.5rem 0 1rem; }}
        section {{
            background: #fff;
            padding: 2rem;
            margin-bottom: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .color-palette {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-top: 1rem;
        }}
        .color-swatch {{
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
        }}
        .color-box {{
            height: 100px;
            width: 100%;
        }}
        .color-info {{
            padding: 1rem;
            background: #fff;
        }}
        .color-info code {{
            display: block;
            margin-top: 0.5rem;
            color: #666;
            font-size: 0.875rem;
        }}
        .typography-sample {{
            margin: 1rem 0;
            padding: 1rem;
            background: #f9f9f9;
            border-left: 4px solid #3b82f6;
        }}
        .spacing-demo {{
            display: flex;
            align-items: center;
            gap: 1rem;
            margin: 1rem 0;
        }}
        .spacing-box {{
            background: #3b82f6;
            color: white;
            padding: 0.5rem;
            border-radius: 4px;
        }}
        .component-demo {{
            border: 2px dashed #ddd;
            padding: 2rem;
            margin: 1rem 0;
            border-radius: 8px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Guía de Estilos</h1>
            <p>{theme_name}</p>
            <p><strong>Prefijo BEM:</strong> <code>{bem_prefix}</code></p>
        </header>

        <section id="colors">
            <h2>Paleta de Colores</h2>
            <div class="color-palette">
                {colors_html if colors_html else '<p>No hay colores definidos</p>'}
            </div>
        </section>

        <section id="typography">
            <h2>Tipografía</h2>
            <div class="typography-sample">
                <h1 style="font-size: 3rem; margin-bottom: 0.5rem;">Heading 1</h1>
                <h2 style="font-size: 2.25rem; margin-bottom: 0.5rem;">Heading 2</h2>
                <h3 style="font-size: 1.875rem; margin-bottom: 0.5rem;">Heading 3</h3>
                <h4 style="font-size: 1.5rem; margin-bottom: 0.5rem;">Heading 4</h4>
                <p style="font-size: 1rem; line-height: 1.6;">Párrafo de ejemplo. Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
            </div>
        </section>

        <section id="spacing">
            <h2>Sistema de Espaciado</h2>
            <div class="spacing-demo">
                <div class="spacing-box" style="padding: 4px;">xs (4px)</div>
                <div class="spacing-box" style="padding: 8px;">sm (8px)</div>
                <div class="spacing-box" style="padding: 16px;">md (16px)</div>
                <div class="spacing-box" style="padding: 24px;">lg (24px)</div>
                <div class="spacing-box" style="padding: 32px;">xl (32px)</div>
            </div>
        </section>

        <section id="components">
            <h2>Componentes</h2>
            <div class="component-demo">
                <h3>Botón</h3>
                <button style="padding: 0.75rem 1.5rem; background: #3b82f6; color: white; border: none; border-radius: 0.5rem; cursor: pointer; margin-right: 1rem;">Botón Primario</button>
                <button style="padding: 0.75rem 1.5rem; background: transparent; color: #3b82f6; border: 2px solid #3b82f6; border-radius: 0.5rem; cursor: pointer;">Botón Outline</button>
            </div>
            <div class="component-demo">
                <h3>Badge</h3>
                <span style="display: inline-block; padding: 0.25rem 0.75rem; background: #3b82f6; color: white; border-radius: 9999px; font-size: 0.875rem; margin-right: 0.5rem;">Nuevo</span>
                <span style="display: inline-block; padding: 0.25rem 0.75rem; background: #10b981; color: white; border-radius: 9999px; font-size: 0.875rem;">Éxito</span>
            </div>
        </section>
    </div>
</body>
</html>
"""
    
    with open(styleguide_path, 'w', encoding='utf-8') as f:
        f.write(styleguide_content)


def generate_components_catalog(theme_dir: str, bem_prefix: str):
    """Genera catálogo de componentes en Markdown."""
    docs_dir = os.path.join(theme_dir, 'docs')
    catalog_path = os.path.join(docs_dir, 'components-catalog.md')
    
    catalog_content = f"""# Catálogo de Componentes

Este documento lista todos los componentes disponibles en el tema.

## Átomos

### {bem_prefix}/atom-button
**Descripción**: Botón básico reutilizable con variantes.

**Atributos**:
- `text` (string): Texto del botón
- `url` (string): URL de destino
- `variant` (string): Variante (primary, secondary, outline)
- `size` (string): Tamaño (sm, md, lg)
- `fullWidth` (boolean): Ancho completo

**Cuándo usar**: Para cualquier acción o enlace que requiera un botón.

**Cuándo NO usar**: Para elementos de navegación complejos (usar molecule-nav-item).

---

### {bem_prefix}/atom-heading
**Descripción**: Título reutilizable.

**Atributos**:
- `text` (string): Texto del título
- `level` (number): Nivel de heading (1-6)
- `align` (string): Alineación (left, center, right)

**Cuándo usar**: Para títulos en cualquier parte del tema.

---

### {bem_prefix}/atom-input
**Descripción**: Campo de entrada básico.

**Atributos**:
- `type` (string): Tipo de input (text, email, tel, etc.)
- `placeholder` (string): Placeholder
- `name` (string): Nombre del campo
- `required` (boolean): Campo requerido

**Cuándo usar**: Dentro de moléculas de formulario.

---

### {bem_prefix}/atom-icon
**Descripción**: Icono reutilizable.

**Atributos**:
- `name` (string): Nombre del icono
- `size` (string): Tamaño (sm, md, lg)

**Cuándo usar**: Para iconos decorativos o informativos.

---

### {bem_prefix}/atom-badge
**Descripción**: Badge/Etiqueta.

**Atributos**:
- `text` (string): Texto del badge
- `variant` (string): Variante (primary, success, warning)

**Cuándo usar**: Para etiquetas, estados o indicadores.

---

### {bem_prefix}/atom-link
**Descripción**: Enlace básico.

**Atributos**:
- `text` (string): Texto del enlace
- `url` (string): URL de destino
- `target` (string): Target (_self, _blank)

**Cuándo usar**: Para enlaces simples.

---

## Moléculas

### {bem_prefix}/molecule-card
**Descripción**: Tarjeta que combina heading, texto, imagen y botón.

**Atributos**:
- `title` (string): Título de la tarjeta
- `text` (string): Descripción
- `imageUrl` (string): URL de la imagen
- `buttonText` (string): Texto del botón
- `buttonUrl` (string): URL del botón

**Cuándo usar**: Para mostrar contenido estructurado (servicios, productos, features).

**Componentes usados**: atom-heading, atom-button

---

### {bem_prefix}/molecule-form-field
**Descripción**: Campo de formulario con label.

**Atributos**:
- `label` (string): Etiqueta del campo
- `type` (string): Tipo de input
- `name` (string): Nombre del campo
- `placeholder` (string): Placeholder
- `required` (boolean): Campo requerido

**Cuándo usar**: Dentro de organismos de formulario.

**Componentes usados**: atom-input

---

### {bem_prefix}/molecule-nav-item
**Descripción**: Item de navegación con enlace e icono opcional.

**Atributos**:
- `text` (string): Texto del enlace
- `url` (string): URL de destino
- `icon` (string): Nombre del icono (opcional)

**Cuándo usar**: En menús de navegación.

**Componentes usados**: atom-link, atom-icon

---

### {bem_prefix}/molecule-testimonial
**Descripción**: Testimonio con cita y autor.

**Atributos**:
- `quote` (string): Texto del testimonio
- `author` (string): Nombre del autor
- `role` (string): Rol/cargo del autor
- `imageUrl` (string): Foto del autor

**Cuándo usar**: Para mostrar testimonios de clientes.

---

### {bem_prefix}/molecule-pricing-item
**Descripción**: Item de precio con características.

**Atributos**:
- `title` (string): Nombre del plan
- `price` (string): Precio
- `period` (string): Período (/mes, /año)
- `features` (array): Lista de características
- `buttonText` (string): Texto del botón
- `buttonUrl` (string): URL del botón
- `featured` (boolean): Plan destacado

**Cuándo usar**: Para tablas de precios.

**Componentes usados**: atom-button

---

## Organismos

### {bem_prefix}/organism-slider
**Descripción**: Slider de imágenes con navegación.

**Cuándo usar**: Para mostrar múltiples imágenes o contenido en carrusel.

**Componentes usados**: Varios átomos y moléculas según configuración.

---

### {bem_prefix}/organism-hero
**Descripción**: Sección Hero con imagen de fondo.

**Cuándo usar**: Como primera sección de la página principal.

---

### {bem_prefix}/organism-cards-grid
**Descripción**: Grid de tarjetas.

**Cuándo usar**: Para mostrar múltiples cards en grid.

**Componentes usados**: molecule-card

---

### {bem_prefix}/organism-header
**Descripción**: Header del sitio.

**Cuándo usar**: En template parts globales.

**Componentes usados**: molecule-nav-item

---

### {bem_prefix}/organism-footer
**Descripción**: Footer del sitio.

**Cuándo usar**: En template parts globales.

---

### {bem_prefix}/organism-form
**Descripción**: Formulario completo.

**Cuándo usar**: Para formularios de contacto o suscripción.

**Componentes usados**: molecule-form-field, atom-button

---

## Guía de Uso

### Cuándo usar Átomos
- Componentes básicos que no tienen lógica compleja
- Elementos que se repiten frecuentemente
- Componentes que forman parte de moléculas

### Cuándo usar Moléculas
- Combinaciones lógicas de átomos
- Componentes que tienen una función específica
- Elementos que se pueden reutilizar en diferentes contextos

### Cuándo usar Organismos
- Componentes complejos que forman secciones completas
- Elementos que combinan múltiples moléculas
- Componentes que tienen lógica y estado complejo

## Mejores Prácticas

1. **Reutilización**: Siempre usa átomos y moléculas existentes antes de crear nuevos
2. **Composición**: Construye organismos usando moléculas, no átomos directamente
3. **Nomenclatura**: Sigue el prefijo BEM `{bem_prefix}`
4. **Documentación**: Documenta cualquier componente nuevo que crees
"""
    
    with open(catalog_path, 'w', encoding='utf-8') as f:
        f.write(catalog_content)


def generate_blocks_documentation(theme_dir: str, bem_prefix: str):
    """Genera documentación individual para cada bloque."""
    blocks_dir = os.path.join(theme_dir, 'blocks')
    docs_blocks_dir = os.path.join(theme_dir, 'docs', 'blocks')
    os.makedirs(docs_blocks_dir, exist_ok=True)
    
    # Documentar átomos
    atoms = ['button', 'heading', 'input', 'icon', 'badge', 'link']
    for atom in atoms:
        atom_dir = os.path.join(blocks_dir, 'atoms', atom)
        if os.path.isdir(atom_dir):
            block_json_path = os.path.join(atom_dir, 'block.json')
            if os.path.isfile(block_json_path):
                try:
                    with open(block_json_path, 'r', encoding='utf-8') as f:
                        block_data = json.load(f)
                    
                    doc_path = os.path.join(docs_blocks_dir, f'atom-{atom}.md')
                    doc_content = f"""# {block_data.get('title', atom.title())}

**Tipo**: Átomo  
**Nombre**: `{block_data.get('name', '')}`  
**Categoría**: {block_data.get('category', '')}

## Descripción

{block_data.get('description', 'Componente básico reutilizable')}

## Atributos

"""
                    attributes = block_data.get('attributes', {})
                    for attr_name, attr_data in attributes.items():
                        attr_type = attr_data.get('type', 'unknown')
                        attr_default = attr_data.get('default', 'N/A')
                        doc_content += f"- **{attr_name}** (`{attr_type}`): {attr_default}\n"
                    
                    doc_content += f"""
## Cuándo usar

Este átomo se usa como componente básico en moléculas y organismos.

## Ejemplo de uso

```html
<!-- wp:{block_data.get('name', '')} {{"text": "Ejemplo"}} /-->
```

## Estilos

Los estilos siguen la metodología BEM con prefijo `{bem_prefix}`.
Clase principal: `{bem_prefix}-atom-{atom}`
"""
                    with open(doc_path, 'w', encoding='utf-8') as f:
                        f.write(doc_content)
                except Exception:
                    pass
    
    # Documentar moléculas
    molecules = ['card', 'form-field', 'nav-item', 'testimonial', 'pricing-item']
    for molecule in molecules:
        molecule_dir = os.path.join(blocks_dir, 'molecules', molecule)
        if os.path.isdir(molecule_dir):
            block_json_path = os.path.join(molecule_dir, 'block.json')
            if os.path.isfile(block_json_path):
                try:
                    with open(block_json_path, 'r', encoding='utf-8') as f:
                        block_data = json.load(f)
                    
                    doc_path = os.path.join(docs_blocks_dir, f'molecule-{molecule}.md')
                    doc_content = f"""# {block_data.get('title', molecule.title())}

**Tipo**: Molécula  
**Nombre**: `{block_data.get('name', '')}`  
**Categoría**: {block_data.get('category', '')}

## Descripción

{block_data.get('description', 'Combinación de átomos')}

## Atributos

"""
                    attributes = block_data.get('attributes', {})
                    for attr_name, attr_data in attributes.items():
                        attr_type = attr_data.get('type', 'unknown')
                        attr_default = attr_data.get('default', 'N/A')
                        doc_content += f"- **{attr_name}** (`{attr_type}`): {attr_default}\n"
                    
                    doc_content += f"""
## Componentes usados

Esta molécula combina los siguientes átomos:
- (Ver código fuente para detalles)

## Cuándo usar

{block_data.get('description', '')}

## Ejemplo de uso

```html
<!-- wp:{block_data.get('name', '')} /-->
```

## Estilos

Clase principal: `{bem_prefix}-molecule-{molecule}`
"""
                    with open(doc_path, 'w', encoding='utf-8') as f:
                        f.write(doc_content)
                except Exception:
                    pass
    
    # Documentar organismos
    organisms = ['slider', 'hero', 'section', 'cards', 'gallery', 'header', 'footer', 'form', 'menu']
    for organism in organisms:
        organism_dir = os.path.join(blocks_dir, 'organisms', organism)
        if os.path.isdir(organism_dir):
            block_json_path = os.path.join(organism_dir, 'block.json')
            if os.path.isdir(organism_dir) and os.path.isfile(block_json_path):
                try:
                    with open(block_json_path, 'r', encoding='utf-8') as f:
                        block_data = json.load(f)
                    
                    doc_path = os.path.join(docs_blocks_dir, f'organism-{organism}.md')
                    doc_content = f"""# {block_data.get('title', organism.title())}

**Tipo**: Organismo  
**Nombre**: `{block_data.get('name', '')}`  
**Categoría**: {block_data.get('category', '')}

## Descripción

{block_data.get('description', 'Componente complejo')}

## Atributos

"""
                    attributes = block_data.get('attributes', {})
                    for attr_name, attr_data in attributes.items():
                        attr_type = attr_data.get('type', 'unknown')
                        attr_default = attr_data.get('default', 'N/A')
                        doc_content += f"- **{attr_name}** (`{attr_type}`): {attr_default}\n"
                    
                    doc_content += f"""
## Componentes usados

Este organismo puede usar moléculas y átomos según su configuración.

## Cuándo usar

Para secciones completas y componentes complejos.

## Ejemplo de uso

```html
<!-- wp:{block_data.get('name', '')} /-->
```

## Estilos

Clase principal: `{bem_prefix}-organism-{organism}`
"""
                    with open(doc_path, 'w', encoding='utf-8') as f:
                        f.write(doc_content)
                except Exception:
                    pass


def generate_patterns_preview(theme_dir: str, bem_prefix: str):
    """Genera preview HTML de todos los patrones."""
    patterns_dir = os.path.join(theme_dir, 'patterns')
    docs_dir = os.path.join(theme_dir, 'docs')
    preview_path = os.path.join(docs_dir, 'patterns-preview.html')
    
    if not os.path.isdir(patterns_dir):
        return
    
    # Leer metadata de patrones
    meta_path = os.path.join(patterns_dir, 'patterns_meta.json')
    patterns_meta = []
    if os.path.isfile(meta_path):
        try:
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta_data = json.load(f)
                patterns_meta = meta_data.get('patterns', [])
        except Exception:
            pass
    
    patterns_html = ""
    for pattern in patterns_meta:
        slug = pattern.get('slug', '')
        title = pattern.get('title', '')
        description = pattern.get('description', '')
        sync_status = pattern.get('syncStatus', 'unsynced')
        sync_badge = '🔄 Sincronizado' if sync_status == 'synced' else '📄 Reutilizable'
        
        patterns_html += f"""
        <div class="pattern-card">
            <div class="pattern-header">
                <h3>{title}</h3>
                <span class="sync-badge">{sync_badge}</span>
            </div>
            <p class="pattern-description">{description}</p>
            <div class="pattern-info">
                <strong>Slug:</strong> <code>{slug}</code><br>
                <strong>Categorías:</strong> {', '.join(pattern.get('categories', []))}
            </div>
            <div class="pattern-preview">
                <p><em>Vista previa disponible en WordPress Editor</em></p>
            </div>
        </div>"""
    
    if not patterns_html:
        patterns_html = "<p>No hay patrones disponibles</p>"
    
    preview_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Preview de Patrones - {bem_prefix}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: system-ui, -apple-system, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 2rem;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        header {{
            background: #fff;
            padding: 2rem;
            margin-bottom: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{ font-size: 2.5rem; margin-bottom: 0.5rem; }}
        .patterns-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1.5rem;
        }}
        .pattern-card {{
            background: #fff;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .pattern-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 1rem;
        }}
        .pattern-header h3 {{
            font-size: 1.25rem;
            margin: 0;
        }}
        .sync-badge {{
            font-size: 0.75rem;
            padding: 0.25rem 0.5rem;
            background: #e0e7ff;
            color: #4338ca;
            border-radius: 4px;
        }}
        .pattern-description {{
            color: #666;
            margin-bottom: 1rem;
        }}
        .pattern-info {{
            font-size: 0.875rem;
            color: #666;
            margin-bottom: 1rem;
            padding: 1rem;
            background: #f9f9f9;
            border-radius: 4px;
        }}
        .pattern-info code {{
            background: #e5e7eb;
            padding: 0.125rem 0.25rem;
            border-radius: 2px;
            font-size: 0.875rem;
        }}
        .pattern-preview {{
            border: 2px dashed #ddd;
            padding: 2rem;
            text-align: center;
            color: #999;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Preview de Patrones</h1>
            <p>Catálogo de todos los patrones disponibles en el tema</p>
        </header>
        
        <div class="patterns-grid">
            {patterns_html}
        </div>
    </div>
</body>
</html>
"""
    
    with open(preview_path, 'w', encoding='utf-8') as f:
        f.write(preview_content)


def ensure_cpt_php(theme_dir: str, plan: Optional[Dict] = None):
    try:
        php_dir = os.path.join(theme_dir, 'php')
        os.makedirs(php_dir, exist_ok=True)
        cpt_path = os.path.join(php_dir, 'cpt.php')

        # Detección simple desde el plan
        wanted = set()
        if isinstance(plan, dict):
            sections = plan.get('sections', [])
            for s in sections:
                name = (s.get('name') or s.get('label') or '').lower()
                if any(k in name for k in ['portfolio', 'work', 'project']):
                    wanted.add('portfolio')
                if any(k in name for k in ['testimonial', 'review']):
                    wanted.add('testimonial')
                if any(k in name for k in ['service', 'servicio']):
                    wanted.add('service')
                if any(k in name for k in ['shop', 'tienda', 'product', 'producto']):
                    wanted.add('woocommerce')

        cpt_defs = {
            'portfolio': {'label': 'Portfolio', 'supports': ['title','editor','thumbnail','excerpt']},
            'testimonial': {'label': 'Testimonio', 'supports': ['title','editor','thumbnail','excerpt']},
            'service': {'label': 'Servicio', 'supports': ['title','editor','thumbnail','excerpt']},
        }

        lines = ["<?php", "// CPT auto-generados por img2html"]
        lines.append("add_action('init', function() {")
        for slug, cfg in cpt_defs.items():
            if wanted and slug not in wanted:
                continue
            lines.append(f"    if (!post_type_exists('{slug}')) {{")
            lines.append(f"        register_post_type('{slug}', [")
            lines.append(f"            'label' => '{cfg['label']}',")
            lines.append("            'public' => true,")
            lines.append("            'show_in_rest' => true,")
            lines.append("            'has_archive' => true,")
            lines.append(f"            'supports' => {cfg['supports']!r},")
            lines.append(f"            'rewrite' => ['slug' => '{slug}'],")
            lines.append("        ]);")
            lines.append("    }")
        lines.append("});")

        # WooCommerce hook básico si se detecta
        if 'woocommerce' in wanted:
            lines.append("")
            lines.append("// Hook básico para WooCommerce: asegurar soporte de imágenes y miniaturas")
            lines.append("add_theme_support('woocommerce');")
            lines.append("add_theme_support('wc-product-gallery-zoom');")
            lines.append("add_theme_support('wc-product-gallery-lightbox');")
            lines.append("add_theme_support('wc-product-gallery-slider');")

        with open(cpt_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))

    except Exception as e:
        print(f"Error al generar cpt.php: {e}")


def optimize_images(images: List[str], output_dir: str):
    """
    Genera variantes optimizadas (webp y tamaños) para cada imagen.
    """
    try:
        from PIL import Image
    except Exception:
        print("PIL no disponible, se omite optimización de imágenes")
        return
    os.makedirs(output_dir, exist_ok=True)
    sizes = {
        'thumb': 300,
        'medium': 768,
        'large': 1280
    }
    optimized_map = {}
    for img_path in images or []:
        try:
            im = Image.open(img_path).convert('RGB')
            base = os.path.splitext(os.path.basename(img_path))[0]
            for label, max_w in sizes.items():
                w, h = im.size
                if w <= max_w:
                    resized = im
                else:
                    ratio = h / float(w)
                    new_h = int(max_w * ratio)
                    resized = im.resize((max_w, new_h))
                out_jpg = os.path.join(output_dir, f"{base}-{label}.jpg")
                resized.save(out_jpg, 'JPEG', quality=85, optimize=True)
                out_webp = os.path.join(output_dir, f"{base}-{label}.webp")
                resized.save(out_webp, 'WEBP', quality=80, method=6)
                optimized_map.setdefault(img_path, {})[label] = {
                    "jpg": out_jpg,
                    "webp": out_webp
                }
        except Exception as e:
            print(f"No se pudo optimizar {img_path}: {e}")
    return optimized_map

def generate_theme_screenshot(theme_dir: str, plan: Dict, dna: Optional[Dict] = None, theme_name: str = "Img2HTML AI Theme", theme_description: str = "Tema de bloques generado y refinado con IA"):
    """
    Genera un screenshot SVG del tema basado en el plan y DNA.
    El screenshot se guarda como screenshot.png (WordPress lo usa como portada del tema).
    """
    try:
        # Extraer colores del DNA
        palette = []
        if isinstance(dna, dict):
            palette = dna.get('palette', [])
        
        bg_color = "#ffffff"
        text_color = "#111111"
        primary_color = "#3b82f6"
        secondary_color = "#64748b"
        
        for p in palette:
            slug = p.get('slug', '')
            color = p.get('color', '')
            if slug == 'background':
                bg_color = color
            elif slug == 'text':
                text_color = color
            elif slug == 'primary':
                primary_color = color
            elif slug == 'secondary':
                secondary_color = color
        
        # Obtener secciones del plan
        sections = plan.get('sections', [])
        section_count = len(sections)
        
        # Dimensiones del screenshot (1200x900 es el estándar de WordPress)
        width = 1200
        height = 900
        
        # Crear SVG
        svg_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{bg_color};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{secondary_color};stop-opacity:0.3" />
    </linearGradient>
  </defs>
  
  <!-- Fondo -->
  <rect width="{width}" height="{height}" fill="url(#bgGradient)"/>
  
  <!-- Header -->
  <rect x="0" y="0" width="{width}" height="80" fill="{primary_color}" opacity="0.9"/>
  <text x="{width//2}" y="50" font-family="system-ui, -apple-system, sans-serif" font-size="32" font-weight="bold" fill="{text_color}" text-anchor="middle">{theme_name[:40]}</text>
  
  <!-- Secciones -->
"""
        
        # Dibujar secciones
        section_height = (height - 120) // max(section_count, 1)
        y_pos = 100
        
        for idx, section in enumerate(sections[:6]):  # Máximo 6 secciones visibles
            label = section.get('label', f'Sección {idx + 1}')
            pattern = section.get('pattern', '').lower()
            
            # Determinar color de la sección
            section_bg = primary_color if 'hero' in pattern else bg_color
            section_text = text_color if 'hero' not in pattern else bg_color
            
            # Dibujar sección
            svg_content += f"""  <!-- Sección: {label} -->
  <rect x="40" y="{y_pos}" width="{width-80}" height="{section_height-20}" fill="{section_bg}" opacity="0.8" rx="8"/>
  <text x="{width//2}" y="{y_pos + section_height//2}" font-family="system-ui, -apple-system, sans-serif" font-size="24" font-weight="600" fill="{section_text}" text-anchor="middle">{label[:50]}</text>
  
"""
            y_pos += section_height
        
        # Footer
        svg_content += f"""  <!-- Footer -->
  <rect x="0" y="{height-60}" width="{width}" height="60" fill="{secondary_color}" opacity="0.7"/>
  <text x="{width//2}" y="{height-20}" font-family="system-ui, -apple-system, sans-serif" font-size="14" fill="{text_color}" text-anchor="middle">{theme_description[:80]}</text>
  
  <!-- Decoración -->
  <circle cx="{width-100}" cy="150" r="30" fill="{primary_color}" opacity="0.2"/>
  <circle cx="100" cy="{height-150}" r="40" fill="{secondary_color}" opacity="0.15"/>
</svg>
"""
        
        # Guardar screenshot SVG
        svg_path = os.path.join(theme_dir, 'screenshot.svg')
        with open(svg_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        # Intentar convertir SVG a PNG si es posible (WordPress prefiere PNG)
        screenshot_path = os.path.join(theme_dir, 'screenshot.png')
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Crear PNG simple basado en el diseño
            img = Image.new('RGB', (width, height), bg_color)
            draw = ImageDraw.Draw(img)
            
            # Dibujar header
            header_color = tuple(int(primary_color[i:i+2], 16) for i in (1, 3, 5))
            draw.rectangle([0, 0, width, 80], fill=header_color)
            
            # Dibujar secciones
            section_height = (height - 120) // max(section_count, 1)
            y_pos = 100
            for idx, section in enumerate(sections[:6]):
                label = section.get('label', f'Sección {idx + 1}')
                pattern = section.get('pattern', '').lower()
                section_bg = header_color if 'hero' in pattern else tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5))
                text_col = tuple(int(text_color[i:i+2], 16) for i in (1, 3, 5))
                
                draw.rectangle([40, y_pos, width-40, y_pos + section_height - 20], 
                              fill=section_bg, outline=tuple(int(secondary_color[i:i+2], 16) for i in (1, 3, 5)), width=2)
                
                # Texto
                try:
                    font = ImageFont.truetype("arial.ttf", 20) if os.name == 'nt' else ImageFont.load_default()
                except:
                    font = ImageFont.load_default()
                
                text_bbox = draw.textbbox((0, 0), label[:30], font=font)
                text_width = text_bbox[2] - text_bbox[0]
                draw.text(((width - text_width) // 2, y_pos + (section_height - 20) // 2 - 10), 
                         label[:30], fill=text_col, font=font)
                
                y_pos += section_height
            
            # Footer
            footer_color = tuple(int(secondary_color[i:i+2], 16) for i in (1, 3, 5))
            draw.rectangle([0, height-60, width, height], fill=footer_color)
            
            img.save(screenshot_path, 'PNG', quality=95)
            print(f"Screenshot PNG generado: {screenshot_path}")
        except Exception as e:
            # Si falla la conversión, al menos tenemos el SVG
            print(f"Nota: No se pudo generar PNG, solo SVG: {e}")
        
        print(f"Screenshot SVG generado: {svg_path}")
        
    except Exception as e:
        print(f"Error al generar screenshot: {e}")

