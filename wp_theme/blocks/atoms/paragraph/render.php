<?php
$text = isset($attributes['text']) ? $attributes['text'] : 'Texto del párrafo';
$align = isset($attributes['align']) ? $attributes['align'] : 'left';
$align_cls = $align === 'center' ? ' img2html-paragraph--center' : ($align === 'right' ? ' img2html-paragraph--right' : '');
echo '<p class="img2html-paragraph'.$align_cls.'">'.esc_html($text).'</p>';
