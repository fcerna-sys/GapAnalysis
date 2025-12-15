"""
Mejoras de UX para editores JavaScript.
Añade placeholders, instrucciones y ayuda contextual.
"""
from typing import Dict


def enhance_editor_js_with_placeholders(editor_js: str, block_type: str, block_name: str, bem_prefix: str) -> str:
    """
    Mejora el código JavaScript del editor añadiendo placeholders y ayuda.
    """
    from .editor_ux import get_editor_placeholder, get_block_instructions
    
    # Añadir instrucciones al inicio del componente si no existen
    if '💡 Tip:' not in editor_js and 'help=' not in editor_js:
        instructions = get_block_instructions(block_type, block_name)
        if instructions:
            # Buscar el return del componente y añadir instrucciones antes
            if 'return (' in editor_js:
                parts = editor_js.split('return (', 1)
                if len(parts) == 2:
                    instruction_comment = f"""
                    // {instructions}
                    """
                    editor_js = parts[0] + instruction_comment + 'return (' + parts[1]
    
    return editor_js


def add_pattern_instructions(pattern_content: str, pattern_slug: str, bem_prefix: str) -> str:
    """
    Añade instrucciones dentro de los patterns para guiar al usuario.
    """
    instructions_map = {
        'header-global': '💡 Este header se sincroniza en todas las páginas. Edítalo desde Editor del Sitio → Patterns.',
        'footer-global': '💡 Este footer se sincroniza en todas las páginas. Edítalo desde Editor del Sitio → Patterns.',
        'cta-primary': '💡 Usa este CTA en páginas de landing o al final de contenido importante. Limita a 1-2 CTAs por página.',
        'hero-section': '💡 Ideal para página principal. Mantén el texto conciso y el CTA visible.',
        'cards-grid': '💡 Configura 2-4 columnas según el espacio. En móvil se adapta automáticamente.',
        'testimonials-section': '💡 Usa 2-3 testimonios máximo. Incluye nombre y cargo del autor cuando sea posible.',
    }
    
    instruction = instructions_map.get(pattern_slug.replace(f'{bem_prefix}-', ''), '')
    
    if instruction and instruction not in pattern_content:
        # Añadir como comentario HTML al inicio
        instruction_html = f'<!-- {instruction} -->\n'
        pattern_content = instruction_html + pattern_content
    
    return pattern_content




