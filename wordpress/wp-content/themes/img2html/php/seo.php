<?php
function img2html_basic_meta(){
  if (is_singular()){
    $title = wp_get_document_title();
    $desc = get_the_excerpt();
    echo '<meta property="og:title" content="'.esc_attr($title).'">';
    if ($desc){
      echo '<meta name="description" content="'.esc_attr(wp_strip_all_tags($desc)).'">';
    }
  }
}
add_action('wp_head','img2html_basic_meta');