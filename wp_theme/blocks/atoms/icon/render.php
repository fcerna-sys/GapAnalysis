<?php
$name = isset($attributes['name']) ? preg_replace('/[^a-z0-9-]/i','',$attributes['name']) : 'star';
$size = isset($attributes['size']) ? intval($attributes['size']) : 20;
$style = 'width:'.$size.'px;height:'.$size.'px;';
$prefix = function_exists('img2html_bem_prefix') ? img2html_bem_prefix() : 'img2html';
$base = $prefix.'-icon';
echo '<span class="'.$base.' '.$base.'__'.$name.'" style="'.esc_attr($style).'" aria-hidden="true"></span>';
