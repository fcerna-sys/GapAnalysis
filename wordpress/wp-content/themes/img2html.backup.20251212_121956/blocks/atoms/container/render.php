<?php
$padding = isset($attributes['padding']) ? $attributes['padding'] : '1rem';
$background = isset($attributes['background']) ? $attributes['background'] : '';
$content = isset($attributes['content']) ? $attributes['content'] : '';
$style = 'padding:'.esc_attr($padding).';';
if ($background){ $style .= 'background:'.esc_attr($background).';'; }
$prefix = function_exists('img2html_bem_prefix') ? img2html_bem_prefix() : 'img2html';
$base = $prefix.'-container';
echo '<div class="'.$base.'" style="'.$style.'">'.wp_kses_post($content).'</div>';
