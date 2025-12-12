<?php
if (!defined('ABSPATH')) { exit; }

function img2html_localize_menu_locations(){
  if (!function_exists('get_registered_nav_menus')) return;
  $locations = get_registered_nav_menus(); // slug => label
  $data = [];
  foreach ($locations as $slug => $label){
    $data[] = [ 'label' => sanitize_text_field($label), 'value' => sanitize_key($slug) ];
  }
  $json = wp_json_encode($data);
  $script = 'window.IMG2HTML_MENU_LOCATIONS = '.$json.';';
  wp_add_inline_script('wp-blocks', $script, 'before');

  if (function_exists('get_nav_menu_locations')){
    $map = get_nav_menu_locations();
    $assign = [];
    if (is_array($map)){
      foreach ($map as $loc => $term_id){
        $name = '';
        if ($term_id){
          $obj = wp_get_nav_menu_object($term_id);
          if ($obj && isset($obj->name)) $name = sanitize_text_field($obj->name);
        }
        $assign[sanitize_key($loc)] = $name;
      }
    }
    $json2 = wp_json_encode($assign);
    $script2 = 'window.IMG2HTML_MENU_ASSIGNED = '.$json2.';';
    wp_add_inline_script('wp-blocks', $script2, 'before');
  }

  if (function_exists('wp_get_nav_menus')){
    $menus = wp_get_nav_menus();
    $list = [];
    foreach ($menus as $m){
      $list[] = [ 'label' => sanitize_text_field($m->name), 'value' => intval($m->term_id) ];
    }
    $json3 = wp_json_encode($list);
    $script3 = 'window.IMG2HTML_MENUS = '.$json3.';';
    wp_add_inline_script('wp-blocks', $script3, 'before');
  }
}
add_action('enqueue_block_editor_assets','img2html_localize_menu_locations');
