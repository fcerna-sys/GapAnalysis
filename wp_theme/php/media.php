<?php
function img2html_media_setup(){
  add_theme_support('post-thumbnails');
  add_image_size('featured-large',1200,630,true);
  add_image_size('gallery-thumb',600,600,true);
}
add_action('after_setup_theme','img2html_media_setup');