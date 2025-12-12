<?php
if (!defined('ABSPATH')) { exit; }
$title = isset($attributes['title']) ? sanitize_text_field($attributes['title']) : 'Nuestros Servicios';
$cols = isset($attributes['columns']) ? max(1, intval($attributes['columns'])) : 3;
$prefix = function_exists('img2html_bem_prefix') ? img2html_bem_prefix() : 'img2html';
$base = $prefix.'-cards-grid';
$classes = $base.' '.$base.'--cols-'.$cols;
?>
<div class="<?php echo esc_attr($classes); ?>">
  <h2 class="<?php echo esc_attr($base.'__title'); ?>"><?php echo esc_html($title); ?></h2>
  <div class="<?php echo esc_attr($base.'__container'); ?>">
    <?php echo $content; ?>
  </div>
</div>

