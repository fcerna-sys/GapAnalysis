<?php
$title = isset($attributes['title']) ? $attributes['title'] : 'Título';
$text = isset($attributes['text']) ? $attributes['text'] : 'Descripción corta.';
$image = isset($attributes['imageUrl']) ? $attributes['imageUrl'] : '';
$btnText = isset($attributes['buttonText']) ? $attributes['buttonText'] : 'Ver más';
$btnUrl = isset($attributes['buttonUrl']) ? $attributes['buttonUrl'] : '#';
?>
<div class="wp-block-group img2html-card">
  <?php if ($image): ?>
    <figure class="wp-block-image img2html-card__imagen">
      <img src="<?php echo esc_url($image); ?>" alt="" />
    </figure>
  <?php endif; ?>
  <h3 class="img2html-card__titulo"><?php echo esc_html($title); ?></h3>
  <p class="img2html-card__texto"><?php echo esc_html($text); ?></p>
  <div class="wp-block-buttons img2html-card__acciones">
    <div class="wp-block-button img2html-button img2html-button__primary">
      <a class="wp-block-button__link" href="<?php echo esc_url($btnUrl); ?>"><?php echo esc_html($btnText); ?></a>
    </div>
  </div>
</div>
