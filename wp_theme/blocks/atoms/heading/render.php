<?php
$text = isset($attributes['text']) ? $attributes['text'] : 'Título';
$level = isset($attributes['level']) ? intval($attributes['level']) : 2;
if ($level < 1) $level = 1; if ($level > 6) $level = 6;
$align = isset($attributes['align']) ? $attributes['align'] : 'left';
$prefix = function_exists('img2html_bem_prefix') ? img2html_bem_prefix() : 'img2html';
$base = $prefix.'-heading';
$align_cls = $align === 'center' ? ' '.$base.'--center' : ($align === 'right' ? ' '.$base.'--right' : '');
$tag = 'h'.$level;
echo '<'.$tag.' class="'.$base.$align_cls.'">'.esc_html($text).'</'.$tag.'>';
