<?php
if (!defined('ABSPATH')) { exit; }

add_action('wp_nav_menu_item_custom_fields', function($item_id, $item){
  $icon  = get_post_meta($item_id, '_menu_icon', true);
  $badge = get_post_meta($item_id, '_menu_badge', true);
  $color = get_post_meta($item_id, '_menu_color', true);
  $title_alt = get_post_meta($item_id, '_menu_title_alt', true);
  $desc  = get_post_meta($item_id, '_menu_desc', true);
  $fs    = get_post_meta($item_id, '_menu_font_size', true);
  $fw    = get_post_meta($item_id, '_menu_font_weight', true);
  $ff    = get_post_meta($item_id, '_menu_font_family', true);
  $pad   = get_post_meta($item_id, '_menu_padding', true);
  $mega  = get_post_meta($item_id, '_menu_megamenu', true);
  $is_heading = get_post_meta($item_id, '_menu_is_heading', true);
  ?>
  <p class="description description-wide">
    <label>Icono (clase CSS)<br>
      <input type="text" name="menu_icon[<?php echo esc_attr($item_id); ?>]" value="<?php echo esc_attr($icon); ?>" />
    </label>
  </p>
  <p class="description description-wide">
    <label>Título alternativo<br>
      <input type="text" name="menu_title_alt[<?php echo esc_attr($item_id); ?>]" value="<?php echo esc_attr($title_alt); ?>" />
    </label>
  </p>
  <p class="description description-wide">
    <label>Descripción corta<br>
      <input type="text" name="menu_desc[<?php echo esc_attr($item_id); ?>]" value="<?php echo esc_attr($desc); ?>" />
    </label>
  </p>
  <p class="description description-wide">
    <label>Badge<br>
      <input type="text" name="menu_badge[<?php echo esc_attr($item_id); ?>]" value="<?php echo esc_attr($badge); ?>" />
    </label>
  </p>
  <p class="description description-wide">
    <label>Color del texto (CSS)<br>
      <input type="text" name="menu_color[<?php echo esc_attr($item_id); ?>]" value="<?php echo esc_attr($color); ?>" placeholder="#000000" />
    </label>
  </p>
  <p class="description description-wide">
    <label>Font Size<br>
      <input type="text" name="menu_font_size[<?php echo esc_attr($item_id); ?>]" value="<?php echo esc_attr($fs); ?>" placeholder="1rem" />
    </label>
  </p>
  <p class="description description-wide">
    <label>Font Weight<br>
      <input type="text" name="menu_font_weight[<?php echo esc_attr($item_id); ?>]" value="<?php echo esc_attr($fw); ?>" placeholder="600" />
    </label>
  </p>
  <p class="description description-wide">
    <label>Font Family<br>
      <input type="text" name="menu_font_family[<?php echo esc_attr($item_id); ?>]" value="<?php echo esc_attr($ff); ?>" placeholder="system-ui" />
    </label>
  </p>
  <p class="description description-wide">
    <label>Padding (CSS)<br>
      <input type="text" name="menu_padding[<?php echo esc_attr($item_id); ?>]" value="<?php echo esc_attr($pad); ?>" placeholder=".5rem 1rem" />
    </label>
  </p>
  <p class="description description-wide">
    <label><input type="checkbox" name="menu_megamenu[<?php echo esc_attr($item_id); ?>]" value="1" <?php checked($mega, '1'); ?>> Activar Mega Menú</label>
  </p>
  <p class="description description-wide">
    <label><input type="checkbox" name="menu_is_heading[<?php echo esc_attr($item_id); ?>]" value="1" <?php checked($is_heading, '1'); ?>> Marcar como encabezado de columna (mega)</label>
  </p>
  <?php
}, 10, 2);
