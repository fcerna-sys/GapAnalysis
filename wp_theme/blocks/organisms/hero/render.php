<?php
$title = isset($attributes['title']) ? $attributes['title'] : 'Título destacado';
$subtitle = isset($attributes['subtitle']) ? $attributes['subtitle'] : 'Subtítulo breve';
$btnText = isset($attributes['buttonText']) ? $attributes['buttonText'] : 'Empezar';
$btnUrl = isset($attributes['buttonUrl']) ? $attributes['buttonUrl'] : '#';
$prefix = function_exists('img2html_bem_prefix') ? img2html_bem_prefix() : 'img2html';
$base = function_exists('img2html_bem') ? img2html_bem('hero') : 'img2html-hero';
$btn_base = function_exists('img2html_bem_prefix') ? img2html_bem_prefix().'-button' : 'img2html-button';
?>
<section class="<?php echo esc_attr($base); ?>">
  <h1 class="<?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('hero','title') : $base.'__title'); ?>"><?php echo esc_html($title); ?></h1>
  <p class="<?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('hero','subtitle') : $base.'__subtitle'); ?>"><?php echo esc_html($subtitle); ?></p>
  <div class="wp-block-buttons <?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('hero','actions') : $base.'__actions'); ?>">
    <div class="wp-block-button <?php echo esc_attr($btn_base.' '.$btn_base.'__primary'); ?>">
      <a class="wp-block-button__link" href="<?php echo esc_url($btnUrl); ?>"><?php echo esc_html($btnText); ?></a>
    </div>
  </div>
</section>
