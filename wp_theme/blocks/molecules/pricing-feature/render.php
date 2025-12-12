<?php
$title = isset($attributes['title']) ? $attributes['title'] : 'Plan Básico';
$price = isset($attributes['price']) ? $attributes['price'] : '$19';
$features = isset($attributes['features']) && is_array($attributes['features']) ? $attributes['features'] : [];
$btnText = isset($attributes['buttonText']) ? $attributes['buttonText'] : 'Comprar';
$btnUrl = isset($attributes['buttonUrl']) ? $attributes['buttonUrl'] : '#';
$prefix = function_exists('img2html_bem_prefix') ? img2html_bem_prefix() : 'img2html';
$base = $prefix.'-pricing-feature';
?>
<div class="<?php echo esc_attr($base); ?>">
  <h3 class="<?php echo esc_attr($base.'__title'); ?>"><?php echo esc_html($title); ?></h3>
  <div class="<?php echo esc_attr($base.'__price'); ?>"><?php echo esc_html($price); ?></div>
  <?php if ($features): ?>
    <ul class="<?php echo esc_attr($base.'__list'); ?>">
      <?php foreach ($features as $f): ?>
        <li><?php echo esc_html($f); ?></li>
      <?php endforeach; ?>
    </ul>
  <?php endif; ?>
  <div class="wp-block-buttons <?php echo esc_attr($base.'__actions'); ?>">
    <?php $btn_base = $prefix.'-button'; ?>
    <div class="wp-block-button <?php echo esc_attr($btn_base.' '.$btn_base.'__primary'); ?>">
      <a class="wp-block-button__link" href="<?php echo esc_url($btnUrl); ?>"><?php echo esc_html($btnText); ?></a>
    </div>
  </div>
</div>
