"""
Módulo para funciones de generación de CSS de bloques.
Contiene TODAS las funciones _generate_*_style_css y _generate_*_editor_css.
Código completo migrado desde blocks_builder_backup.py
"""


def _generate_slider_style_css(css_framework: str) -> str:
    """Genera los estilos CSS del slider según el framework."""
    if css_framework == 'tailwind':
        return """/* Estilos del Slider - Tailwind CSS */
/* La mayoría de estilos se manejan con clases de Tailwind */
"""
    elif css_framework == 'bootstrap':
        return """/* Estilos del Slider - Bootstrap 5 */
/* Los estilos principales vienen de Bootstrap */
.img2html-slider .carousel-overlay {
    z-index: 1;
}
"""
    else:
        return """/* Estilos del Slider - CSS Propio */
.img2html-slider {
    position: relative;
    overflow: hidden;
}

.img2html-slider .slider-wrapper {
    position: relative;
    width: 100%;
    height: 100%;
}

.img2html-slider .slide {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    transition: opacity 0.5s ease-in-out;
}

.img2html-slider .slide.active {
    opacity: 1;
    z-index: 1;
}

.img2html-slider .slider-arrow {
    cursor: pointer;
    z-index: 10;
}

.img2html-slider .slider-dots {
    z-index: 10;
}

.img2html-slider .dot {
    cursor: pointer;
    border: none;
    background: rgba(255, 255, 255, 0.5);
}

.img2html-slider .dot.active {
    background: rgba(255, 255, 255, 1);
}
"""

def _generate_slider_editor_css() -> str:
    """Genera los estilos CSS del editor."""
    return """/* Estilos del Editor del Slider */
.img2html-slider-editor {
    border: 2px dashed #ccc;
    padding: 20px;
    margin: 20px 0;
}

.slider-editor-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.slider-empty-state {
    text-align: center;
    padding: 40px;
    color: #666;
}

.slider-slides-list {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.slider-slide-editor {
    border: 1px solid #ddd;
    padding: 15px;
    border-radius: 4px;
    background: #f9f9f9;
}

.slide-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}

.slide-actions {
    display: flex;
    gap: 5px;
}

.slide-preview {
    max-width: 100%;
    height: auto;
    margin: 10px 0;
    border-radius: 4px;
}
"""

__all__ = [
    '_generate_slider_style_css',
    '_generate_slider_editor_css',
]
