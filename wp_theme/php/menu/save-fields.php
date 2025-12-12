<?php
if (!defined('ABSPATH')) { exit; }

add_action('wp_update_nav_menu_item', function($menu_id, $menu_item_db_id){
  if (isset($_POST['menu_icon'][$menu_item_db_id])){
    update_post_meta($menu_item_db_id, '_menu_icon', sanitize_text_field($_POST['menu_icon'][$menu_item_db_id]));
  }
  if (isset($_POST['menu_badge'][$menu_item_db_id])){
    update_post_meta($menu_item_db_id, '_menu_badge', sanitize_text_field($_POST['menu_badge'][$menu_item_db_id]));
  }
  if (isset($_POST['menu_color'][$menu_item_db_id])){
    update_post_meta($menu_item_db_id, '_menu_color', sanitize_hex_color($_POST['menu_color'][$menu_item_db_id]));
  }
  if (isset($_POST['menu_title_alt'][$menu_item_db_id])){
    update_post_meta($menu_item_db_id, '_menu_title_alt', sanitize_text_field($_POST['menu_title_alt'][$menu_item_db_id]));
  }
  if (isset($_POST['menu_desc'][$menu_item_db_id])){
    update_post_meta($menu_item_db_id, '_menu_desc', sanitize_text_field($_POST['menu_desc'][$menu_item_db_id]));
  }
  if (isset($_POST['menu_font_size'][$menu_item_db_id])){
    update_post_meta($menu_item_db_id, '_menu_font_size', sanitize_text_field($_POST['menu_font_size'][$menu_item_db_id]));
  }
  if (isset($_POST['menu_font_weight'][$menu_item_db_id])){
    update_post_meta($menu_item_db_id, '_menu_font_weight', sanitize_text_field($_POST['menu_font_weight'][$menu_item_db_id]));
  }
  if (isset($_POST['menu_font_family'][$menu_item_db_id])){
    update_post_meta($menu_item_db_id, '_menu_font_family', sanitize_text_field($_POST['menu_font_family'][$menu_item_db_id]));
  }
  if (isset($_POST['menu_padding'][$menu_item_db_id])){
    update_post_meta($menu_item_db_id, '_menu_padding', sanitize_text_field($_POST['menu_padding'][$menu_item_db_id]));
  }
  $mega = isset($_POST['menu_megamenu'][$menu_item_db_id]) ? '1' : '';
  update_post_meta($menu_item_db_id, '_menu_megamenu', $mega);
  $is_heading = isset($_POST['menu_is_heading'][$menu_item_db_id]) ? '1' : '';
  update_post_meta($menu_item_db_id, '_menu_is_heading', $is_heading);
}, 10, 2);
