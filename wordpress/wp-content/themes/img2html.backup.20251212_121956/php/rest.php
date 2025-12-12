<?php
function img2html_register_rest_fields(){
  register_rest_field('post','featured_image',[
    'get_callback'=>function($obj){
      $id = isset($obj['id']) ? intval($obj['id']) : 0;
      return $id ? get_the_post_thumbnail_url($id,'full') : null;
    },
    'schema'=>['description'=>'Featured image URL']
  ]);
  register_rest_field('post','excerpt_plain',[
    'get_callback'=>function($obj){
      $id = isset($obj['id']) ? intval($obj['id']) : 0;
      return $id ? wp_strip_all_tags(get_the_excerpt($id)) : '';
    },
    'schema'=>['description'=>'Plain excerpt']
  ]);
}
add_action('rest_api_init','img2html_register_rest_fields');