"""
Sistema de optimización de rendimiento para temas WordPress.
Incluye: minificación, purga de CSS, critical CSS, lazy-loading, carga condicional.
"""
import os
import re
import json
from typing import Dict, List, Optional, Set
import subprocess
import shutil
def _validate_bem_class(class_name: str, bem_prefix: str) -> bool:
    if not class_name or not bem_prefix:
        return False
    pattern = rf'^{re.escape(bem_prefix)}-[a-z0-9-]+(__[a-z0-9-]+)?(--[a-z0-9-]+)?$'
    return bool(re.match(pattern, class_name))


def setup_build_pipeline(theme_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """
    Configura el pipeline de build completo con todas las optimizaciones.
    """
    try:
        # 1. Crear estructura de directorios para build
        build_dir = os.path.join(theme_dir, 'build')
        assets_dir = os.path.join(theme_dir, 'assets')
        css_dir = os.path.join(assets_dir, 'css')
        js_dir = os.path.join(assets_dir, 'js')
        blocks_dir = os.path.join(theme_dir, 'blocks')
        
        os.makedirs(build_dir, exist_ok=True)
        os.makedirs(css_dir, exist_ok=True)
        os.makedirs(js_dir, exist_ok=True)
        
        # Validación BEM
        validate_bem_in_theme(theme_dir, bem_prefix)

        # 2. Generar manifest de bloques para carga condicional
        generate_block_manifest(theme_dir, bem_prefix)
        
        # 3. Configurar sistema de carga condicional
        setup_conditional_loading(theme_dir, bem_prefix)
        
        # 4. Configurar minificación
        setup_minification(theme_dir, css_framework)
        
        # 5. Configurar purga de CSS
        setup_css_purge(theme_dir, css_framework, bem_prefix)
        
        # 6. Generar critical CSS
        generate_critical_css(theme_dir, css_framework, bem_prefix)
        
        # 7. Configurar lazy-loading mejorado
        setup_lazy_loading(theme_dir)
        
        # 8. Crear script de build
        create_build_script(theme_dir, css_framework)
        
        print("✓ Pipeline de optimización configurado")
        
    except Exception as e:
        print(f"Error al configurar pipeline de build: {e}")
        import traceback
        traceback.print_exc()


def validate_bem_in_theme(theme_dir: str, bem_prefix: str):
    invalid: Set[str] = set()

    def _collect_from_php(path: str):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            return
        for m in re.finditer(r'class\s*=\s*"([^"]+)"', content):
            classes = re.split(r"\s+", m.group(1))
            for cls in classes:
                if cls.startswith(f"{bem_prefix}-") and not _validate_bem_class(cls, bem_prefix):
                    invalid.add(cls)

    def _collect_from_css(path: str):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            return
        for cls in re.findall(r"\.([a-z0-9_-]+)", content, flags=re.I):
            if cls.startswith(f"{bem_prefix}-") and not _validate_bem_class(cls, bem_prefix):
                invalid.add(cls)

    blocks_dir = os.path.join(theme_dir, 'blocks')
    for level in ['atoms', 'molecules', 'organisms']:
        level_dir = os.path.join(blocks_dir, level)
        if not os.path.isdir(level_dir):
            continue
        for block_name in os.listdir(level_dir):
            block_path = os.path.join(level_dir, block_name)
            if not os.path.isdir(block_path):
                continue
            _collect_from_php(os.path.join(block_path, 'render.php'))
            _collect_from_css(os.path.join(block_path, 'style.css'))
            _collect_from_css(os.path.join(block_path, 'editor.css'))

    patterns_dir = os.path.join(theme_dir, 'patterns')
    if os.path.isdir(patterns_dir):
        for fname in os.listdir(patterns_dir):
            if fname.endswith('.php') or fname.endswith('.html'):
                _collect_from_php(os.path.join(patterns_dir, fname))

    templates_dir = os.path.join(theme_dir, 'templates')
    if os.path.isdir(templates_dir):
        for root, _, files in os.walk(templates_dir):
            for fname in files:
                if fname.endswith('.html') or fname.endswith('.php'):
                    _collect_from_php(os.path.join(root, fname))

    parts_dir = os.path.join(theme_dir, 'parts')
    if os.path.isdir(parts_dir):
        for root, _, files in os.walk(parts_dir):
            for fname in files:
                if fname.endswith('.html') or fname.endswith('.php'):
                    _collect_from_php(os.path.join(root, fname))

    if invalid:
        msg = "\n".join(sorted(invalid))
        raise RuntimeError(f"Clases BEM inválidas detectadas para prefijo '{bem_prefix}':\n{msg}")


def generate_block_manifest(theme_dir: str, bem_prefix: str):
    """
    Genera blocks-manifest.php con todos los bloques y sus assets.
    """
    blocks_dir = os.path.join(theme_dir, 'blocks')
    manifest_path = os.path.join(theme_dir, 'blocks-manifest.php')
    manifest_json_path = os.path.join(theme_dir, 'blocks-manifest.json')
    
    manifest = {}
    
    # Escanear todos los bloques (átomos, moléculas, organismos)
    for level in ['atoms', 'molecules', 'organisms']:
        level_dir = os.path.join(blocks_dir, level)
        if not os.path.isdir(level_dir):
            continue
        
        for block_name in os.listdir(level_dir):
            block_path = os.path.join(level_dir, block_name)
            if not os.path.isdir(block_path):
                continue
            
            # Leer block.json
            block_json_path = os.path.join(block_path, 'block.json')
            if not os.path.isfile(block_json_path):
                continue
            
            try:
                with open(block_json_path, 'r', encoding='utf-8') as f:
                    block_data = json.load(f)
                
                block_name_full = block_data.get('name', f'{bem_prefix}/{level}-{block_name}')
                block_version = block_data.get('version', '1.0.0')
                
                # Buscar archivos CSS y JS del bloque
                style_path = os.path.join(block_path, 'style.css')
                editor_style_path = os.path.join(block_path, 'editor.css')
                script_path = os.path.join(block_path, 'script.js')
                
                assets = {}
                
                # CSS del bloque
                styles = []
                if os.path.isfile(style_path):
                    rel_style = f'blocks/{level}/{block_name}/style.css'
                    styles.append(rel_style)
                if os.path.isfile(editor_style_path):
                    rel_editor = f'blocks/{level}/{block_name}/editor.css'
                    styles.append(rel_editor)
                
                if styles:
                    assets['style'] = styles
                
                # JS del bloque
                if os.path.isfile(script_path):
                    rel_script = f'blocks/{level}/{block_name}/script.js'
                    assets['script'] = [rel_script]
                
                if assets:
                    assets['version'] = block_version
                    manifest[block_name_full] = assets
                    
            except Exception:
                continue
    
    # Generar PHP manifest
    manifest_php = f"""<?php
/**
 * Manifest de assets por bloque
 * Generado automáticamente - NO EDITAR MANUALMENTE
 * 
 * @package {bem_prefix}
 */

return {_php_array(manifest)};
"""
    
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(manifest_php)
    try:
        with open(manifest_json_path, 'w', encoding='utf-8') as jf:
            json.dump(manifest, jf, indent=2)
    except Exception:
        pass


def _php_array(data: Dict) -> str:
    """Convierte un dict Python a formato PHP array."""
    if isinstance(data, dict):
        items = []
        for key, value in data.items():
            key_str = f"'{key}'" if isinstance(key, str) else str(key)
            value_str = _php_array(value)
            items.append(f"{key_str} => {value_str}")
        return "[\n        " + ",\n        ".join(items) + "\n    ]"
    elif isinstance(data, list):
        items = [_php_array(item) for item in data]
        return "[" + ", ".join(items) + "]"
    elif isinstance(data, str):
        return f"'{data.replace(chr(39), chr(92) + chr(39))}'"
    else:
        return str(data)


def setup_conditional_loading(theme_dir: str, bem_prefix: str):
    """
    Configura el sistema de carga condicional de assets por bloque.
    """
    php_dir = os.path.join(theme_dir, 'php')
    os.makedirs(php_dir, exist_ok=True)
    
    conditional_loading_php = f"""<?php
/**
 * Sistema de carga condicional de assets por bloque
 * Solo carga CSS/JS de bloques que están presentes en el contenido
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
    
    // En el editor, cargar todos los assets
    if (is_admin() || (defined('REST_REQUEST') && REST_REQUEST)) {{
        foreach ($manifest as $block_name => $assets) {{
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
        return;
    }}
    
    // En el front-end, cargar solo bloques usados
    add_filter('render_block', function($content, $block) use ($manifest) {{
        $block_name = isset($block['blockName']) ? $block['blockName'] : null;
        if (!$block_name || !isset($manifest[$block_name])) {{
            return $content;
        }}
        
        $assets = $manifest[$block_name];
        
        // Cargar CSS
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
        
        // Cargar JS
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
    }}, 10, 2);
}}
add_action('init', '{bem_prefix}_conditional_block_assets');
"""
    
    conditional_path = os.path.join(php_dir, 'conditional-assets.php')
    with open(conditional_path, 'w', encoding='utf-8') as f:
        f.write(conditional_loading_php)


def setup_minification(theme_dir: str, css_framework: str):
    """
    Configura minificación de CSS y JS.
    """
    build_dir = os.path.join(theme_dir, 'build')
    minify_script = os.path.join(build_dir, 'minify.js')
    
    # Script Node.js para minificación (usa clean-css y terser)
    minify_js = """const fs = require('fs');
const path = require('path');
const CleanCSS = require('clean-css');
const { minify } = require('terser');

const themeDir = path.join(__dirname, '..');
const assetsDir = path.join(themeDir, 'assets');

// Minificar CSS
function minifyCSS() {
    const cssDir = path.join(assetsDir, 'css');
    if (!fs.existsSync(cssDir)) return;
    
    fs.readdirSync(cssDir).forEach(file => {
        if (file.endsWith('.css') && !file.endsWith('.min.css')) {
            const filePath = path.join(cssDir, file);
            const content = fs.readFileSync(filePath, 'utf8');
            const minified = new CleanCSS({}).minify(content).styles;
            const minPath = filePath.replace('.css', '.min.css');
            fs.writeFileSync(minPath, minified);
            console.log(`✓ Minificado: ${file}`);
        }
    });
}

// Minificar JS
function minifyJS() {
    const jsDir = path.join(assetsDir, 'js');
    if (!fs.existsSync(jsDir)) return;
    
    fs.readdirSync(jsDir).forEach(file => {
        if (file.endsWith('.js') && !file.endsWith('.min.js')) {
            const filePath = path.join(jsDir, file);
            const content = fs.readFileSync(filePath, 'utf8');
            minify(content).then(result => {
                const minPath = filePath.replace('.js', '.min.js');
                fs.writeFileSync(minPath, result.code);
                console.log(`✓ Minificado: ${file}`);
            }).catch(err => {
                console.error(`Error minificando ${file}:`, err);
            });
        }
    });
}

minifyCSS();
minifyJS();
"""
    
    with open(minify_script, 'w', encoding='utf-8') as f:
        f.write(minify_js)
    
    # Package.json para dependencias
    package_json_path = os.path.join(theme_dir, 'package.json')
    if not os.path.isfile(package_json_path):
        package_json = {
            "name": "theme-build",
            "version": "1.0.0",
            "scripts": {
                "minify": "node build/minify.js",
                "purge": "node build/purge.js",
                "build": "npm run minify && npm run purge"
            },
            "devDependencies": {
                "clean-css": "^5.3.2",
                "terser": "^5.19.2",
                "purgecss": "^5.0.0"
            }
        }
        with open(package_json_path, 'w', encoding='utf-8') as f:
            json.dump(package_json, f, indent=2)


def setup_css_purge(theme_dir: str, css_framework: str, bem_prefix: str):
    """
    Configura purga de CSS no usado usando PurgeCSS.
    """
    build_dir = os.path.join(theme_dir, 'build')
    purge_script = os.path.join(build_dir, 'purge.js')
    
    # Los paths se generarán dinámicamente en el script JS
    
    purge_js = f"""const PurgeCSS = require('purgecss').PurgeCSS;
const fs = require('fs');
const path = require('path');

const themeDir = path.join(__dirname, '..');
const assetsDir = path.join(themeDir, 'assets');
const cssDir = path.join(assetsDir, 'css');

const content = [
    '{theme_dir}/**/*.html',
    '{theme_dir}/**/*.php',
    '{theme_dir}/blocks/**/*.php',
    '{theme_dir}/templates/**/*.html',
    '{theme_dir}/parts/**/*.html',
    '{theme_dir}/patterns/**/*.php'
];

// Los archivos CSS se listan desde el directorio

const safelist = [
    /^{bem_prefix}-/,
    /wp-/,
    /has-/,
    /is-/,
    /align/,
    /^screen-reader/,
    /^sr-only/
];

async function purge() {{
    if (!fs.existsSync(cssDir)) return;
    const files = fs.readdirSync(cssDir).filter(f => f.endsWith('.css') && !f.endsWith('.min.css') && !f.endsWith('.purged.css'));
    for (const file of files) {{
        const filePath = path.join(cssDir, file);
        const results = await new PurgeCSS().purge({{
            content: content,
            css: [filePath],
            safelist: safelist,
            defaultExtractor: (content) => content.match(/[A-Za-z0-9-_/:]*[A-Za-z0-9-_/]/g) || []
        }});
        if (results && results[0]) {{
            const purgedPath = path.join(cssDir, file.replace('.css', '.purged.css'));
            fs.writeFileSync(purgedPath, results[0].css);
            console.log(`✓ Purged: ${{file}}`);
        }}
    }}
}}

purge();
"""
    
    with open(purge_script, 'w', encoding='utf-8') as f:
        f.write(purge_js)


def generate_critical_css(theme_dir: str, css_framework: str, bem_prefix: str):
    """
    Genera critical CSS para above-the-fold content.
    """
    css_dir = os.path.join(theme_dir, 'assets', 'css')
    critical_css_path = os.path.join(css_dir, 'critical.css')
    
    # Critical CSS básico (se puede expandir)
    critical_css = f"""/* Critical CSS - Above the fold */
/* Generado automáticamente */

/* Reset básico */
* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    font-family: system-ui, -apple-system, sans-serif;
}}

/* Header crítico */
.{bem_prefix}-organism-header {{
    position: relative;
    z-index: 100;
}}

/* Hero crítico */
.{bem_prefix}-organism-hero {{
    min-height: 60vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* Tipografía crítica */
h1, h2, h3 {{
    margin: 0;
    font-weight: 700;
    line-height: 1.2;
}}

/* Botones críticos */
.{bem_prefix}-atom-button {{
    display: inline-block;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    text-decoration: none;
    cursor: pointer;
    transition: opacity 0.2s;
}}

.{bem_prefix}-atom-button:hover {{
    opacity: 0.9;
}}

/* Layout crítico */
.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
}}
"""
    
    with open(critical_css_path, 'w', encoding='utf-8') as f:
        f.write(critical_css)
    
    # Agregar inline critical CSS en functions.php
    functions_path = os.path.join(theme_dir, 'functions.php')
    if os.path.isfile(functions_path):
        with open(functions_path, 'r', encoding='utf-8') as f:
            functions_content = f.read()
        
        if 'critical_css_inline' not in functions_content:
            critical_php = f"""
// Inyectar Critical CSS inline
function {bem_prefix}_critical_css() {{
    $critical_path = get_theme_file_path('assets/css/critical.css');
    if (file_exists($critical_path)) {{
        $critical_css = file_get_contents($critical_path);
        echo '<style id="{bem_prefix}-critical-css">' . $critical_css . '</style>';
    }}
}}
add_action('wp_head', '{bem_prefix}_critical_css', 1);
"""
            functions_content += critical_php
            with open(functions_path, 'w', encoding='utf-8') as f:
                f.write(functions_content)


def setup_lazy_loading(theme_dir: str):
    """
    Configura lazy-loading mejorado para imágenes.
    """
    php_dir = os.path.join(theme_dir, 'php')
    os.makedirs(php_dir, exist_ok=True)
    
    lazy_loading_php = """<?php
/**
 * Sistema mejorado de lazy-loading para imágenes
 * 
 * @package img2html
 */

function img2html_lazy_load_images($content) {
    if (is_admin() || is_feed()) {
        return $content;
    }
    
    // Agregar loading="lazy" y decoding="async" a todas las imágenes
    $content = preg_replace_callback(
        '/<img([^>]+)>/i',
        function($matches) {
            $img_attrs = $matches[1];
            
            // Si ya tiene loading, no modificar
            if (strpos($img_attrs, 'loading=') !== false) {
                return $matches[0];
            }
            
            // Agregar loading="lazy" y decoding="async"
            $img_attrs .= ' loading="lazy" decoding="async"';
            
            return '<img' . $img_attrs . '>';
        },
        $content
    );
    
    // Agregar lazy-loading a imágenes en picture tags
    $content = preg_replace_callback(
        '/<picture([^>]*)>([\\s\\S]*?)<\\/picture>/i',
        function($matches) {
            $picture_content = $matches[2];
            
            // Agregar loading="lazy" a la img dentro del picture
            $picture_content = preg_replace(
                '/(<img[^>]+)(>)/i',
                '$1 loading="lazy" decoding="async"$2',
                $picture_content
            );
            
            return '<picture' . $matches[1] . '>' . $picture_content . '</picture>';
        },
        $content
    );
    
    return $content;
}
add_filter('the_content', 'img2html_lazy_load_images', 99);
add_filter('widget_text', 'img2html_lazy_load_images', 99);
"""
    
    lazy_path = os.path.join(php_dir, 'lazy-loading.php')
    with open(lazy_path, 'w', encoding='utf-8') as f:
        f.write(lazy_loading_php)


def create_build_script(theme_dir: str, css_framework: str):
    """
    Crea script de build completo.
    """
    build_script = os.path.join(theme_dir, 'build.sh')
    build_bat = os.path.join(theme_dir, 'build.bat')
    
    # Script bash para Linux/Mac
    build_sh = """#!/bin/bash
echo "🚀 Iniciando build del tema..."

# Instalar dependencias si no existen
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependencias..."
    npm install
fi

# Minificar CSS y JS
echo "🔨 Minificando assets..."
npm run minify

# Purga de CSS no usado
echo "🧹 Purgando CSS no usado..."
npm run purge

# Optimizar imágenes (requiere imagemin-cli)
if command -v imagemin &> /dev/null; then
    echo "🖼️  Optimizando imágenes..."
    imagemin assets/img/**/*.{jpg,png} --out-dir=assets/img-optimized
fi

echo "✅ Build completado!"
"""
    
    # Script batch para Windows
    build_bat_content = """@echo off
echo 🚀 Iniciando build del tema...

REM Instalar dependencias si no existen
if not exist "node_modules" (
    echo 📦 Instalando dependencias...
    call npm install
)

REM Minificar CSS y JS
echo 🔨 Minificando assets...
call npm run minify

REM Purga de CSS no usado
echo 🧹 Purgando CSS no usado...
call npm run purge

echo ✅ Build completado!
pause
"""
    
    with open(build_script, 'w', encoding='utf-8') as f:
        f.write(build_sh)
    
    with open(build_bat, 'w', encoding='utf-8') as f:
        f.write(build_bat_content)
    
    # Hacer ejecutable en Unix
    try:
        os.chmod(build_script, 0o755)
    except Exception:
        pass
