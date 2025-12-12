<?php
$title = isset($attributes['title']) ? $attributes['title'] : 'Plan Básico';
$price = isset($attributes['price']) ? $attributes['price'] : '$19';
$features = isset($attributes['features']) && is_array($attributes['features']) ? $attributes['features'] : [];
$btnText = isset($attributes['buttonText']) ? $attributes['buttonText'] : 'Comprar';
$btnUrl = isset($attributes['buttonUrl']) ? $attributes['buttonUrl'] : '#';
$base = function_exists('img2html_bem') ? img2html_bem('pricing-feature') : 'img2html-pricing-feature';
?>
<div class="<?php echo esc_attr($base); ?>">
  <h3 class="<?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('pricing-feature','title') : $base.'__title'); ?>"><?php echo esc_html($title); ?></h3>
  <div class="<?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('pricing-feature','price') : $base.'__price'); ?>"><?php echo esc_html($price); ?></div>
  <?php if ($features): ?>
    <ul class="<?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('pricing-feature','list') : $base.'__list'); ?>">
      <?php foreach ($features as $f): ?>
        <li><?php echo esc_html($f); ?></li>
      <?php endforeach; ?>
    </ul>
  <?php endif; ?>
  <div class="wp-block-buttons <?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('pricing-feature','actions') : $base.'__actions'); ?>">
    <?php $btn_base = function_exists('img2html_bem') ? img2html_bem('button') : 'img2html-button'; $btn_primary = function_exists('img2html_bem') ? img2html_bem('button','primary') : 'img2html-button__primary'; ?>
    <div class="wp-block-button <?php echo esc_attr($btn_base.' '.$btn_primary); ?>">
      <a class="wp-block-button__link" href="<?php echo esc_url($btnUrl); ?>"><?php echo esc_html($btnText); ?></a>
    </div>
  </div>
</div>
