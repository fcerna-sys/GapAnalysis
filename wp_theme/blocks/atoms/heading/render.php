<?php
$text = isset($attributes['text']) ? $attributes['text'] : 'Título';
$level = isset($attributes['level']) ? intval($attributes['level']) : 2;
if ($level < 1) $level = 1; if ($level > 6) $level = 6;
$align = isset($attributes['align']) ? $attributes['align'] : 'left';
$align_cls = $align === 'center' ? ' img2html-heading--center' : ($align === 'right' ? ' img2html-heading--right' : '');
$tag = 'h'.$level;
echo '<'.$tag.' class="img2html-heading'.$align_cls.'">'.esc_html($text).'</'.$tag.'>';
