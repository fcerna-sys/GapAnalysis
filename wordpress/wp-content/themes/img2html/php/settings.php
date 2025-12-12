<?php
function img2html_register_settings(){
  register_setting('img2html_options','img2html_gtag_id',['type'=>'string','sanitize_callback'=>'sanitize_text_field']);
  add_settings_section('img2html_main','Img2HTML','__return_false','img2html');
  add_settings_field('img2html_gtag_id','Google Tag ID',function(){
    $val = get_option('img2html_gtag_id','');
    echo '<input type="text" name="img2html_gtag_id" value="'.esc_attr($val).'" class="regular-text">';
  },'img2html','img2html_main');
}
add_action('admin_init','img2html_register_settings');

function img2html_options_page(){
  echo '<div class="wrap"><h1>Img2HTML</h1><form method="post" action="options.php">';
  settings_fields('img2html_options');
  do_settings_sections('img2html');
  submit_button();
  echo '</form></div>';
}
function img2html_add_menu(){
  add_options_page('Img2HTML','Img2HTML','manage_options','img2html','img2html_options_page');
}
add_action('admin_menu','img2html_add_menu');