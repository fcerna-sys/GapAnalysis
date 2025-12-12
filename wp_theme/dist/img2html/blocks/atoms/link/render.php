<?php
$text = isset($attributes['text']) ? $attributes['text'] : 'Leer más';
$url = isset($attributes['url']) ? $attributes['url'] : '#';
$target = isset($attributes['target']) ? $attributes['target'] : '';
$rel = isset($attributes['rel']) ? $attributes['rel'] : '';
$base = function_exists('img2html_bem') ? img2html_bem('link') : 'img2html-link';
$is_external = ($target === '_blank');
$cls = $base.($is_external ? ' '.$base.'--external' : '');
?>
<a class="<?php echo esc_attr($cls); ?>" href="<?php echo esc_url($url); ?>"<?php echo $target ? ' target="'.esc_attr($target).'"' : ''; ?><?php echo $rel ? ' rel="'.esc_attr($rel).'"' : ''; ?>><?php echo esc_html($text); ?></a>

