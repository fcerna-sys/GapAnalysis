<?php
$padding = isset($attributes['padding']) ? $attributes['padding'] : '1rem';
$background = isset($attributes['background']) ? $attributes['background'] : '';
$content = isset($attributes['content']) ? $attributes['content'] : '';
$style = 'padding:'.esc_attr($padding).';';
if ($background){ $style .= 'background:'.esc_attr($background).';'; }
echo '<div class="img2html-container" style="'.$style.'">'.wp_kses_post($content).'</div>';
