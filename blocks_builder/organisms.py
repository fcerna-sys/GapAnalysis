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
    """
    slider_dir = os.path.join(blocks_dir, 'slider')
    os.makedirs(slider_dir, exist_ok=True)
    
    # block.json
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": "img2html/slider",
        "version": "1.0.0",
        "title": "Slider",
        "category": "img2html",
        "icon": "slides",
        "description": "Slider administrable con múltiples diapositivas",
        "keywords": ["slider", "carousel", "slideshow"],
        "textdomain": "img2html",
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
    editor_js = _generate_slider_editor_js()
    editor_js_path = os.path.join(slider_dir, 'index.js')
    with open(editor_js_path, 'w', encoding='utf-8') as f:
        f.write(editor_js)
    
    # style.css (frontend)
    style_css = _generate_slider_style_css(css_framework)
    style_path = os.path.join(slider_dir, 'style.css')
    with open(style_path, 'w', encoding='utf-8') as f:
        f.write(style_css)
    
    # editor.css (editor)
    editor_css = _generate_slider_editor_css()
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
        "name": "img2html/hero",
        "version": "1.0.0",
        "title": "Hero",
        "category": "img2html",
        "icon": "cover-image",
        "description": "Bloque Hero administrable",
        "textdomain": "img2html",
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
        "name": "img2html/section",
        "version": "1.0.0",
        "title": "Sección",
        "category": "img2html",
        "icon": "columns",
        "description": "Bloque de sección multipropósito",
        "textdomain": "img2html",
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
        "name": "img2html/cards",
        "version": "1.0.0",
        "title": "Cards",
        "category": "img2html",
        "icon": "grid-view",
        "description": "Bloque de tarjetas",
        "textdomain": "img2html",
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
        "name": "img2html/gallery",
        "version": "1.0.0",
        "title": "Galería",
        "category": "img2html",
        "icon": "format-gallery",
        "description": "Bloque de galería",
        "textdomain": "img2html",
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
        "name": "img2html/text-image",
        "version": "1.0.0",
        "title": "Texto + Imagen",
        "category": "img2html",
        "icon": "align-pull-left",
        "description": "Bloque de texto con imagen multipropósito",
        "textdomain": "img2html",
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
        f.write(_editor_simple_section())
    with open(os.path.join(dir_path, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* text-image styles */")

def create_sidebar_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    dir_path = os.path.join(blocks_dir, 'sidebar')
    os.makedirs(dir_path, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": "img2html/sidebar",
        "version": "1.0.0",
        "title": "Sidebar Dinámico",
        "category": "img2html",
        "icon": "menu",
        "description": "Sidebar administrable con enlaces y widgets",
        "textdomain": "img2html",
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
        f.write(_editor_sidebar())
    with open(os.path.join(dir_path, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* sidebar styles */")

def create_search_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    dir_path = os.path.join(blocks_dir, 'search-extended')
    os.makedirs(dir_path, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": "img2html/search-extended",
        "version": "1.0.0",
        "title": "Buscador",
        "category": "img2html",
        "icon": "search",
        "description": "Buscador extendido",
        "textdomain": "img2html",
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
        f.write(_editor_search())
    with open(os.path.join(dir_path, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* search styles */")

def create_pagination_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    dir_path = os.path.join(blocks_dir, 'pagination')
    os.makedirs(dir_path, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": "img2html/pagination",
        "version": "1.0.0",
        "title": "Paginación",
        "category": "img2html",
        "icon": "controls-repeat",
        "description": "Bloque de paginación",
        "textdomain": "img2html",
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
        f.write(_editor_pagination())
    with open(os.path.join(dir_path, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* pagination styles */")

def create_header_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    dir_path = os.path.join(blocks_dir, 'header')
    os.makedirs(dir_path, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": "img2html/header",
        "version": "1.0.0",
        "title": "Header",
        "category": "img2html",
        "icon": "admin-site",
        "description": "Header editable con logo, menú y CTA",
        "textdomain": "img2html",
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
        f.write(_editor_header())
    with open(os.path.join(dir_path, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* header styles */")

def create_footer_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    dir_path = os.path.join(blocks_dir, 'footer')
    os.makedirs(dir_path, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": "img2html/footer",
        "version": "1.0.0",
        "title": "Footer",
        "category": "img2html",
        "icon": "editor-insertmore",
        "description": "Footer editable multicolumna",
        "textdomain": "img2html",
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
        f.write(_editor_footer())
    with open(os.path.join(dir_path, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* footer styles */")

def create_form_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    dir_path = os.path.join(blocks_dir, 'form')
    os.makedirs(dir_path, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": "img2html/form",
        "version": "1.0.0",
        "title": "Formulario de Contacto",
        "category": "img2html",
        "icon": "email",
        "description": "Formulario nativo (nombre, email, teléfono, mensaje)",
        "textdomain": "img2html",
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
        f.write(_editor_form())
    with open(os.path.join(dir_path, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* form styles */")

def create_menu_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    dir_path = os.path.join(blocks_dir, 'menu')
    os.makedirs(dir_path, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": "img2html/menu",
        "version": "1.0.0",
        "title": "Menú Avanzado",
        "category": "img2html",
        "icon": "menu",
        "description": "Menú desktop/mobile con CTA y redes",
        "textdomain": "img2html",
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
        f.write(_editor_menu())
    with open(os.path.join(dir_path, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* menu styles */")

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
]
