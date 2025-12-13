<?php
$text = isset($attributes['text']) ? $attributes['text'] : 'Acción';
$url = isset($attributes['url']) ? $attributes['url'] : '#';
$variant = isset($attributes['variant']) ? $attributes['variant'] : 'primary';
$prefix = function_exists('img2html_bem_prefix') ? img2html_bem_prefix() : 'img2html';
$base = $prefix.'-button';
$full = !empty($attributes['fullWidth']) ? ' '.$base.'--full' : '';
$cls = $base.' '.$base.'--'.sanitize_title($variant).$full;
echo '<div class="wp-block-button '.$cls.'"><a class="wp-block-button__link" href="'.esc_url($url).'">'.esc_html($text).'</a></div>';
