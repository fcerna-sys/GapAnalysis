"""
Sistema de gestión de assets condicionales por bloque.
Organiza CSS/JS en /assets/blocks/ y genera carga condicional.
"""
import os
import json
import shutil
from typing import Dict, List, Optional


def setup_conditional_assets(theme_dir: str, bem_prefix: str = 'img2html'):
    """
    Configura el sistema de carga condicional de assets.
    Mueve CSS/JS a /assets/blocks/ y actualiza block.json.
    """
    blocks_dir = os.path.join(theme_dir, 'blocks')
    assets_dir = os.path.join(theme_dir, 'assets', 'blocks')
    
    # Crear estructura de assets
    atoms_assets = os.path.join(assets_dir, 'atoms')
    molecules_assets = os.path.join(assets_dir, 'molecules')
    organisms_assets = os.path.join(assets_dir, 'organisms')
    os.makedirs(atoms_assets, exist_ok=True)
    os.makedirs(molecules_assets, exist_ok=True)
    os.makedirs(organisms_assets, exist_ok=True)
    
    # Manifest de bloques para carga condicional
    blocks_manifest = {}
    
    # Procesar átomos
    atoms_dir = os.path.join(blocks_dir, 'atoms')
    if os.path.isdir(atoms_dir):
        for atom_name in os.listdir(atoms_dir):
            atom_path = os.path.join(atoms_dir, atom_name)
            if os.path.isdir(atom_path):
                _process_block_assets(
                    atom_path, 
                    os.path.join(atoms_assets, atom_name),
                    f"{bem_prefix}/atom-{atom_name}",
                    blocks_manifest
                )
    
    # Procesar moléculas
    molecules_dir = os.path.join(blocks_dir, 'molecules')
    if os.path.isdir(molecules_dir):
        for molecule_name in os.listdir(molecules_dir):
            molecule_path = os.path.join(molecules_dir, molecule_name)
            if os.path.isdir(molecule_path):
                _process_block_assets(
                    molecule_path,
                    os.path.join(molecules_assets, molecule_name),
                    f"{bem_prefix}/molecule-{molecule_name}",
                    blocks_manifest
                )
    
    # Procesar organismos
    organisms_dir = os.path.join(blocks_dir, 'organisms')
    if os.path.isdir(organisms_dir):
        for organism_name in os.listdir(organisms_dir):
            organism_path = os.path.join(organisms_dir, organism_name)
            if os.path.isdir(organism_path):
                _process_block_assets(
                    organism_path,
                    os.path.join(organisms_assets, organism_name),
                    f"{bem_prefix}/organism-{organism_name}",
                    blocks_manifest
                )
    
    # Guardar manifest
    manifest_path = os.path.join(theme_dir, 'blocks-manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(blocks_manifest, f, indent=2, ensure_ascii=False)
    
    # Generar PHP para carga condicional
    _generate_conditional_loading_php(theme_dir, bem_prefix, blocks_manifest)
    
    return blocks_manifest


def _process_block_assets(block_dir: str, assets_dir: str, block_name: str, manifest: Dict):
    """Procesa y mueve assets de un bloque a la estructura de assets."""
    os.makedirs(assets_dir, exist_ok=True)
    
    block_json_path = os.path.join(block_dir, 'block.json')
    if not os.path.isfile(block_json_path):
        return
    
    # Leer block.json
    with open(block_json_path, 'r', encoding='utf-8') as f:
        block_json = json.load(f)
    
    # Determinar theme_dir desde assets_dir
    # assets_dir está en theme_dir/assets/blocks/...
    theme_dir = os.path.dirname(os.path.dirname(os.path.dirname(assets_dir)))
    rel_assets_dir = os.path.relpath(assets_dir, theme_dir).replace('\\', '/')
    
    block_assets = {
        'style': [],
        'script': [],
        'editorStyle': [],
        'editorScript': []
    }
    
    # Mover y actualizar style.css
    style_src = os.path.join(block_dir, 'style.css')
    if os.path.isfile(style_src):
        style_dst = os.path.join(assets_dir, 'style.css')
        shutil.copy2(style_src, style_dst)
        rel_style = f"{rel_assets_dir}/style.css"
        block_assets['style'].append(rel_style)
        # En block.json, la ruta debe ser relativa al bloque, pero WordPress la resuelve desde el tema
        # Usamos la ruta completa relativa al tema
        block_json['style'] = rel_style
    
    # Mover y actualizar editor.css
    editor_style_src = os.path.join(block_dir, 'editor.css')
    if os.path.isfile(editor_style_src):
        editor_style_dst = os.path.join(assets_dir, 'editor.css')
        shutil.copy2(editor_style_src, editor_style_dst)
        rel_editor_style = f"{rel_assets_dir}/editor.css"
        block_assets['editorStyle'].append(rel_editor_style)
        block_json['editorStyle'] = rel_editor_style
    
    # Mover y actualizar index.js (editor script)
    editor_js_src = os.path.join(block_dir, 'index.js')
    if os.path.isfile(editor_js_src):
        editor_js_dst = os.path.join(assets_dir, 'index.js')
        shutil.copy2(editor_js_src, editor_js_dst)
        rel_editor_js = f"{rel_assets_dir}/index.js"
        block_assets['editorScript'].append(rel_editor_js)
        block_json['editorScript'] = rel_editor_js
    
    # Mover y actualizar view.js (frontend script) si existe
    view_js_src = os.path.join(block_dir, 'view.js')
    if os.path.isfile(view_js_src):
        view_js_dst = os.path.join(assets_dir, 'view.js')
        shutil.copy2(view_js_src, view_js_dst)
        rel_view_js = f"{rel_assets_dir}/view.js"
        block_assets['script'].append(rel_view_js)
        block_json['viewScript'] = rel_view_js
    
    # Actualizar block.json
    with open(block_json_path, 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2, ensure_ascii=False)
    
    # Agregar al manifest
    manifest[block_name] = block_assets


def _generate_conditional_loading_php(theme_dir: str, bem_prefix: str, blocks_manifest: Dict):
    """Genera el archivo PHP para carga condicional de assets."""
    php_dir = os.path.join(theme_dir, 'php')
    os.makedirs(php_dir, exist_ok=True)
    
    # Convertir manifest a formato PHP
    manifest_php = "<?php\nreturn [\n"
    for block_name, assets in blocks_manifest.items():
        manifest_php += f"    '{block_name}' => [\n"
        if assets.get('style'):
            manifest_php += f"        'style' => {json.dumps(assets['style'], ensure_ascii=False)},\n"
        if assets.get('script'):
            manifest_php += f"        'script' => {json.dumps(assets['script'], ensure_ascii=False)},\n"
        if assets.get('editorStyle'):
            manifest_php += f"        'editorStyle' => {json.dumps(assets['editorStyle'], ensure_ascii=False)},\n"
        if assets.get('editorScript'):
            manifest_php += f"        'editorScript' => {json.dumps(assets['editorScript'], ensure_ascii=False)},\n"
        manifest_php += "    ],\n"
    manifest_php += "];\n"
    
    # Guardar manifest PHP
    manifest_php_path = os.path.join(theme_dir, 'blocks-manifest.php')
    with open(manifest_php_path, 'w', encoding='utf-8') as f:
        f.write(manifest_php)
    
    # Generar función de carga condicional
    conditional_php = f"""<?php
/**
 * Sistema de carga condicional de assets por bloque
 * Solo carga CSS/JS de bloques presentes en el contenido
 * 
 * @package {bem_prefix}
 */

function {bem_prefix}_conditional_block_assets() {{
    $manifest_path = get_theme_file_path('blocks-manifest.php');
    if (!file_exists($manifest_path)) {{
        return;
    }}
    
    $manifest = include $manifest_path;
    if (!is_array($manifest)) {{
        return;
    }}
    
    // En el editor, cargar todos los assets de editor
    if (is_admin() || (defined('REST_REQUEST') && REST_REQUEST)) {{
        foreach ($manifest as $block_name => $assets) {{
            // Editor styles
            if (isset($assets['editorStyle'])) {{
                foreach ((array)$assets['editorStyle'] as $style_path) {{
                    $full_path = get_theme_file_path($style_path);
                    if (file_exists($full_path)) {{
                        $handle = '{bem_prefix}-block-editor-' . md5($block_name . $style_path);
                        $uri = get_theme_file_uri($style_path);
                        $version = filemtime($full_path);
                        wp_enqueue_style($handle, $uri, [], $version);
                    }}
                }}
            }}
            // Editor scripts
            if (isset($assets['editorScript'])) {{
                foreach ((array)$assets['editorScript'] as $script_path) {{
                    $full_path = get_theme_file_path($script_path);
                    if (file_exists($full_path)) {{
                        $handle = '{bem_prefix}-block-editor-' . md5($block_name . $script_path);
                        $uri = get_theme_file_uri($script_path);
                        $version = filemtime($full_path);
                        wp_enqueue_script($handle, $uri, ['wp-blocks', 'wp-element', 'wp-editor'], $version, true);
                    }}
                }}
            }}
        }}
        return;
    }}
    
    // En el frontend, cargar solo assets de bloques presentes
    $content_to_check = '';
    
    // Obtener contenido de la página/post actual
    if (is_singular()) {{
        global $post;
        if ($post) {{
            $content_to_check = $post->post_content;
        }}
    }}
    
    // También verificar en template parts (FSE)
    if (function_exists('wp_is_block_theme') && wp_is_block_theme()) {{
        // Verificar en templates
        $template = get_block_template();
        if ($template && isset($template->content)) {{
            $content_to_check .= $template->content;
        }}
        
        // Verificar en template parts
        $template_parts = get_block_template_parts();
        foreach ($template_parts as $part) {{
            if (isset($part->content)) {{
                $content_to_check .= $part->content;
            }}
        }}
    }}
    
    // Verificar cada bloque y encolar assets si está presente
    foreach ($manifest as $block_name => $assets) {{
        if (has_block($block_name, $content_to_check)) {{
            // Frontend styles
            if (isset($assets['style'])) {{
                foreach ((array)$assets['style'] as $style_path) {{
                    $full_path = get_theme_file_path($style_path);
                    if (file_exists($full_path)) {{
                        $handle = '{bem_prefix}-block-' . md5($block_name . $style_path);
                        $uri = get_theme_file_uri($style_path);
                        $version = filemtime($full_path);
                        wp_enqueue_style($handle, $uri, [], $version);
                    }}
                }}
            }}
            // Frontend scripts
            if (isset($assets['script'])) {{
                foreach ((array)$assets['script'] as $script_path) {{
                    $full_path = get_theme_file_path($script_path);
                    if (file_exists($full_path)) {{
                        $handle = '{bem_prefix}-block-' . md5($block_name . $script_path);
                        $uri = get_theme_file_uri($script_path);
                        $version = filemtime($full_path);
                        wp_enqueue_script($handle, $uri, [], $version, true);
                    }}
                }}
            }}
        }}
    }}
}}

// Hook para carga condicional en frontend
add_action('wp_enqueue_scripts', '{bem_prefix}_conditional_block_assets', 20);

// Hook para carga en editor
add_action('enqueue_block_editor_assets', '{bem_prefix}_conditional_block_assets', 20);

// También usar render_block filter para detectar bloques dinámicos
function {bem_prefix}_enqueue_block_assets_on_render($content, $block) {{
    if (is_admin() || (defined('REST_REQUEST') && REST_REQUEST)) {{
        return $content;
    }}
    
    $manifest_path = get_theme_file_path('blocks-manifest.php');
    if (!file_exists($manifest_path)) {{
        return $content;
    }}
    
    $manifest = include $manifest_path;
    if (!is_array($manifest)) {{
        return $content;
    }}
    
    $block_name = isset($block['blockName']) ? $block['blockName'] : null;
    if (!$block_name || !isset($manifest[$block_name])) {{
        return $content;
    }}
    
    $assets = $manifest[$block_name];
    
    // Encolar styles
    if (isset($assets['style'])) {{
        foreach ((array)$assets['style'] as $style_path) {{
            $full_path = get_theme_file_path($style_path);
            if (file_exists($full_path)) {{
                $handle = '{bem_prefix}-block-' . md5($block_name . $style_path);
                if (!wp_style_is($handle, 'enqueued')) {{
                    $uri = get_theme_file_uri($style_path);
                    $version = filemtime($full_path);
                    wp_enqueue_style($handle, $uri, [], $version);
                }}
            }}
        }}
    }}
    
    // Encolar scripts
    if (isset($assets['script'])) {{
        foreach ((array)$assets['script'] as $script_path) {{
            $full_path = get_theme_file_path($script_path);
            if (file_exists($full_path)) {{
                $handle = '{bem_prefix}-block-' . md5($block_name . $script_path);
                if (!wp_script_is($handle, 'enqueued')) {{
                    $uri = get_theme_file_uri($script_path);
                    $version = filemtime($full_path);
                    wp_enqueue_script($handle, $uri, [], $version, true);
                }}
            }}
        }}
    }}
    
    return $content;
}}
add_filter('render_block', '{bem_prefix}_enqueue_block_assets_on_render', 10, 2);
"""
    
    conditional_php_path = os.path.join(php_dir, 'conditional-assets.php')
    with open(conditional_php_path, 'w', encoding='utf-8') as f:
        f.write(conditional_php)
    
    print(f"✓ Sistema de carga condicional configurado ({bem_prefix})")


def minimize_global_css(theme_dir: str, bem_prefix: str = 'img2html'):
    """
    Minimiza el CSS global removiendo estilos que están en bloques.
    Solo mantiene estilos base del tema.
    """
    style_css_path = os.path.join(theme_dir, 'style.css')
    if not os.path.isfile(style_css_path):
        return
    
    # Leer style.css
    with open(style_css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraer solo el header (comentario) y estilos base mínimos
    lines = content.split('\n')
    header_end = 0
    for i, line in enumerate(lines):
        if line.strip() == '*/':
            header_end = i + 1
            break
    
    # Mantener header y solo variables CSS y estilos base
    minimal_css = '\n'.join(lines[:header_end]) + '\n\n'
    minimal_css += """:root {
    --wp--preset--color--background: #ffffff;
    --wp--preset--color--text: #111111;
    --wp--preset--color--primary: #3b82f6;
    --wp--preset--color--secondary: #64748b;
}

/* Estilos base mínimos del tema */
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
    line-height: 1.6;
}

:focus-visible {
    outline: 2px solid var(--wp--preset--color--primary);
    outline-offset: 2px;
}

img {
    max-width: 100%;
    height: auto;
}
"""
    
    # Guardar CSS minimizado
    with open(style_css_path, 'w', encoding='utf-8') as f:
        f.write(minimal_css)
    
    print(f"✓ CSS global minimizado ({bem_prefix})")

