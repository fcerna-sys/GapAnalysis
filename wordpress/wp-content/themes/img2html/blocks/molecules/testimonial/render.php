<?php
$text = isset($attributes['text']) ? $attributes['text'] : 'Excelente servicio.';
$author = isset($attributes['author']) ? $attributes['author'] : 'Nombre';
$role = isset($attributes['role']) ? $attributes['role'] : 'Cargo';
$avatar = isset($attributes['avatarUrl']) ? $attributes['avatarUrl'] : '';
$base = function_exists('img2html_bem') ? img2html_bem('testimonial') : 'img2html-testimonial';
?>
<div class="<?php echo esc_attr($base); ?>">
  <div class="<?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('testimonial','header') : $base.'__header'); ?>">
    <?php if ($avatar): ?>
      <img class="<?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('testimonial','avatar') : $base.'__avatar'); ?>" src="<?php echo esc_url($avatar); ?>" alt="" />
    <?php endif; ?>
    <div class="<?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('testimonial','meta') : $base.'__meta'); ?>">
      <strong class="<?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('testimonial','author') : $base.'__author'); ?>"><?php echo esc_html($author); ?></strong>
      <span class="<?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('testimonial','role') : $base.'__role'); ?>"><?php echo esc_html($role); ?></span>
    </div>
  </div>
  <blockquote class="<?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('testimonial','text') : $base.'__text'); ?>"><?php echo esc_html($text); ?></blockquote>
</div>
