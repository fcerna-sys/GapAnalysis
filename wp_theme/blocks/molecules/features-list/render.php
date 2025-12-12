<?php
$title = isset($attributes['title']) ? $attributes['title'] : 'Características';
$items = isset($attributes['items']) && is_array($attributes['items']) ? $attributes['items'] : [];
$base = function_exists('img2html_bem') ? img2html_bem('features-list') : 'img2html-features-list';
?>
<div class="<?php echo esc_attr($base); ?>">
  <h3 class="<?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('features-list','title') : $base.'__title'); ?>"><?php echo esc_html($title); ?></h3>
  <?php if ($items): ?>
    <ul class="<?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('features-list','list') : $base.'__list'); }?>">
      <?php foreach ($items as $it): ?>
        <li class="<?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('features-list','item') : $base.'__item'); }?>"><?php echo esc_html($it); ?></li>
      <?php endforeach; ?>
    </ul>
  <?php endif; ?>
</div>
