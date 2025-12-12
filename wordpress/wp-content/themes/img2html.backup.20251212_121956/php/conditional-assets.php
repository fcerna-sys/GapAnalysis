<?php
/**
 * Sistema de carga condicional de assets por bloque
 * Solo carga CSS/JS de bloques que están presentes en el contenido
 * 
 * @package img2html
 */

function img2html_conditional_block_assets() {
    $manifest_path = get_theme_file_path('blocks-manifest.php');
    if (!file_exists($manifest_path)) {
        return;
    }
    
    $manifest = include $manifest_path;
    if (!is_array($manifest)) {
        return;
    }
    
    // En el editor, cargar todos los assets
    if (is_admin() || (defined('REST_REQUEST') && REST_REQUEST)) {
        foreach ($manifest as $block_name => $assets) {
            if (isset($assets['style'])) {
                foreach ((array)$assets['style'] as $style_path) {
                    $full_path = get_theme_file_path($style_path);
                    if (file_exists($full_path)) {
                        $handle = 'img2html-block-' . md5($block_name . $style_path);
                        $uri = get_theme_file_uri($style_path);
                        $version = filemtime($full_path);
                        wp_enqueue_style($handle, $uri, [], $version);
                    }
                }
            }
            if (isset($assets['script'])) {
                foreach ((array)$assets['script'] as $script_path) {
                    $full_path = get_theme_file_path($script_path);
                    if (file_exists($full_path)) {
                        $handle = 'img2html-block-' . md5($block_name . $script_path);
                        $uri = get_theme_file_uri($script_path);
                        $version = filemtime($full_path);
                        wp_enqueue_script($handle, $uri, [], $version, true);
                    }
                }
            }
        }
        return;
    }
    
    // En el front-end, cargar solo bloques usados
    add_filter('render_block', function($content, $block) use ($manifest) {
        $block_name = isset($block['blockName']) ? $block['blockName'] : null;
        if (!$block_name || !isset($manifest[$block_name])) {
            return $content;
        }
        
        $assets = $manifest[$block_name];
        
        // Cargar CSS
        if (isset($assets['style'])) {
            foreach ((array)$assets['style'] as $style_path) {
                $full_path = get_theme_file_path($style_path);
                if (file_exists($full_path)) {
                    $handle = 'img2html-block-' . md5($block_name . $style_path);
                    if (!wp_style_is($handle, 'enqueued')) {
                        $uri = get_theme_file_uri($style_path);
                        $version = filemtime($full_path);
                        wp_enqueue_style($handle, $uri, [], $version);
                    }
                }
            }
        }
        
        // Cargar JS
        if (isset($assets['script'])) {
            foreach ((array)$assets['script'] as $script_path) {
                $full_path = get_theme_file_path($script_path);
                if (file_exists($full_path)) {
                    $handle = 'img2html-block-' . md5($block_name . $script_path);
                    if (!wp_script_is($handle, 'enqueued')) {
                        $uri = get_theme_file_uri($script_path);
                        $version = filemtime($full_path);
                        wp_enqueue_script($handle, $uri, [], $version, true);
                    }
                }
            }
        }
        
        return $content;
    }, 10, 2);
}
add_action('init', 'img2html_conditional_block_assets');
