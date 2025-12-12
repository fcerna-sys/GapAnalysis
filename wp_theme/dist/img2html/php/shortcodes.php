<?php
function img2html_shortcode_render_pattern($atts){
  $slug = isset($atts['slug']) ? sanitize_key($atts['slug']) : '';
  if (!$slug) return '';
  $path = get_theme_file_path('patterns/'.$slug.'.html');
  return file_exists($path) ? file_get_contents($path) : '';
}
add_shortcode('img2html_pattern','img2html_shortcode_render_pattern');

function img2html_shortcode_breadcrumbs(){
  return img2html_shortcode_render_pattern(['slug'=>'breadcrumbs']);
}
add_shortcode('img2html_breadcrumbs','img2html_shortcode_breadcrumbs');