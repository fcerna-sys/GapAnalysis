<?php
$title = isset($attributes['title']) ? $attributes['title'] : 'Plan Básico';
$price = isset($attributes['price']) ? $attributes['price'] : '$19';
$features = isset($attributes['features']) && is_array($attributes['features']) ? $attributes['features'] : [];
$btnText = isset($attributes['buttonText']) ? $attributes['buttonText'] : 'Comprar';
$btnUrl = isset($attributes['buttonUrl']) ? $attributes['buttonUrl'] : '#';
?>
<div class="img2html-pricing-feature">
  <h3 class="img2html-pricing-feature__title"><?php echo esc_html($title); ?></h3>
  <div class="img2html-pricing-feature__price"><?php echo esc_html($price); ?></div>
  <?php if ($features): ?>
    <ul class="img2html-pricing-feature__list">
      <?php foreach ($features as $f): ?>
        <li><?php echo esc_html($f); ?></li>
      <?php endforeach; ?>
    </ul>
  <?php endif; ?>
  <div class="wp-block-buttons img2html-pricing-feature__actions">
    <div class="wp-block-button img2html-button img2html-button__primary">
      <a class="wp-block-button__link" href="<?php echo esc_url($btnUrl); ?>"><?php echo esc_html($btnText); ?></a>
    </div>
  </div>
</div>
