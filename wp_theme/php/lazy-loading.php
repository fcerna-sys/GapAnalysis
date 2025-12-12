<?php
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
        '/<picture([^>]*)>([\s\S]*?)<\/picture>/i',
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
