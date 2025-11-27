<?php
function img2html_register_taxonomies(){
  register_taxonomy('project-type',['portfolio'],[
    'label'=>'Project Type',
    'public'=>true,
    'show_in_rest'=>true,
    'hierarchical'=>true
  ]);
  register_taxonomy('client',['portfolio'],[
    'label'=>'Client',
    'public'=>true,
    'show_in_rest'=>true,
    'hierarchical'=>false
  ]);
}
add_action('init','img2html_register_taxonomies');