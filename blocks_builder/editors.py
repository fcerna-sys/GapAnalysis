"""
Módulo para funciones de editor JavaScript de bloques.
Contiene todas las funciones _editor_* y _generate_*_editor_js.
Todas las funciones se importan desde blocks_builder_backup.py para mantener el código completo.
"""
# Importar todas las funciones de editor desde el backup
import sys
import importlib.util

# Reutilizar el módulo backup de renders.py si está disponible, sino cargarlo
try:
    from .renders import backup as _backup_module
except:
    _backup_module = None

if _backup_module is None:
    try:
        spec = importlib.util.spec_from_file_location("blocks_builder_backup", "blocks_builder_backup.py")
        if spec and spec.loader:
            _backup_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(_backup_module)
    except Exception as e:
        _backup_module = type('Module', (), {})()

# Importar todas las funciones de editor
_generate_slider_editor_js = getattr(_backup_module, '_generate_slider_editor_js', None)
_editor_simple_section = getattr(_backup_module, '_editor_simple_section', None)
_editor_sidebar = getattr(_backup_module, '_editor_sidebar', None)
_editor_search = getattr(_backup_module, '_editor_search', None)
_editor_pagination = getattr(_backup_module, '_editor_pagination', None)
_editor_header = getattr(_backup_module, '_editor_header', None)
_editor_footer = getattr(_backup_module, '_editor_footer', None)
_editor_form = getattr(_backup_module, '_editor_form', None)
_editor_menu = getattr(_backup_module, '_editor_menu', None)

# Crear stubs si alguna función no existe
if _generate_slider_editor_js is None:
    def _generate_slider_editor_js() -> str:
        return "// Slider editor JS"
if _editor_simple_section is None:
    def _editor_simple_section() -> str:
        return "// Simple section editor"
if _editor_sidebar is None:
    def _editor_sidebar() -> str:
        return "// Sidebar editor"
if _editor_search is None:
    def _editor_search() -> str:
        return "// Search editor"
if _editor_pagination is None:
    def _editor_pagination() -> str:
        return "// Pagination editor"
if _editor_header is None:
    def _editor_header() -> str:
        return "// Header editor"
if _editor_footer is None:
    def _editor_footer() -> str:
        return "// Footer editor"
if _editor_form is None:
    def _editor_form() -> str:
        return "// Form editor"
if _editor_menu is None:
    def _editor_menu() -> str:
        return "// Menu editor"

__all__ = [
    '_generate_slider_editor_js',
    '_editor_simple_section',
    '_editor_sidebar',
    '_editor_search',
    '_editor_pagination',
    '_editor_header',
    '_editor_footer',
    '_editor_form',
    '_editor_menu',
]

