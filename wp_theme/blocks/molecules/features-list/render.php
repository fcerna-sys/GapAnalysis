<?php
$title = isset($attributes['title']) ? $attributes['title'] : 'Características';
$items = isset($attributes['items']) && is_array($attributes['items']) ? $attributes['items'] : [];
$prefix = function_exists('img2html_bem_prefix') ? img2html_bem_prefix() : 'img2html';
$base = $prefix.'-features-list';
?>
<div class="<?php echo esc_attr($base); ?>">
  <h3 class="<?php echo esc_attr($base.'__title'); ?>"><?php echo esc_html($title); ?></h3>
  <?php if ($items): ?>
    <ul class="<?php echo esc_attr($base.'__list'); ?>">
      <?php foreach ($items as $it): ?>
        <li class="<?php echo esc_attr($base.'__item'); ?>"><?php echo esc_html($it); ?></li>
      <?php endforeach; ?>
    </ul>
  <?php endif; ?>
</div>
