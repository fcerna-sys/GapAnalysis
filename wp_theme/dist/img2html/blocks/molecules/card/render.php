<?php
$title = isset($attributes['title']) ? $attributes['title'] : 'Título';
$text = isset($attributes['text']) ? $attributes['text'] : 'Descripción corta.';
$image = isset($attributes['imageUrl']) ? $attributes['imageUrl'] : '';
$btnText = isset($attributes['buttonText']) ? $attributes['buttonText'] : 'Ver más';
$btnUrl = isset($attributes['buttonUrl']) ? $attributes['buttonUrl'] : '#';
$base = function_exists('img2html_bem') ? img2html_bem('card') : 'img2html-card';
?>
<div class="wp-block-group <?php echo esc_attr($base); ?>">
  <?php if ($image): ?>
    <figure class="wp-block-image <?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('card','imagen') : $base.'__imagen'); ?>">
      <img src="<?php echo esc_url($image); ?>" alt="" />
    </figure>
  <?php endif; ?>
  <h3 class="<?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('card','titulo') : $base.'__titulo'); ?>"><?php echo esc_html($title); ?></h3>
  <p class="<?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('card','texto') : $base.'__texto'); ?>"><?php echo esc_html($text); ?></p>
  <div class="wp-block-buttons <?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('card','acciones') : $base.'__acciones'); ?>">
    <?php $btn_base = function_exists('img2html_bem') ? img2html_bem('button') : 'img2html-button'; $btn_primary = function_exists('img2html_bem') ? img2html_bem('button','primary') : 'img2html-button__primary'; ?>
    <div class="wp-block-button <?php echo esc_attr($btn_base.' '.$btn_primary); ?>">
      <a class="wp-block-button__link" href="<?php echo esc_url($btnUrl); ?>"><?php echo esc_html($btnText); ?></a>
    </div>
  </div>
</div>
