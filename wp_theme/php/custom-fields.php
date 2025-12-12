<?php
if (!defined('ABSPATH')) { exit; }
function img2html_theme_settings_init(){
  register_setting('img2html_theme_settings','img2html_theme_options',[
    'type'=>'array',
    'sanitize_callback'=>function($input){
      $out = [];
      $out['contact_email'] = isset($input['contact_email']) ? sanitize_email($input['contact_email']) : '';
      $out['contact_phone'] = isset($input['contact_phone']) ? sanitize_text_field($input['contact_phone']) : '';
      $out['contact_address'] = isset($input['contact_address']) ? sanitize_text_field($input['contact_address']) : '';
      $out['facebook_url'] = isset($input['facebook_url']) ? esc_url_raw($input['facebook_url']) : '';
      $out['twitter_url'] = isset($input['twitter_url']) ? esc_url_raw($input['twitter_url']) : '';
      $out['instagram_url'] = isset($input['instagram_url']) ? esc_url_raw($input['instagram_url']) : '';
      $out['linkedin_url'] = isset($input['linkedin_url']) ? esc_url_raw($input['linkedin_url']) : '';
      return $out;
    }
  ]);
  add_settings_section('img2html_theme_contact','Contacto',function(){},'img2html-theme-settings');
  add_settings_field('img2html_contact_email','Email',function(){
    $opts = get_option('img2html_theme_options',[]);
    $v = isset($opts['contact_email']) ? $opts['contact_email'] : '';
    echo '<input type="email" name="img2html_theme_options[contact_email]" value="'.esc_attr($v).'" class="regular-text" />';
  },'img2html-theme-settings','img2html_theme_contact');
  add_settings_field('img2html_contact_phone','Teléfono',function(){
    $opts = get_option('img2html_theme_options',[]);
    $v = isset($opts['contact_phone']) ? $opts['contact_phone'] : '';
    echo '<input type="text" name="img2html_theme_options[contact_phone]" value="'.esc_attr($v).'" class="regular-text" />';
  },'img2html-theme-settings','img2html_theme_contact');
  add_settings_field('img2html_contact_address','Dirección',function(){
    $opts = get_option('img2html_theme_options',[]);
    $v = isset($opts['contact_address']) ? $opts['contact_address'] : '';
    echo '<input type="text" name="img2html_theme_options[contact_address]" value="'.esc_attr($v).'" class="regular-text" />';
  },'img2html-theme-settings','img2html_theme_contact');
  add_settings_section('img2html_theme_social','Redes',function(){},'img2html-theme-settings');
  add_settings_field('img2html_facebook_url','Facebook',function(){
    $opts = get_option('img2html_theme_options',[]);
    $v = isset($opts['facebook_url']) ? $opts['facebook_url'] : '';
    echo '<input type="url" name="img2html_theme_options[facebook_url]" value="'.esc_attr($v).'" class="regular-text" />';
  },'img2html-theme-settings','img2html_theme_social');
  add_settings_field('img2html_twitter_url','Twitter',function(){
    $opts = get_option('img2html_theme_options',[]);
    $v = isset($opts['twitter_url']) ? $opts['twitter_url'] : '';
    echo '<input type="url" name="img2html_theme_options[twitter_url]" value="'.esc_attr($v).'" class="regular-text" />';
  },'img2html-theme-settings','img2html_theme_social');
  add_settings_field('img2html_instagram_url','Instagram',function(){
    $opts = get_option('img2html_theme_options',[]);
    $v = isset($opts['instagram_url']) ? $opts['instagram_url'] : '';
    echo '<input type="url" name="img2html_theme_options[instagram_url]" value="'.esc_attr($v).'" class="regular-text" />';
  },'img2html-theme-settings','img2html_theme_social');
  add_settings_field('img2html_linkedin_url','LinkedIn',function(){
    $opts = get_option('img2html_theme_options',[]);
    $v = isset($opts['linkedin_url']) ? $opts['linkedin_url'] : '';
    echo '<input type="url" name="img2html_theme_options[linkedin_url]" value="'.esc_attr($v).'" class="regular-text" />';
  },'img2html-theme-settings','img2html_theme_social');
}
function img2html_theme_settings_page(){
  if (!current_user_can('manage_options')) return;
  echo '<div class="wrap"><h1>Ajustes del Tema</h1><form action="options.php" method="post">';
  settings_fields('img2html_theme_settings');
  do_settings_sections('img2html-theme-settings');
  submit_button('Guardar ajustes');
  echo '</form></div>';
}
function img2html_theme_settings_menu(){
  add_theme_page('Ajustes del Tema','Ajustes del Tema','manage_options','img2html-theme-settings','img2html_theme_settings_page');
}
function img2html_get_theme_option($key,$default=''){
  $opts = get_option('img2html_theme_options',[]);
  return isset($opts[$key]) ? $opts[$key] : $default;
}
add_action('admin_init','img2html_theme_settings_init');
add_action('admin_menu','img2html_theme_settings_menu');
