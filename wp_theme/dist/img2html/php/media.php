<?php
function img2html_media_setup(){
  add_theme_support('post-thumbnails');
  add_image_size('featured-large',1200,630,true);
  add_image_size('gallery-thumb',600,600,true);
}
add_action('after_setup_theme','img2html_media_setup');

add_filter('wp_get_attachment_image_attributes', function($attr){
  $attr['decoding'] = 'async';
  if (!isset($attr['loading'])) $attr['loading'] = 'lazy';
  return $attr;
});

add_filter('render_block', function($content, $block){
  $name = isset($block['blockName']) ? $block['blockName'] : '';
  if ($name === 'img2html/organism-hero' && is_string($content)){
    $content = preg_replace('/<img(\s+)([^>]*?)>/', '<img$1fetchpriority="high" $2>', $content, 1);
  }
  return $content;
}, 9, 2);
