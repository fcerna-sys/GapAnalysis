<?php
function img2html_register_cpts(){
  register_post_type('portfolio',[
    'label'=>'Portfolio',
    'public'=>true,
    'show_in_rest'=>true,
    'supports'=>['title','editor','thumbnail','excerpt'],
    'has_archive'=>true
  ]);
  register_post_type('testimonial',[
    'label'=>'Testimonials',
    'public'=>true,
    'show_in_rest'=>true,
    'supports'=>['title','editor','thumbnail','excerpt'],
    'has_archive'=>true
  ]);
}
add_action('init','img2html_register_cpts');