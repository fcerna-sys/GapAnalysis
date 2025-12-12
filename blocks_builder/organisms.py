"""
Módulo para crear componentes complejos (organismos).
Contiene TODAS las funciones create_*_block.
Código completo migrado desde blocks_builder_backup.py
"""
import os
import json
from .renders import (
    _generate_slider_render_php,
    _render_simple_section,
    _render_sidebar,
    _render_search,
    _render_pagination,
    _render_header,
    _render_footer,
    _render_form,
    _render_menu,
    _render_gallery,
    _render_section,
    _render_cards,
    _render_hero,
)
from .editors import (
    _generate_slider_editor_js,
    _editor_simple_section,
    _editor_sidebar,
    _editor_search,
    _editor_pagination,
    _editor_header,
    _editor_footer,
    _editor_form,
    _editor_menu,
)
from .styles import (
    _generate_slider_style_css,
    _generate_slider_editor_css,
)


def create_slider_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """
    Crea el bloque Slider completo con todas las funcionalidades.
    Usa prefijo BEM para clases CSS.
    NOTA: Esta función crea en blocks_dir directamente. Use create_organism_slider para estructura atómica.
    """
    slider_dir = os.path.join(blocks_dir, 'slider')
    os.makedirs(slider_dir, exist_ok=True)
    
    # block.json
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": f"{bem_prefix}/slider",
        "version": "1.0.0",
        "title": "Slider",
        "category": f"{bem_prefix}-organisms",
        "icon": "slides",
        "description": "Slider administrable con múltiples diapositivas",
        "keywords": ["slider", "carousel", "slideshow"],
        "textdomain": bem_prefix,
        "editorScript": "file:./index.js",
        "editorStyle": "file:./editor.css",
        "style": "file:./style.css",
        "render": "file:./render.php",
        "supports": {
            "align": ["wide", "full"],
            "html": False
        },
        "attributes": {
            "showSlider": {
                "type": "boolean",
                "default": True
            },
            "fullWidth": {
                "type": "boolean",
                "default": False
            },
            "showArrows": {
                "type": "boolean",
                "default": True
            },
            "showDots": {
                "type": "boolean",
                "default": True
            },
            "autoplay": {
                "type": "boolean",
                "default": True
            },
            "autoplaySpeed": {
                "type": "number",
                "default": 5000
            },
            "transitionSpeed": {
                "type": "number",
                "default": 500
            },
            "height": {
                "type": "string",
                "default": "70vh"
            },
            "slides": {
                "type": "array",
                "default": []
            }
        }
    }
    
    block_json_path = os.path.join(slider_dir, 'block.json')
    with open(block_json_path, 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2, ensure_ascii=False)
    
    # render.php (frontend)
    render_php = _generate_slider_render_php(css_framework, bem_prefix)
    render_path = os.path.join(slider_dir, 'render.php')
    with open(render_path, 'w', encoding='utf-8') as f:
        f.write(render_php)
    
    # index.js (editor)
    editor_js = _generate_slider_editor_js(bem_prefix)
    editor_js_path = os.path.join(slider_dir, 'index.js')
    with open(editor_js_path, 'w', encoding='utf-8') as f:
        f.write(editor_js)
    
    # style.css (frontend)
    style_css = _generate_slider_style_css(css_framework, bem_prefix)
    style_path = os.path.join(slider_dir, 'style.css')
    with open(style_path, 'w', encoding='utf-8') as f:
        f.write(style_css)
    
    # editor.css (editor)
    editor_css = _generate_slider_editor_css(bem_prefix)
    editor_css_path = os.path.join(slider_dir, 'editor.css')
    with open(editor_css_path, 'w', encoding='utf-8') as f:
        f.write(editor_css)

def create_hero_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Crea el bloque Hero."""
    hero_dir = os.path.join(blocks_dir, 'hero')
    os.makedirs(hero_dir, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": f"{bem_prefix}/hero",
        "version": "1.0.0",
        "title": "Hero",
        "category": f"{bem_prefix}-organisms",
        "icon": "cover-image",
        "description": "Bloque Hero administrable",
        "textdomain": bem_prefix,
        "render": "file:./render.php",
        "attributes": {
            "title": {"type": "string", "default": "Título hero"},
            "subtitle": {"type": "string", "default": "Subtítulo"},
            "buttonText": {"type": "string", "default": "Call to action"},
            "buttonUrl": {"type": "string", "default": "#"},
            "showButton": {"type": "boolean", "default": True},
            "showOverlay": {"type": "boolean", "default": True},
            "height": {"type": "string", "default": "70vh"},
            "align": {"type": "string", "default": "center"},
            "imageUrl": {"type": "string", "default": ""},
            "imageWebp": {"type": "string", "default": ""},
            "imageThumb": {"type": "string", "default": ""}
        }
    }
    block_json_path = os.path.join(hero_dir, 'block.json')
    with open(block_json_path, 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2)
    with open(os.path.join(hero_dir, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(_render_hero(css_framework, bem_prefix))
    with open(os.path.join(hero_dir, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* hero styles */")

def create_section_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Crea el bloque Section con prefijo BEM."""
    section_dir = os.path.join(blocks_dir, 'section')
    os.makedirs(section_dir, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": f"{bem_prefix}/section",
        "version": "1.0.0",
        "title": "Sección",
        "category": f"{bem_prefix}-organisms",
        "icon": "columns",
        "description": "Bloque de sección multipropósito",
        "textdomain": bem_prefix,
        "render": "file:./render.php",
        "attributes": {
            "variant": {"type": "string", "default": "default"},
            "title": {"type": "string", "default": "Sección"},
            "content": {"type": "string", "default": "Texto de ejemplo"},
            "columns": {"type": "number", "default": 2},
            "imageUrl": {"type": "string", "default": ""},
            "imageWebp": {"type": "string", "default": ""},
            "imageThumb": {"type": "string", "default": ""}
        }
    }
    block_json_path = os.path.join(section_dir, 'block.json')
    with open(block_json_path, 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2)
    with open(os.path.join(section_dir, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(_render_section(css_framework, bem_prefix))
    with open(os.path.join(section_dir, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* section styles */")

def create_cards_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Crea el bloque Cards."""
    cards_dir = os.path.join(blocks_dir, 'cards')
    os.makedirs(cards_dir, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": f"{bem_prefix}/cards",
        "version": "1.0.0",
        "title": "Cards",
        "category": f"{bem_prefix}-organisms",
        "icon": "grid-view",
        "description": "Bloque de tarjetas",
        "textdomain": bem_prefix,
        "render": "file:./render.php",
        "attributes": {
            "cards": {"type": "array", "default": []},
            "columns": {"type": "number", "default": 3},
            "gap": {"type": "number", "default": 16}
        }
    }
    block_json_path = os.path.join(cards_dir, 'block.json')
    with open(block_json_path, 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2)
    with open(os.path.join(cards_dir, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(_render_cards(css_framework, bem_prefix))
    with open(os.path.join(cards_dir, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* cards styles */")

def create_gallery_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Crea el bloque Gallery."""
    gallery_dir = os.path.join(blocks_dir, 'gallery')
    os.makedirs(gallery_dir, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": f"{bem_prefix}/gallery",
        "version": "1.0.0",
        "title": "Galería",
        "category": f"{bem_prefix}-organisms",
        "icon": "format-gallery",
        "description": "Bloque de galería",
        "textdomain": bem_prefix,
        "render": "file:./render.php",
        "attributes": {
            "images": {"type": "array", "default": []},
            "columns": {"type": "number", "default": 3},
            "gap": {"type": "number", "default": 12},
            "lightbox": {"type": "boolean", "default": False}
        }
    }
    block_json_path = os.path.join(gallery_dir, 'block.json')
    with open(block_json_path, 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2)
    with open(os.path.join(gallery_dir, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(_render_gallery(css_framework, bem_prefix))
    with open(os.path.join(gallery_dir, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* gallery styles */")

def create_text_image_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    dir_path = os.path.join(blocks_dir, 'text-image')
    os.makedirs(dir_path, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": f"{bem_prefix}/text-image",
        "version": "1.0.0",
        "title": "Texto + Imagen",
        "category": f"{bem_prefix}-organisms",
        "icon": "align-pull-left",
        "description": "Bloque de texto con imagen multipropósito",
        "textdomain": bem_prefix,
        "editorScript": "file:./index.js",
        "style": "file:./style.css",
        "attributes": {
            "layout": {"type": "string", "default": "image-left"},
            "title": {"type": "string", "default": "Título de sección"},
            "body": {"type": "string", "default": "Contenido de ejemplo"},
            "imageUrl": {"type": "string", "default": ""},
            "imageWebp": {"type": "string", "default": ""},
            "imageThumb": {"type": "string", "default": ""},
            "imageId": {"type": "number"},
            "bgStyle": {"type": "string", "default": "light"},
            "padding": {"type": "string", "default": "md"}
        }
    }
    with open(os.path.join(dir_path, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2, ensure_ascii=False)
    with open(os.path.join(dir_path, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(_render_simple_section(css_framework, "text-image", bem_prefix))
    with open(os.path.join(dir_path, 'index.js'), 'w', encoding='utf-8') as f:
        f.write(_editor_simple_section(bem_prefix))
    with open(os.path.join(dir_path, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* text-image styles */")

def create_sidebar_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    dir_path = os.path.join(blocks_dir, 'sidebar')
    os.makedirs(dir_path, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": f"{bem_prefix}/sidebar",
        "version": "1.0.0",
        "title": "Sidebar Dinámico",
        "category": f"{bem_prefix}-organisms",
        "icon": "menu",
        "description": "Sidebar administrable con enlaces y widgets",
        "textdomain": bem_prefix,
        "editorScript": "file:./index.js",
        "style": "file:./style.css",
        "attributes": {
            "title": {"type": "string", "default": "Sidebar"},
            "links": {"type": "array", "default": []},
            "showRecent": {"type": "boolean", "default": True},
            "showCategories": {"type": "boolean", "default": True},
            "showTags": {"type": "boolean", "default": True},
            "styleVariant": {"type": "string", "default": "light"},
            "padding": {"type": "string", "default": "md"},
            "border": {"type": "boolean", "default": False},
            "linkStyle": {"type": "string", "default": "normal"}
        }
    }
    with open(os.path.join(dir_path, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2, ensure_ascii=False)
    with open(os.path.join(dir_path, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(_render_sidebar(css_framework, bem_prefix))
    with open(os.path.join(dir_path, 'index.js'), 'w', encoding='utf-8') as f:
        f.write(_editor_sidebar(bem_prefix))
    with open(os.path.join(dir_path, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* sidebar styles */")

def create_search_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    dir_path = os.path.join(blocks_dir, 'search-extended')
    os.makedirs(dir_path, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": f"{bem_prefix}/search-extended",
        "version": "1.0.0",
        "title": "Buscador",
        "category": f"{bem_prefix}-organisms",
        "icon": "search",
        "description": "Buscador extendido",
        "textdomain": bem_prefix,
        "editorScript": "file:./index.js",
        "style": "file:./style.css",
        "attributes": {
            "size": {"type": "string", "default": "md"},
            "rounded": {"type": "boolean", "default": True},
            "buttonInside": {"type": "boolean", "default": True},
            "placeholder": {"type": "string", "default": "Buscar..."},
            "showIcon": {"type": "boolean", "default": True}
        }
    }
    with open(os.path.join(dir_path, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2, ensure_ascii=False)
    with open(os.path.join(dir_path, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(_render_search(css_framework, bem_prefix))
    with open(os.path.join(dir_path, 'index.js'), 'w', encoding='utf-8') as f:
        f.write(_editor_search(bem_prefix))
    with open(os.path.join(dir_path, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* search styles */")

def create_pagination_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    dir_path = os.path.join(blocks_dir, 'pagination')
    os.makedirs(dir_path, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": f"{bem_prefix}/pagination",
        "version": "1.0.0",
        "title": "Paginación",
        "category": f"{bem_prefix}-organisms",
        "icon": "controls-repeat",
        "description": "Bloque de paginación",
        "textdomain": bem_prefix,
        "editorScript": "file:./index.js",
        "style": "file:./style.css",
        "attributes": {
            "mode": {"type": "string", "default": "numbers"},
            "align": {"type": "string", "default": "center"},
            "size": {"type": "string", "default": "md"},
            "gap": {"type": "number", "default": 8},
            "showPageCount": {"type": "boolean", "default": False}
        }
    }
    with open(os.path.join(dir_path, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2, ensure_ascii=False)
    with open(os.path.join(dir_path, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(_render_pagination(css_framework, bem_prefix))
    with open(os.path.join(dir_path, 'index.js'), 'w', encoding='utf-8') as f:
        f.write(_editor_pagination(bem_prefix))
    with open(os.path.join(dir_path, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* pagination styles */")

def create_header_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    dir_path = os.path.join(blocks_dir, 'header')
    os.makedirs(dir_path, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": f"{bem_prefix}/header",
        "version": "1.0.0",
        "title": "Header",
        "category": f"{bem_prefix}-organisms",
        "icon": "admin-site",
        "description": "Header editable con logo, menú y CTA",
        "textdomain": bem_prefix,
        "editorScript": "file:./index.js",
        "style": "file:./style.css",
        "attributes": {
            "sticky": {"type": "boolean", "default": False},
            "transparent": {"type": "boolean", "default": False},
            "scrollChange": {"type": "boolean", "default": False},
            "height": {"type": "string", "default": "md"},
            "ctaText": {"type": "string", "default": "Contáctanos"},
            "ctaUrl": {"type": "string", "default": "#"},
            "ctaShow": {"type": "boolean", "default": True}
        }
    }
    with open(os.path.join(dir_path, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2, ensure_ascii=False)
    with open(os.path.join(dir_path, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(_render_header(css_framework, bem_prefix))
    with open(os.path.join(dir_path, 'index.js'), 'w', encoding='utf-8') as f:
        f.write(_editor_header(bem_prefix))
    with open(os.path.join(dir_path, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* header styles */")

def create_footer_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    dir_path = os.path.join(blocks_dir, 'footer')
    os.makedirs(dir_path, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": f"{bem_prefix}/footer",
        "version": "1.0.0",
        "title": "Footer",
        "category": f"{bem_prefix}-organisms",
        "icon": "editor-insertmore",
        "description": "Footer editable multicolumna",
        "textdomain": bem_prefix,
        "editorScript": "file:./index.js",
        "style": "file:./style.css",
        "attributes": {
            "columns": {"type": "number", "default": 3},
            "bg": {"type": "string", "default": "dark"},
            "legal": {"type": "string", "default": "© 2025. Todos los derechos reservados."},
            "links": {"type": "array", "default": []},
            "showSocial": {"type": "boolean", "default": True}
        }
    }
    with open(os.path.join(dir_path, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2, ensure_ascii=False)
    with open(os.path.join(dir_path, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(_render_footer(css_framework, bem_prefix))
    with open(os.path.join(dir_path, 'index.js'), 'w', encoding='utf-8') as f:
        f.write(_editor_footer(bem_prefix))
    with open(os.path.join(dir_path, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* footer styles */")

def create_form_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    dir_path = os.path.join(blocks_dir, 'form')
    os.makedirs(dir_path, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": f"{bem_prefix}/form",
        "version": "1.0.0",
        "title": "Formulario de Contacto",
        "category": f"{bem_prefix}-organisms",
        "icon": "email",
        "description": "Formulario nativo (nombre, email, teléfono, mensaje)",
        "textdomain": bem_prefix,
        "editorScript": "file:./index.js",
        "style": "file:./style.css",
        "render": "file:./render.php",
        "attributes": {
            "showPhone": {"type": "boolean", "default": True},
            "submitText": {"type": "string", "default": "Enviar"},
            "successMessage": {"type": "string", "default": "Mensaje enviado"},
            "errorMessage": {"type": "string", "default": "Ocurrió un error"},
            "endpoint": {"type": "string", "default": "/wp-json/img2html/v1/contact"}
        }
    }
    with open(os.path.join(dir_path, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2, ensure_ascii=False)
    with open(os.path.join(dir_path, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(_render_form(css_framework, bem_prefix))
    with open(os.path.join(dir_path, 'index.js'), 'w', encoding='utf-8') as f:
        f.write(_editor_form(bem_prefix))
    with open(os.path.join(dir_path, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* form styles */")

def create_menu_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    dir_path = os.path.join(blocks_dir, 'menu')
    os.makedirs(dir_path, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": f"{bem_prefix}/menu",
        "version": "1.0.0",
        "title": "Menú Avanzado",
        "category": f"{bem_prefix}-organisms",
        "icon": "menu",
        "description": "Menú desktop/mobile con CTA y redes",
        "textdomain": bem_prefix,
        "editorScript": "file:./index.js",
        "style": "file:./style.css",
        "render": "file:./render.php",
        "attributes": {
            "sticky": {"type": "boolean", "default": False},
            "transparent": {"type": "boolean", "default": False},
            "ctaText": {"type": "string", "default": "Contáctanos"},
            "ctaUrl": {"type": "string", "default": "#"},
            "ctaShow": {"type": "boolean", "default": True},
            "showSocial": {"type": "boolean", "default": False}
        }
    }
    with open(os.path.join(dir_path, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2, ensure_ascii=False)
    with open(os.path.join(dir_path, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(_render_menu(css_framework, bem_prefix))
    with open(os.path.join(dir_path, 'index.js'), 'w', encoding='utf-8') as f:
        f.write(_editor_menu(bem_prefix))
    with open(os.path.join(dir_path, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* menu styles */")

# ========================================
# FUNCIONES WRAPPER PARA ESTRUCTURA ATÓMICA
# Estas funciones crean organismos en organisms_dir (blocks/organisms/)
# ========================================

def create_organism_slider(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Wrapper para crear slider en estructura atómica."""
    create_slider_block(organisms_dir, css_framework, bem_prefix)

def create_organism_hero(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Wrapper para crear hero en estructura atómica."""
    create_hero_block(organisms_dir, css_framework, bem_prefix)

def create_organism_section(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Wrapper para crear section en estructura atómica."""
    create_section_block(organisms_dir, css_framework, bem_prefix)

def create_organism_cards_grid(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Wrapper para crear cards grid en estructura atómica."""
    create_cards_block(organisms_dir, css_framework, bem_prefix)

def create_organism_gallery(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Wrapper para crear gallery en estructura atómica."""
    create_gallery_block(organisms_dir, css_framework, bem_prefix)

def create_organism_text_image(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Wrapper para crear text-image en estructura atómica."""
    create_text_image_block(organisms_dir, css_framework, bem_prefix)

def create_organism_sidebar(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Wrapper para crear sidebar en estructura atómica."""
    create_sidebar_block(organisms_dir, css_framework, bem_prefix)

def create_organism_search(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Wrapper para crear search en estructura atómica."""
    create_search_block(organisms_dir, css_framework, bem_prefix)

def create_organism_pagination(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Wrapper para crear pagination en estructura atómica."""
    create_pagination_block(organisms_dir, css_framework, bem_prefix)

def create_organism_header(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Wrapper para crear header en estructura atómica."""
    create_header_block(organisms_dir, css_framework, bem_prefix)

def create_organism_footer(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Wrapper para crear footer en estructura atómica."""
    create_footer_block(organisms_dir, css_framework, bem_prefix)

def create_organism_form(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Wrapper para crear form en estructura atómica."""
    create_form_block(organisms_dir, css_framework, bem_prefix)

def create_organism_menu(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Wrapper para crear menu en estructura atómica."""
    create_menu_block(organisms_dir, css_framework, bem_prefix)

def create_organism_cta(organisms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """
    Crea el organismo CTA (Call to Action) completo.
    Combina heading, paragraph, button atoms.
    """
    cta_dir = os.path.join(organisms_dir, 'cta')
    os.makedirs(cta_dir, exist_ok=True)
    
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": f"{bem_prefix}/organism-cta",
        "version": "1.0.0",
        "title": "CTA (Call to Action)",
        "category": f"{bem_prefix}-organisms",
        "icon": "megaphone",
        "description": "Bloque CTA completo con título, descripción y botones",
        "textdomain": bem_prefix,
        "editorScript": "file:./index.js",
        "style": "file:./style.css",
        "render": "file:./render.php",
        "attributes": {
            "title": {"type": "string", "default": "¿Listo para comenzar?"},
            "description": {"type": "string", "default": "Únete a nosotros hoy mismo"},
            "primaryButtonText": {"type": "string", "default": "Comenzar"},
            "primaryButtonUrl": {"type": "string", "default": "#"},
            "secondaryButtonText": {"type": "string", "default": ""},
            "secondaryButtonUrl": {"type": "string", "default": "#"},
            "showSecondaryButton": {"type": "boolean", "default": False},
            "backgroundStyle": {"type": "string", "default": "primary"},
            "alignment": {"type": "string", "default": "center"}
        },
        "supports": {
            "align": ["wide", "full"],
            "html": False,
            "color": {
                "background": True,
                "text": True,
                "gradients": True
            },
            "spacing": {
                "padding": True,
                "margin": True
            }
        }
    }
    
    with open(os.path.join(cta_dir, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2, ensure_ascii=False)
    
    # Render PHP
    render_php = f"""<?php
$title = $attributes['title'] ?? '¿Listo para comenzar?';
$description = $attributes['description'] ?? 'Únete a nosotros hoy mismo';
$primary_text = $attributes['primaryButtonText'] ?? 'Comenzar';
$primary_url = $attributes['primaryButtonUrl'] ?? '#';
$secondary_text = $attributes['secondaryButtonText'] ?? '';
$secondary_url = $attributes['secondaryButtonUrl'] ?? '#';
$show_secondary = $attributes['showSecondaryButton'] ?? false;
$bg_style = $attributes['backgroundStyle'] ?? 'primary';
$alignment = $attributes['alignment'] ?? 'center';

$align_class = $alignment === 'left' ? '{bem_prefix}-organism-cta--align-left' : 
               ($alignment === 'right' ? '{bem_prefix}-organism-cta--align-right' : '{bem_prefix}-organism-cta--align-center');
?>
<div class="{bem_prefix}-organism-cta {bem_prefix}-organism-cta--<?php echo esc_attr($bg_style); ?> <?php echo esc_attr($align_class); ?>">
    <div class="{bem_prefix}-organism-cta__content">
        <?php if ($title): ?>
            <h2 class="{bem_prefix}-organism-cta__title"><?php echo esc_html($title); ?></h2>
        <?php endif; ?>
        
        <?php if ($description): ?>
            <p class="{bem_prefix}-organism-cta__description"><?php echo esc_html($description); ?></p>
        <?php endif; ?>
        
        <div class="{bem_prefix}-organism-cta__actions">
            <a href="<?php echo esc_url($primary_url); ?>" class="{bem_prefix}-organism-cta__button {bem_prefix}-organism-cta__button--primary">
                <?php echo esc_html($primary_text); ?>
            </a>
            <?php if ($show_secondary && $secondary_text): ?>
                <a href="<?php echo esc_url($secondary_url); ?>" class="{bem_prefix}-organism-cta__button {bem_prefix}-organism-cta__button--secondary">
                    <?php echo esc_html($secondary_text); ?>
                </a>
            <?php endif; ?>
        </div>
    </div>
</div>
"""
    
    with open(os.path.join(cta_dir, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(render_php)
    
    # Editor JS
    editor_js = f"""import {{ registerBlockType }} from '@wordpress/blocks';
import {{ InspectorControls, useBlockProps, RichText }} from '@wordpress/block-editor';
import {{ PanelBody, TextControl, ToggleControl, SelectControl }} from '@wordpress/components';
import {{ __ }} from '@wordpress/i18n';

registerBlockType('{bem_prefix}/organism-cta', {{
    edit: ({{ attributes, setAttributes }}) => {{
        const {{
            title,
            description,
            primaryButtonText,
            primaryButtonUrl,
            secondaryButtonText,
            secondaryButtonUrl,
            showSecondaryButton,
            backgroundStyle,
            alignment
        }} = attributes;
        
        const blockProps = useBlockProps({{
            className: '{bem_prefix}-organism-cta-editor'
        }});
        
        return (
            <div {{...blockProps}}>
                <InspectorControls>
                    <PanelBody title={{__('Configuración CTA', 'img2html')}} initialOpen={{true}}>
                        <TextControl
                            label={{__('Título', 'img2html')}}
                            value={{title}}
                            onChange={{(value) => setAttributes({{ title: value }})}}
                        />
                        <TextControl
                            label={{__('Descripción', 'img2html')}}
                            value={{description}}
                            onChange={{(value) => setAttributes({{ description: value }})}}
                        />
                        <TextControl
                            label={{__('Texto botón principal', 'img2html')}}
                            value={{primaryButtonText}}
                            onChange={{(value) => setAttributes({{ primaryButtonText: value }})}}
                        />
                        <TextControl
                            label={{__('URL botón principal', 'img2html')}}
                            value={{primaryButtonUrl}}
                            onChange={{(value) => setAttributes({{ primaryButtonUrl: value }})}}
                        />
                        <ToggleControl
                            label={{__('Mostrar botón secundario', 'img2html')}}
                            checked={{showSecondaryButton}}
                            onChange={{(value) => setAttributes({{ showSecondaryButton: value }})}}
                        />
                        {{showSecondaryButton && (
                            <>
                                <TextControl
                                    label={{__('Texto botón secundario', 'img2html')}}
                                    value={{secondaryButtonText}}
                                    onChange={{(value) => setAttributes({{ secondaryButtonText: value }})}}
                                />
                                <TextControl
                                    label={{__('URL botón secundario', 'img2html')}}
                                    value={{secondaryButtonUrl}}
                                    onChange={{(value) => setAttributes({{ secondaryButtonUrl: value }})}}
                                />
                            </>
                        )}}
                        <SelectControl
                            label={{__('Estilo de fondo', 'img2html')}}
                            value={{backgroundStyle}}
                            options={{[
                                {{ label: __('Primario', 'img2html'), value: 'primary' }},
                                {{ label: __('Secundario', 'img2html'), value: 'secondary' }},
                                {{ label: __('Oscuro', 'img2html'), value: 'dark' }},
                                {{ label: __('Claro', 'img2html'), value: 'light' }}
                            ]}}
                            onChange={{(value) => setAttributes({{ backgroundStyle: value }})}}
                        />
                        <SelectControl
                            label={{__('Alineación', 'img2html')}}
                            value={{alignment}}
                            options={{[
                                {{ label: __('Izquierda', 'img2html'), value: 'left' }},
                                {{ label: __('Centro', 'img2html'), value: 'center' }},
                                {{ label: __('Derecha', 'img2html'), value: 'right' }}
                            ]}}
                            onChange={{(value) => setAttributes({{ alignment: value }})}}
                        />
                    </PanelBody>
                </InspectorControls>
                <div className="{bem_prefix}-organism-cta-editor__preview">
                    <h2>{{title}}</h2>
                    <p>{{description}}</p>
                    <div>
                        <button>{{primaryButtonText}}</button>
                        {{showSecondaryButton && <button>{{secondaryButtonText}}</button>}}
                    </div>
                </div>
            </div>
        );
    }},
    save: () => null
}});
"""
    
    with open(os.path.join(cta_dir, 'index.js'), 'w', encoding='utf-8') as f:
        f.write(editor_js)
    
    # Style CSS con BEM
    from .helpers import generate_bem_css
    style_css = generate_bem_css(
        block_name='organism-cta',
        bem_prefix=bem_prefix,
        css_framework=css_framework,
        elements=[
            ('content', '    max-width: 800px; margin: 0 auto; padding: 2rem;'),
            ('title', '    font-size: 2rem; font-weight: bold; margin-bottom: 1rem;'),
            ('description', '    font-size: 1.125rem; margin-bottom: 2rem;'),
            ('actions', '    display: flex; gap: 1rem; justify-content: center;'),
            ('button', '    padding: 0.75rem 2rem; border-radius: 4px; text-decoration: none; display: inline-block;')
        ],
        modifiers={
            'cta': ['primary', 'secondary', 'dark', 'light', 'align-left', 'align-center', 'align-right'],
            'button': ['primary', 'secondary']
        },
        base_styles='''    padding: 3rem 1rem;
    text-align: center;
    border-radius: 8px;'''
    )
    
    with open(os.path.join(cta_dir, 'style.css'), 'w', encoding='utf-8') as f:
        f.write(style_css)

__all__ = [
    'create_slider_block',
    'create_hero_block',
    'create_section_block',
    'create_cards_block',
    'create_gallery_block',
    'create_text_image_block',
    'create_sidebar_block',
    'create_search_block',
    'create_pagination_block',
    'create_header_block',
    'create_footer_block',
    'create_form_block',
    'create_menu_block',
    'create_organism_slider',
    'create_organism_hero',
    'create_organism_section',
    'create_organism_cards_grid',
    'create_organism_gallery',
    'create_organism_text_image',
    'create_organism_sidebar',
    'create_organism_search',
    'create_organism_pagination',
    'create_organism_header',
    'create_organism_footer',
    'create_organism_form',
    'create_organism_menu',
    'create_organism_cta',
]
