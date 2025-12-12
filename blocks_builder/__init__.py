"""
Módulo modular para crear bloques personalizados de Gutenberg.
Estructura organizada por propósito para facilitar mantenimiento.
"""
from .helpers import get_bem_prefix, setup_css_framework, generate_bem_css
from .atoms import (
    create_atom_button,
    create_atom_heading,
    create_atom_input,
    create_atom_icon,
    create_atom_badge,
    create_atom_link,
    create_atom_image
)
from .molecules import (
    create_molecule_card,
    create_molecule_form_field,
    create_molecule_nav_item,
    create_molecule_testimonial,
    create_molecule_pricing_item
)
from .organisms import (
    create_slider_block,
    create_hero_block,
    create_section_block,
    create_cards_block,
    create_gallery_block,
    create_text_image_block,
    create_sidebar_block,
    create_search_block,
    create_pagination_block,
    create_header_block,
    create_footer_block,
    create_form_block,
    create_menu_block,
    create_organism_slider,
    create_organism_hero,
    create_organism_section,
    create_organism_cards_grid,
    create_organism_gallery,
    create_organism_text_image,
    create_organism_sidebar,
    create_organism_search,
    create_organism_pagination,
    create_organism_header,
    create_organism_footer,
    create_organism_form,
    create_organism_menu
)
from .registration import (
    register_blocks_in_functions,
    register_atomic_blocks_in_functions
)
from .assets import (
    setup_conditional_assets,
    minimize_global_css
)

# Función principal que orquesta todo
def create_custom_blocks(theme_dir: str, css_framework: str, plan: dict, theme_slug: str = None):
    """
    Crea todos los bloques personalizados de Gutenberg usando Atomic Design.
    Estructura: atoms/ → molecules/ → organisms/
    Usa prefijo BEM derivado de theme_slug.
    Integrado con controles nativos de Gutenberg.
    """
    import os
    from typing import Dict, Optional
    
    blocks_dir = os.path.join(theme_dir, 'blocks')
    os.makedirs(blocks_dir, exist_ok=True)
    
    # Obtener prefijo BEM
    bem_prefix = get_bem_prefix(theme_slug)
    
    # Crear estructura de directorios atómicos
    atoms_dir = os.path.join(blocks_dir, 'atoms')
    molecules_dir = os.path.join(blocks_dir, 'molecules')
    organisms_dir = os.path.join(blocks_dir, 'organisms')
    os.makedirs(atoms_dir, exist_ok=True)
    os.makedirs(molecules_dir, exist_ok=True)
    os.makedirs(organisms_dir, exist_ok=True)
    
    # ========================================
    # ÁTOMOS: Componentes básicos reutilizables
    # ========================================
    create_atom_button(atoms_dir, css_framework, bem_prefix)
    create_atom_heading(atoms_dir, css_framework, bem_prefix)
    create_atom_input(atoms_dir, css_framework, bem_prefix)
    create_atom_icon(atoms_dir, css_framework, bem_prefix)
    create_atom_badge(atoms_dir, css_framework, bem_prefix)
    create_atom_link(atoms_dir, css_framework, bem_prefix)
    create_atom_image(atoms_dir, css_framework, bem_prefix)
    
    # ========================================
    # MOLÉCULAS: Combinaciones de átomos
    # ========================================
    create_molecule_card(molecules_dir, css_framework, bem_prefix)
    create_molecule_form_field(molecules_dir, css_framework, bem_prefix)
    create_molecule_nav_item(molecules_dir, css_framework, bem_prefix)
    create_molecule_testimonial(molecules_dir, css_framework, bem_prefix)
    create_molecule_pricing_item(molecules_dir, css_framework, bem_prefix)
    
    # ========================================
    # ORGANISMOS: Componentes complejos
    # ========================================
    create_organism_slider(organisms_dir, css_framework, bem_prefix)
    create_organism_hero(organisms_dir, css_framework, bem_prefix)
    create_organism_section(organisms_dir, css_framework, bem_prefix)
    create_organism_cards_grid(organisms_dir, css_framework, bem_prefix)
    create_organism_gallery(organisms_dir, css_framework, bem_prefix)
    create_organism_text_image(organisms_dir, css_framework, bem_prefix)
    create_organism_sidebar(organisms_dir, css_framework, bem_prefix)
    create_organism_search(organisms_dir, css_framework, bem_prefix)
    create_organism_pagination(organisms_dir, css_framework, bem_prefix)
    create_organism_header(organisms_dir, css_framework, bem_prefix)
    create_organism_footer(organisms_dir, css_framework, bem_prefix)
    create_organism_form(organisms_dir, css_framework, bem_prefix)
    create_organism_menu(organisms_dir, css_framework, bem_prefix)
    create_organism_cta(organisms_dir, css_framework, bem_prefix)
    
    # Registrar bloques en functions.php con estructura atómica
    register_atomic_blocks_in_functions(theme_dir, blocks_dir, bem_prefix)
    
    # Configurar carga condicional de assets
    setup_conditional_assets(theme_dir, bem_prefix)
    
    # Minimizar CSS global
    minimize_global_css(theme_dir, bem_prefix)


# Exportar funciones principales para compatibilidad hacia atrás
__all__ = [
    'get_bem_prefix',
    'setup_css_framework',
    'generate_bem_css',
    'create_custom_blocks',
    'create_atom_button',
    'create_atom_heading',
    'create_atom_input',
    'create_atom_icon',
    'create_atom_badge',
    'create_atom_link',
    'create_atom_image',
    'create_molecule_card',
    'create_molecule_form_field',
    'create_molecule_nav_item',
    'create_molecule_testimonial',
    'create_molecule_pricing_item',
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
    'create_organism_cta',
    'register_blocks_in_functions',
    'register_atomic_blocks_in_functions',
    'setup_conditional_assets',
    'minimize_global_css',
]

