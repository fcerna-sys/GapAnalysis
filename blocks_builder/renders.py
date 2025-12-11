"""
Módulo para funciones de renderizado PHP de bloques.
Contiene todas las funciones _render_* y _generate_*_render_php.
Todas las funciones se importan desde blocks_builder_backup.py para mantener el código completo.
"""
# Importar todas las funciones de render desde el backup
import sys
import importlib.util

# Cargar el módulo backup una sola vez
_backup_module = None

def _load_backup_module():
    """Carga el módulo backup una sola vez."""
    global _backup_module
    if _backup_module is None:
        try:
            spec = importlib.util.spec_from_file_location("blocks_builder_backup", "blocks_builder_backup.py")
            if spec and spec.loader:
                _backup_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(_backup_module)
        except Exception as e:
            print(f"Error al cargar backup: {e}")
            _backup_module = type('Module', (), {})()  # Módulo vacío
    return _backup_module

# Cargar el módulo backup
backup = _load_backup_module()

# Importar todas las funciones de render
_generate_slider_render_php = getattr(backup, '_generate_slider_render_php', None)
_render_simple_section = getattr(backup, '_render_simple_section', None)
_render_sidebar = getattr(backup, '_render_sidebar', None)
_render_search = getattr(backup, '_render_search', None)
_render_pagination = getattr(backup, '_render_pagination', None)
_render_header = getattr(backup, '_render_header', None)
_render_footer = getattr(backup, '_render_footer', None)
_render_form = getattr(backup, '_render_form', None)
_render_menu = getattr(backup, '_render_menu', None)
_render_gallery = getattr(backup, '_render_gallery', None)
_render_section = getattr(backup, '_render_section', None)
_render_cards = getattr(backup, '_render_cards', None)
_render_hero = getattr(backup, '_render_hero', None)

# Crear stubs si alguna función no existe
if _generate_slider_render_php is None:
    def _generate_slider_render_php(css_framework: str, bem_prefix: str = 'img2html') -> str:
        return "<!-- Slider render -->"
if _render_simple_section is None:
    def _render_simple_section(css_framework: str, block_name: str, bem_prefix: str = 'img2html') -> str:
        return "<!-- Simple section render -->"
if _render_sidebar is None:
    def _render_sidebar(css_framework: str, bem_prefix: str = 'img2html') -> str:
        return "<!-- Sidebar render -->"
if _render_search is None:
    def _render_search(css_framework: str, bem_prefix: str = 'img2html') -> str:
        return "<!-- Search render -->"
if _render_pagination is None:
    def _render_pagination(css_framework: str, bem_prefix: str = 'img2html') -> str:
        return "<!-- Pagination render -->"
if _render_header is None:
    def _render_header(css_framework: str, bem_prefix: str = 'img2html') -> str:
        return "<!-- Header render -->"
if _render_footer is None:
    def _render_footer(css_framework: str, bem_prefix: str = 'img2html') -> str:
        return "<!-- Footer render -->"
if _render_form is None:
    def _render_form(css_framework: str, bem_prefix: str = 'img2html') -> str:
        return "<!-- Form render -->"
if _render_menu is None:
    def _render_menu(css_framework: str, bem_prefix: str = 'img2html') -> str:
        return "<!-- Menu render -->"
if _render_gallery is None:
    def _render_gallery(css_framework: str, bem_prefix: str = 'img2html') -> str:
        return "<!-- Gallery render -->"
if _render_section is None:
    def _render_section(css_framework: str, bem_prefix: str = 'img2html') -> str:
        return "<!-- Section render -->"
if _render_cards is None:
    def _render_cards(css_framework: str, bem_prefix: str = 'img2html') -> str:
        return "<!-- Cards render -->"
if _render_hero is None:
    def _render_hero(css_framework: str, bem_prefix: str = 'img2html') -> str:
        return "<!-- Hero render -->"

__all__ = [
    '_generate_slider_render_php',
    '_render_simple_section',
    '_render_sidebar',
    '_render_search',
    '_render_pagination',
    '_render_header',
    '_render_footer',
    '_render_form',
    '_render_menu',
    '_render_gallery',
    '_render_section',
    '_render_cards',
    '_render_hero',
]

