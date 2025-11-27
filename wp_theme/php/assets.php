<?php
function img2html_enqueue_assets(){
  $css = get_theme_file_uri('blocks.css');
  if ($css) { wp_enqueue_style('img2html-blocks', $css, [], null); }
}
add_action('wp_enqueue_scripts','img2html_enqueue_assets');
if (function_exists('add_filter')){
  add_filter('should_load_block_assets_on_demand','__return_true');
}