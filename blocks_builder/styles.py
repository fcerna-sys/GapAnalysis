"""
Módulo para funciones de generación de CSS de bloques.
Contiene todas las funciones _generate_*_style_css y _generate_*_editor_css.
Todas las funciones se importan desde blocks_builder_backup.py para mantener el código completo.
"""
# Importar todas las funciones de estilos desde el backup
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

# Importar todas las funciones de estilos
_generate_slider_style_css = getattr(_backup_module, '_generate_slider_style_css', None)
_generate_slider_editor_css = getattr(_backup_module, '_generate_slider_editor_css', None)

# Crear stubs si alguna función no existe
if _generate_slider_style_css is None:
    def _generate_slider_style_css(css_framework: str) -> str:
        return "/* Slider styles */"

if _generate_slider_editor_css is None:
    def _generate_slider_editor_css() -> str:
        return "/* Slider editor styles */"

__all__ = [
    '_generate_slider_style_css',
    '_generate_slider_editor_css',
]

