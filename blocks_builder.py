"""
Módulo para crear bloques personalizados de Gutenberg
REFACTORIZADO: Ahora usa estructura modular en blocks_builder/

Este archivo mantiene compatibilidad hacia atrás importando desde blocks_builder/
NOTA: Si hay errores de importación, las funciones están en blocks_builder_backup.py
"""
# Importar todo desde el módulo modular
try:
    from blocks_builder import (
    get_bem_prefix,
    setup_css_framework,
    generate_bem_css,
    create_custom_blocks,
    create_atom_button,
    create_atom_heading,
    create_atom_input,
    create_atom_icon,
    create_atom_badge,
    create_atom_link,
    create_molecule_card,
    create_molecule_form_field,
    create_molecule_nav_item,
    create_molecule_testimonial,
    create_molecule_pricing_item,
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
    register_blocks_in_functions,
    register_atomic_blocks_in_functions,
    )
except ImportError:
    # Fallback: importar desde el backup si el módulo modular no está completo
    import sys
    import importlib.util
    spec = importlib.util.spec_from_file_location("blocks_builder_backup", "blocks_builder_backup.py")
    if spec and spec.loader:
        backup_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(backup_module)
        # Re-exportar funciones principales
        get_bem_prefix = backup_module.get_bem_prefix
        setup_css_framework = backup_module.setup_css_framework
        create_custom_blocks = backup_module.create_custom_blocks
        # Otras funciones según necesidad
        create_slider_block = getattr(backup_module, 'create_slider_block', None)
        create_hero_block = getattr(backup_module, 'create_hero_block', None)
        # ... agregar más según necesidad
    else:
        raise ImportError("No se pudo cargar blocks_builder_backup.py")

# Mantener compatibilidad hacia atrás
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
    'register_blocks_in_functions',
    'register_atomic_blocks_in_functions',
]
