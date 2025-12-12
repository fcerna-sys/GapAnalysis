<?php
$text = isset($attributes['text']) ? $attributes['text'] : 'Texto del párrafo';
$align = isset($attributes['align']) ? $attributes['align'] : 'left';
$prefix = function_exists('img2html_bem_prefix') ? img2html_bem_prefix() : 'img2html';
$base = $prefix.'-paragraph';
$align_cls = $align === 'center' ? ' '.$base.'--center' : ($align === 'right' ? ' '.$base.'--right' : '');
echo '<p class="'.$base.$align_cls.'">'.esc_html($text).'</p>';
