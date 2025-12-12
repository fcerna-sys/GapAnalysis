<?php
$name = isset($attributes['name']) ? preg_replace('/[^a-z0-9-]/i','',$attributes['name']) : 'star';
$size = isset($attributes['size']) ? intval($attributes['size']) : 20;
$style = 'width:'.$size.'px;height:'.$size.'px;';
echo '<span class="img2html-icon img2html-icon__'.$name.'" style="'.esc_attr($style).'" aria-hidden="true"></span>';
