"""
Funciones de registro de bloques en functions.php de WordPress.
"""
import os
from .prefix_manager import get_prefix_manager


def register_blocks_in_functions(theme_dir: str, blocks_dir: str):
    """Registra todos los bloques en functions.php."""
    functions_path = os.path.join(theme_dir, 'functions.php')
    
    # Leer functions.php existente
    functions_content = ""
    if os.path.isfile(functions_path):
        with open(functions_path, 'r', encoding='utf-8') as f:
            functions_content = f.read()
    
    # Agregar registro de bloques si no existe
    if 'register_block_type' not in functions_content or 'img2html' not in functions_content:
        blocks_registration = """
// Registrar bloques personalizados
function img2html_register_blocks() {
    $blocks = [
        'slider',
        'hero',
        'section',
        'cards',
        'gallery',
        'text-image',
        'sidebar',
        'search-extended',
        'pagination',
        'header',
        'footer',
        'form',
        'menu'
    ];
    
    foreach ($blocks as $block) {
        $block_path = get_template_directory() . '/blocks/' . $block;
        if (file_exists($block_path . '/block.json')) {
            register_block_type($block_path);
        }
    }
}
add_action('init', 'img2html_register_blocks');
"""
        # Agregar al final del archivo
        if not functions_content.strip().endswith('?>'):
            functions_content += blocks_registration
        else:
            functions_content = functions_content.rstrip('?>') + blocks_registration + "\n?>"
        
        with open(functions_path, 'w', encoding='utf-8') as f:
            f.write(functions_content)


def register_atomic_blocks_in_functions(theme_dir: str, blocks_dir: str, bem_prefix: str = 'img2html'):
    """Registra todos los bloques atómicos, moleculares y organismos en functions.php."""
    # Usar PrefixManager para obtener prefijos consistentes
    pm = get_prefix_manager(bem_prefix, bem_prefix)
    php_prefix = pm.bem_prefix.replace('-', '_')
    
    functions_path = os.path.join(theme_dir, 'functions.php')
    
    # Leer functions.php existente
    functions_content = ""
    if os.path.isfile(functions_path):
        with open(functions_path, 'r', encoding='utf-8') as f:
            functions_content = f.read()
    
    # Agregar registro de bloques atómicos si no existe
    register_function = pm.get_php_function_name('register_atomic_blocks')
    categories_function = pm.get_php_function_name('register_block_categories')
    
    if register_function not in functions_content:
        blocks_registration = f"""
// Registrar categorías de bloques atómicos
function {categories_function}() {{
    register_block_pattern_category('{pm.get_block_category('atoms')}', array('label' => 'Átomos'));
    register_block_pattern_category('{pm.get_block_category('molecules')}', array('label' => 'Moléculas'));
    register_block_pattern_category('{pm.get_block_category('organisms')}', array('label' => 'Organismos'));
}}
add_action('init', '{categories_function}');

// Registrar bloques con estructura atómica (átomos → moléculas → organismos)
function {register_function}() {{
    $base_path = get_template_directory() . '/blocks';
    
    // Átomos: Componentes básicos reutilizables
    $atoms = ['button', 'heading', 'input', 'icon', 'badge', 'link', 'image'];
    foreach ($atoms as $atom) {{
        $block_path = $base_path . '/atoms/' . $atom;
        if (file_exists($block_path . '/block.json')) {{
            register_block_type($block_path);
        }}
    }}
    
    // Moléculas: Combinaciones de átomos
    $molecules = ['card', 'form-field', 'nav-item', 'testimonial', 'pricing-item'];
    foreach ($molecules as $molecule) {{
        $block_path = $base_path . '/molecules/' . $molecule;
        if (file_exists($block_path . '/block.json')) {{
            register_block_type($block_path);
        }}
    }}
    
    // Organismos: Componentes complejos que usan moléculas y átomos
    $organisms = ['slider', 'hero', 'section', 'cards', 'gallery', 'text-image', 
                  'sidebar', 'search-extended', 'pagination', 'header', 'footer', 'form', 'menu', 'cta'];
    foreach ($organisms as $organism) {{
        $block_path = $base_path . '/organisms/' . $organism;
        if (file_exists($block_path . '/block.json')) {{
            register_block_type($block_path);
        }}
    }}
}}
add_action('init', '{register_function}');
"""
        # Agregar al final del archivo
        if not functions_content.strip().endswith('?>'):
            functions_content += blocks_registration
        else:
            functions_content = functions_content.rstrip('?>') + blocks_registration + "\n?>"
        
        with open(functions_path, 'w', encoding='utf-8') as f:
            f.write(functions_content)

