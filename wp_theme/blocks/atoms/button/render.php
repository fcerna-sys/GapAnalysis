<?php
$text = isset($attributes['text']) ? $attributes['text'] : 'Acción';
$url = isset($attributes['url']) ? $attributes['url'] : '#';
$variant = isset($attributes['variant']) ? $attributes['variant'] : 'primary';
$full = !empty($attributes['fullWidth']) ? ' img2html-button--full' : '';
$cls = 'img2html-button img2html-button__'.$variant.$full;
echo '<div class="wp-block-button '.$cls.'"><a class="wp-block-button__link" href="'.esc_url($url).'">'.esc_html($text).'</a></div>';
