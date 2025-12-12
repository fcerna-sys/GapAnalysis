<?php
$name = isset($attributes['name']) ? $attributes['name'] : 'Nombre';
$role = isset($attributes['role']) ? $attributes['role'] : 'Rol';
$avatar = isset($attributes['avatarUrl']) ? $attributes['avatarUrl'] : '';
$prefix = function_exists('img2html_bem_prefix') ? img2html_bem_prefix() : 'img2html';
$base = $prefix.'-team-member';
$extra = (isset($attributes['className']) && is_string($attributes['className'])) ? ' '.esc_attr($attributes['className']) : '';
?>
<div class="<?php echo esc_attr($base); ?><?php echo $extra; ?>">
  <div class="<?php echo esc_attr($base.'__header'); ?>">
    <?php if ($avatar): ?>
      <img class="<?php echo esc_attr($base.'__avatar'); ?>" src="<?php echo esc_url($avatar); ?>" alt="" />
    <?php endif; ?>
    <div class="<?php echo esc_attr($base.'__meta'); ?>">
      <strong class="<?php echo esc_attr($base.'__name'); ?>"><?php echo esc_html($name); ?></strong>
      <span class="<?php echo esc_attr($base.'__role'); ?>"><?php echo esc_html($role); ?></span>
    </div>
  </div>
</div>
