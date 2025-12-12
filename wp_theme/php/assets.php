<?php
if (!defined('ABSPATH')) { exit; }
function img2html_enqueue_assets(){
  $css = get_theme_file_uri('blocks.css');
  if ($css) { wp_enqueue_style('img2html-blocks', $css, [], null); }
}
add_action('wp_enqueue_scripts','img2html_enqueue_assets');
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
