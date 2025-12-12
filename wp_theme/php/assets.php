<?php
if (!defined('ABSPATH')) { exit; }
add_action('enqueue_block_editor_assets', function(){
  $css = get_theme_file_path('blocks.css');
  if (file_exists($css)){
    wp_enqueue_style('img2html-blocks-editor', get_theme_file_uri('blocks.css'), [], filemtime($css));
  }
});
if (function_exists('add_filter')){
  add_filter('should_load_block_assets_on_demand','__return_true');
}

// Helpers BEM con prefijo dinámico
if (!function_exists('img2html_bem_prefix')){
  function img2html_bem_prefix(){
    $theme = wp_get_theme();
    $td = $theme && method_exists($theme,'get') ? $theme->get('TextDomain') : '';
    $name = $theme && method_exists($theme,'get') ? $theme->get('Name') : '';
    $slug_raw = $td ?: $name;
    $slug = $slug_raw ? sanitize_key($slug_raw) : 'img2html';
    $slug = $slug ?: sanitize_title($slug_raw);
    if (!$slug) { error_log('img2html_bem_prefix: invalid theme slug'); return 'img2html'; }
    return apply_filters('img2html_bem_prefix', $slug ?: 'img2html');
  }
}

if (!function_exists('img2html_bem')){
  function img2html_bem($block, $element = '', $modifier = ''){
    $prefix = img2html_bem_prefix();
    $cls = $prefix.'-'.$block;
    if ($element){ $cls .= '__'.$element; }
    if ($modifier){ $cls .= '--'.$modifier; }
    return $cls;
  }
}
