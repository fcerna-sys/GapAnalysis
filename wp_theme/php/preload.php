<?php
function img2html_preload_featured(){
  if (is_singular()){ 
    $src = get_the_post_thumbnail_url(get_the_ID(),'full');
    if ($src){
      echo '<link rel="preload" as="image" href="'.esc_url($src).'" imagesrcset="'.esc_attr(wp_get_attachment_image_srcset(get_post_thumbnail_id(), 'full')).'">';
    }
  }
}
add_action('wp_head','img2html_preload_featured',1);