<?php
if (!defined('ABSPATH')) { exit; }
$title = isset($attributes['title']) ? sanitize_text_field($attributes['title']) : 'Título';
$text = isset($attributes['text']) ? sanitize_text_field($attributes['text']) : 'Descripción corta.';
$img = isset($attributes['imageUrl']) ? esc_url($attributes['imageUrl']) : '';
$btnText = isset($attributes['buttonText']) ? sanitize_text_field($attributes['buttonText']) : 'Ver más';
$btnUrl = isset($attributes['buttonUrl']) ? esc_url($attributes['buttonUrl']) : '#';
$prefix = function_exists('img2html_bem_prefix') ? img2html_bem_prefix() : 'img2html';
$base = $prefix.'-card';
?>
<article class="<?php echo esc_attr($base); ?>">
  <?php if ($img): ?>
  <img src="<?php echo $img; ?>" alt="" class="<?php echo esc_attr($base.'__image'); ?>" loading="lazy">
  <?php endif; ?>
  <div class="<?php echo esc_attr($base.'__body'); ?>">
    <h3 class="<?php echo esc_attr($base.'__title'); ?>"><?php echo esc_html($title); ?></h3>
    <p class="<?php echo esc_attr($base.'__text'); ?>"><?php echo esc_html($text); ?></p>
    <a href="<?php echo $btnUrl; ?>" class="<?php echo esc_attr($base.'__button'); ?>"><?php echo esc_html($btnText); ?></a>
  </div>
</article>
