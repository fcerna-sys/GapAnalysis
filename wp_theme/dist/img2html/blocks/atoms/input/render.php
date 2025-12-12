<?php
$type = isset($attributes['type']) ? $attributes['type'] : 'text';
$placeholder = isset($attributes['placeholder']) ? $attributes['placeholder'] : '';
$value = isset($attributes['value']) ? $attributes['value'] : '';
$full = !empty($attributes['fullWidth']);
$base = function_exists('img2html_bem') ? img2html_bem('input') : 'img2html-input';
$cls = $base.($full ? ' '.$base.'--full' : '');
?>
<input class="<?php echo esc_attr($cls); ?>" type="<?php echo esc_attr($type); ?>" placeholder="<?php echo esc_attr($placeholder); ?>" value="<?php echo esc_attr($value); ?>" />
