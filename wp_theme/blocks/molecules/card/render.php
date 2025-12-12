<?php
$title = isset($attributes['title']) ? $attributes['title'] : 'Título';
$text = isset($attributes['text']) ? $attributes['text'] : 'Descripción corta.';
$image = isset($attributes['imageUrl']) ? $attributes['imageUrl'] : '';
$btnText = isset($attributes['buttonText']) ? $attributes['buttonText'] : 'Ver más';
$btnUrl = isset($attributes['buttonUrl']) ? $attributes['buttonUrl'] : '#';
$prefix = function_exists('img2html_bem_prefix') ? img2html_bem_prefix() : 'img2html';
$base = $prefix.'-card';
?>
<div class="wp-block-group <?php echo esc_attr($base); ?>">
  <?php if ($image): ?>
    <figure class="wp-block-image <?php echo esc_attr($base.'__imagen'); ?>">
      <img src="<?php echo esc_url($image); ?>" alt="" />
    </figure>
  <?php endif; ?>
  <h3 class="<?php echo esc_attr($base.'__titulo'); ?>"><?php echo esc_html($title); ?></h3>
  <p class="<?php echo esc_attr($base.'__texto'); ?>"><?php echo esc_html($text); ?></p>
  <div class="wp-block-buttons <?php echo esc_attr($base.'__acciones'); ?>">
    <?php $btn_base = $prefix.'-button'; ?>
    <div class="wp-block-button <?php echo esc_attr($btn_base.' '.$btn_base.'__primary'); ?>">
      <a class="wp-block-button__link" href="<?php echo esc_url($btnUrl); ?>"><?php echo esc_html($btnText); ?></a>
    </div>
  </div>
</div>
