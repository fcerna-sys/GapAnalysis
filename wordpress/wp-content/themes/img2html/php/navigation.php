<?php
function img2html_register_menus(){
  register_nav_menus([
    'primary' => 'Primary Menu',
    'footer' => 'Footer Menu'
  ]);
}
add_action('after_setup_theme','img2html_register_menus');