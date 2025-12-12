<?php
$text = isset($attributes['text']) ? $attributes['text'] : 'Título';
$level = isset($attributes['level']) ? intval($attributes['level']) : 2;
if ($level < 1) $level = 1; if ($level > 6) $level = 6;
$align = isset($attributes['align']) ? $attributes['align'] : 'left';
$base = function_exists('img2html_bem') ? img2html_bem('heading') : 'img2html-heading';
$align_cls = $align === 'center' ? ' '.$base.'--center' : ($align === 'right' ? ' '.$base.'--right' : '');
$tag = 'h'.$level;
echo '<'.$tag.' class="'.$base.$align_cls.'">'.esc_html($text).'</'.$tag.'>';
