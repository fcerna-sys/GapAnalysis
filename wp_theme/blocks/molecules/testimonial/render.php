<?php
$text = isset($attributes['text']) ? $attributes['text'] : 'Excelente servicio.';
$author = isset($attributes['author']) ? $attributes['author'] : 'Nombre';
$role = isset($attributes['role']) ? $attributes['role'] : 'Cargo';
$avatar = isset($attributes['avatarUrl']) ? $attributes['avatarUrl'] : '';
?>
<div class="img2html-testimonial">
  <div class="img2html-testimonial__header">
    <?php if ($avatar): ?>
      <img class="img2html-testimonial__avatar" src="<?php echo esc_url($avatar); ?>" alt="" />
    <?php endif; ?>
    <div class="img2html-testimonial__meta">
      <strong class="img2html-testimonial__author"><?php echo esc_html($author); ?></strong>
      <span class="img2html-testimonial__role"><?php echo esc_html($role); ?></span>
    </div>
  </div>
  <blockquote class="img2html-testimonial__text"><?php echo esc_html($text); ?></blockquote>
</div>
