"""
Sistema de mejora de UX en el editor de WordPress (Gutenberg).
Añade descripciones, placeholders, restricciones y guías.
"""
from typing import Dict, Optional, List


def enhance_block_json_ux(block_json: Dict, block_type: str, block_name: str, bem_prefix: str) -> Dict:
    """
    Mejora el block.json con UX avanzada:
    - Descripciones detalladas
    - Placeholders
    - Restricciones de supports
    - Instrucciones
    """
    # Mejorar descripción
    enhanced_description = _get_enhanced_description(block_type, block_name, block_json.get('description', ''))
    block_json['description'] = enhanced_description
    
    # Añadir ejemplo/placeholder
    if 'example' not in block_json:
        block_json['example'] = _get_block_example(block_type, block_name, block_json.get('attributes', {}))
    
    # Mejorar supports con restricciones
    if 'supports' not in block_json:
        block_json['supports'] = {}
    
    supports = block_json['supports']
    _apply_support_restrictions(supports, block_type, block_name)
    
    # Añadir instrucciones en attributes
    attributes = block_json.get('attributes', {})
    _enhance_attributes_with_instructions(attributes, block_type, block_name)
    block_json['attributes'] = attributes
    
    # Añadir keywords si no existen
    if 'keywords' not in block_json:
        block_json['keywords'] = _get_block_keywords(block_type, block_name)
    
    return block_json


def _get_enhanced_description(block_type: str, block_name: str, current_desc: str) -> str:
    """Obtiene descripción mejorada con instrucciones."""
    descriptions = {
        'atom-button': 'Botón básico reutilizable. Usa para acciones principales, CTAs o navegación. Elige el estilo (primary/secondary/outline) según la importancia de la acción.',
        'atom-heading': 'Título con niveles configurables (h1-h6). Usa h1 solo una vez por página. Mantén jerarquía clara: h1 > h2 > h3.',
        'atom-input': 'Campo de entrada para formularios. Incluye validación automática y placeholder configurable.',
        'atom-image': 'Imagen optimizada con lazy loading. Siempre añade texto alternativo para accesibilidad. Usa imágenes optimizadas (WebP recomendado).',
        'molecule-card': 'Tarjeta que combina imagen, título, texto y botón opcional. Ideal para mostrar servicios, productos o características.',
        'molecule-testimonial': 'Testimonio con cita, autor e imagen opcional. Usa para mostrar opiniones de clientes o usuarios.',
        'organism-slider': 'Slider completo con múltiples diapositivas. Recomendado: 3-5 slides máximo. Usa imágenes optimizadas. Configura autoplay solo si es necesario.',
        'organism-hero': 'Sección hero para página principal o landing. Incluye título, subtítulo, imagen de fondo y CTA. Mantén el texto conciso y el CTA visible.',
        'organism-section': 'Sección multipropósito con layouts configurables. Usa para agrupar contenido relacionado. Elige entre container o full-width según necesidad.',
        'organism-cards-grid': 'Grid de tarjetas. Configura el número de columnas según el espacio disponible. En móvil se adapta automáticamente a 1 columna.',
        'organism-header': 'Header global del sitio. Se sincroniza en todas las páginas. Incluye logo, menú y botones opcionales.',
        'organism-footer': 'Footer global del sitio. Se sincroniza en todas las páginas. Organiza en columnas según necesidad.',
        'organism-form': 'Formulario de contacto completo. Valida campos en frontend y backend. Configura endpoint de envío según necesidad.',
        'organism-cta': 'Call to Action completo. Usa en páginas de landing o al final de contenido importante. Limita a 1-2 CTAs por página.',
    }
    
    key = f"{block_type}-{block_name}"
    return descriptions.get(key, current_desc or f"Componente {block_type} para {block_name.replace('-', ' ')}.")


def _get_block_example(block_type: str, block_name: str, attributes: Dict) -> Dict:
    """Genera ejemplo para el block.json."""
    examples = {
        'atom-button': {
            'attributes': {
                'text': 'Haz clic aquí',
                'url': '#',
                'variant': 'primary'
            }
        },
        'atom-heading': {
            'attributes': {
                'text': 'Título de ejemplo',
                'level': 2
            }
        },
        'organism-slider': {
            'attributes': {
                'showSlider': True,
                'autoplay': True,
                'slides': [
                    {
                        'title': 'Slide 1',
                        'subtitle': 'Descripción del slide',
                        'imageUrl': ''
                    }
                ]
            }
        },
        'organism-hero': {
            'attributes': {
                'title': 'Título Principal',
                'subtitle': 'Subtítulo descriptivo',
                'buttonText': 'Comenzar',
                'buttonUrl': '#'
            }
        },
        'organism-cta': {
            'attributes': {
                'title': '¿Listo para empezar?',
                'description': 'Únete a nosotros hoy mismo',
                'primaryButtonText': 'Comenzar ahora'
            }
        },
    }
    
    key = f"{block_type}-{block_name}"
    return examples.get(key, {'attributes': {}})


def _apply_support_restrictions(supports: Dict, block_type: str, block_name: str):
    """Aplica restricciones a supports para evitar que se rompa el diseño."""
    # Restricciones por tipo de bloque
    restrictions = {
        'atom-button': {
            'align': False,  # Los botones no deben alinearse
            'color': {
                'background': False,  # Usa variant en lugar de color de fondo
                'text': False,
                'gradients': False
            },
            'spacing': {
                'margin': True,
                'padding': False  # Padding controlado por size
            },
            'typography': {
                'fontSize': False,  # Tamaño controlado por size
                'fontFamily': False,
                'fontWeight': False,
                'fontStyle': False,
                'textTransform': False,
                'lineHeight': False
            }
        },
        'atom-heading': {
            'align': ['left', 'center', 'right'],  # Solo estas alineaciones
            'color': {
                'text': True,
                'background': False,
                'gradients': False
            },
            'spacing': {
                'margin': True,
                'padding': False
            },
            'typography': {
                'fontSize': True,  # Permitir tamaño
                'fontFamily': False,  # Usar familia global
                'fontWeight': True,
                'fontStyle': False,
                'textTransform': False,
                'lineHeight': True
            }
        },
        'organism-slider': {
            'align': ['wide', 'full'],  # Solo wide y full
            'html': False,
            'color': False,  # No permitir colores (usa overlay)
            'spacing': {
                'margin': True,
                'padding': False
            }
        },
        'organism-hero': {
            'align': ['wide', 'full'],
            'html': False,
            'color': {
                'text': True,
                'background': False,  # Usa imagen de fondo
                'gradients': False
            },
            'spacing': {
                'margin': False,
                'padding': True
            }
        },
        'organism-section': {
            'align': ['wide', 'full'],
            'html': False,
            'color': {
                'text': True,
                'background': True,
                'gradients': True
            },
            'spacing': {
                'margin': True,
                'padding': True
            }
        },
        'organism-cta': {
            'align': ['wide', 'full'],
            'html': False,
            'color': {
                'text': True,
                'background': True,
                'gradients': True
            },
            'spacing': {
                'margin': True,
                'padding': True
            }
        },
    }
    
    key = f"{block_type}-{block_name}"
    restriction = restrictions.get(key, {})
    
    # Aplicar restricciones
    for key, value in restriction.items():
        if isinstance(value, bool):
            supports[key] = value
        elif isinstance(value, dict):
            if key not in supports:
                supports[key] = {}
            supports[key].update(value)
        elif isinstance(value, list):
            supports[key] = value


def _enhance_attributes_with_instructions(attributes: Dict, block_type: str, block_name: str):
    """Añade instrucciones y placeholders a los atributos."""
    instructions = {
        ('atom-button', 'text'): {
            'description': 'Texto que se muestra en el botón. Sé claro y directo.',
            'placeholder': 'Ej: Comenzar, Saber más, Contactar'
        },
        ('atom-button', 'url'): {
            'description': 'URL de destino. Puede ser una página, post o enlace externo.',
            'placeholder': 'https://ejemplo.com o /pagina'
        },
        ('atom-button', 'variant'): {
            'description': 'Estilo del botón. Primary para acciones principales, Secondary para acciones secundarias.',
            'placeholder': 'primary'
        },
        ('atom-heading', 'text'): {
            'description': 'Texto del título. Usa h1 solo una vez por página.',
            'placeholder': 'Título descriptivo'
        },
        ('atom-heading', 'level'): {
            'description': 'Nivel del título (1-6). Mantén jerarquía: h1 > h2 > h3.',
            'placeholder': '2'
        },
        ('organism-slider', 'slides'): {
            'description': 'Lista de diapositivas. Recomendado: 3-5 slides máximo para mejor rendimiento.',
            'placeholder': 'Agrega slides usando el botón "Añadir slide"'
        },
        ('organism-hero', 'title'): {
            'description': 'Título principal. Sé conciso y directo. Máximo 8-10 palabras.',
            'placeholder': 'Ej: Transformamos tu negocio'
        },
        ('organism-hero', 'subtitle'): {
            'description': 'Subtítulo o descripción. Complementa el título sin repetir información.',
            'placeholder': 'Ej: Soluciones innovadoras para tu empresa'
        },
        ('organism-cta', 'title'): {
            'description': 'Título del CTA. Debe ser una pregunta o declaración que invite a la acción.',
            'placeholder': 'Ej: ¿Listo para comenzar?'
        },
        ('organism-form', 'submitText'): {
            'description': 'Texto del botón de envío. Sé claro sobre la acción que se realizará.',
            'placeholder': 'Ej: Enviar, Solicitar, Contactar'
        },
    }
    
    for attr_name, attr_data in attributes.items():
        key = (f"{block_type}-{block_name}", attr_name)
        instruction = instructions.get(key)
        
        if instruction:
            if 'description' not in attr_data:
                attr_data['description'] = instruction.get('description', '')
            if 'placeholder' not in attr_data and 'placeholder' in instruction:
                # Para atributos string, añadir placeholder como metadata
                if attr_data.get('type') == 'string':
                    attr_data['__placeholder'] = instruction['placeholder']


def _get_block_keywords(block_type: str, block_name: str) -> List[str]:
    """Obtiene keywords relevantes para el bloque."""
    keywords_map = {
        'atom-button': ['button', 'btn', 'action', 'cta', 'link'],
        'atom-heading': ['heading', 'title', 'h1', 'h2', 'h3'],
        'atom-image': ['image', 'img', 'photo', 'picture'],
        'organism-slider': ['slider', 'carousel', 'slideshow', 'banner'],
        'organism-hero': ['hero', 'banner', 'header', 'landing'],
        'organism-cta': ['cta', 'call-to-action', 'button', 'action'],
        'organism-form': ['form', 'contact', 'formulario', 'submit'],
    }
    
    key = f"{block_type}-{block_name}"
    return keywords_map.get(key, [block_name])


def get_editor_placeholder(block_type: str, block_name: str, attribute_name: str) -> str:
    """Obtiene placeholder para mostrar en el editor."""
    placeholders = {
        ('atom-button', 'text'): 'Escribe el texto del botón...',
        ('atom-heading', 'text'): 'Escribe el título...',
        ('organism-hero', 'title'): 'Título principal (máx. 10 palabras)',
        ('organism-hero', 'subtitle'): 'Subtítulo descriptivo',
        ('organism-cta', 'title'): '¿Listo para comenzar?',
        ('organism-cta', 'description'): 'Descripción que invite a la acción',
        ('organism-form', 'submitText'): 'Enviar mensaje',
    }
    
    key = (f"{block_type}-{block_name}", attribute_name)
    return placeholders.get(key, f'Ingresa {attribute_name.replace("-", " ")}...')


def get_block_instructions(block_type: str, block_name: str) -> str:
    """Obtiene instrucciones para mostrar en el editor."""
    instructions = {
        'organism-slider': '💡 Tip: Limita a 3-5 slides para mejor rendimiento. Usa imágenes optimizadas (WebP).',
        'organism-hero': '💡 Tip: Mantén el texto conciso. El CTA debe ser claro y visible.',
        'organism-cta': '💡 Tip: Usa máximo 1-2 CTAs por página. El título debe invitar a la acción.',
        'organism-form': '💡 Tip: Valida todos los campos. Considera usar reCAPTCHA para prevenir spam.',
        'organism-cards-grid': '💡 Tip: En móvil se adapta automáticamente. Elige 2-4 columnas en desktop.',
        'atom-button': '💡 Tip: Usa botones primarios solo para acciones principales. Limita a 1-2 por sección.',
        'atom-heading': '💡 Tip: Usa h1 solo una vez por página. Mantén jerarquía clara.',
        'atom-image': '💡 Tip: Siempre añade texto alternativo para accesibilidad. Usa imágenes optimizadas.',
    }
    
    key = f"{block_type}-{block_name}"
    return instructions.get(key, '')


