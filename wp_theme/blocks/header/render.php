<?php
if (!defined('ABSPATH')) { exit; }
$sticky = !empty($attributes['sticky']);
$transparent = !empty($attributes['transparent']);
$dark = !empty($attributes['darkBackground']);
$align = isset($attributes['alignment']) ? sanitize_html_class($attributes['alignment']) : 'space-between';
$shadow = array_key_exists('shadow',$attributes) ? !empty($attributes['shadow']) : true;
$prefix = function_exists('img2html_bem_prefix') ? img2html_bem_prefix() : 'img2html';
$base = $prefix.'-header';
$classes = $base.' '.$base.'--justify-'.$align.($sticky?' '.$base.'--sticky':'').($transparent?' '.$base.'--transparent':'').($dark?' '.$base.'--dark':'').(($sticky && $shadow)?' '.$base.'--shadow':'');
?>
<header class="<?php echo esc_attr($classes); ?>">
  <div class="<?php echo esc_attr($base.'__inner'); ?>">
    <?php echo $content; ?>
  </div>
</header>
