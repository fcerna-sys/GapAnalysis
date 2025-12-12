<?php
if (!defined('ABSPATH')) { exit; }
$cols = isset($attributes['columns']) ? max(1, intval($attributes['columns'])) : 3;
$dark = !empty($attributes['darkBackground']);
$prefix = function_exists('img2html_bem_prefix') ? img2html_bem_prefix() : 'img2html';
$base = $prefix.'-footer';
$classes = $base.' '.$base.'--cols-'.$cols.($dark?' '.$base.'--dark':'');
?>
<footer class="<?php echo esc_attr($classes); ?>">
  <div class="<?php echo esc_attr($base.'__inner'); ?>">
    <?php echo $content; ?>
  </div>
</footer>
