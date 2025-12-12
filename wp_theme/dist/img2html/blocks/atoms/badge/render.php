<?php
$text = isset($attributes['text']) ? $attributes['text'] : 'Nuevo';
$variant = isset($attributes['variant']) ? $attributes['variant'] : 'default';
$base = function_exists('img2html_bem') ? img2html_bem('badge') : 'img2html-badge';
$cls = $base.($variant ? ' '.$base.'--'.sanitize_title($variant) : '');
?>
<span class="<?php echo esc_attr($cls); ?>"><?php echo esc_html($text); ?></span>
