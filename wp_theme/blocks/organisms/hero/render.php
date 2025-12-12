<?php
$title = isset($attributes['title']) ? $attributes['title'] : 'Título destacado';
$subtitle = isset($attributes['subtitle']) ? $attributes['subtitle'] : 'Subtítulo breve';
$btnText = isset($attributes['buttonText']) ? $attributes['buttonText'] : 'Empezar';
$btnUrl = isset($attributes['buttonUrl']) ? $attributes['buttonUrl'] : '#';
$prefix = function_exists('img2html_bem_prefix') ? img2html_bem_prefix() : 'img2html';
$base = $prefix.'-hero';
$btn_base = $prefix.'-button';
?>
<section class="<?php echo esc_attr($base); ?>">
  <h1 class="<?php echo esc_attr($base.'__title'); ?>"><?php echo esc_html($title); ?></h1>
  <p class="<?php echo esc_attr($base.'__subtitle'); ?>"><?php echo esc_html($subtitle); ?></p>
  <div class="wp-block-buttons <?php echo esc_attr($base.'__actions'); ?>">
    <div class="wp-block-button <?php echo esc_attr($btn_base.' '.$btn_base.'__primary'); ?>">
      <a class="wp-block-button__link" href="<?php echo esc_url($btnUrl); ?>"><?php echo esc_html($btnText); ?></a>
    </div>
  </div>
</section>
