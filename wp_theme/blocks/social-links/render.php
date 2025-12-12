<?php
if (!defined('ABSPATH')) { exit; }
$fb = isset($attributes['facebook']) ? esc_url($attributes['facebook']) : '';
$tw = isset($attributes['twitter']) ? esc_url($attributes['twitter']) : '';
$ig = isset($attributes['instagram']) ? esc_url($attributes['instagram']) : '';
$in = isset($attributes['linkedin']) ? esc_url($attributes['linkedin']) : '';
if (function_exists('img2html_get_theme_option')){
  if (!$fb) { $fb = esc_url(img2html_get_theme_option('facebook_url')); }
  if (!$tw) { $tw = esc_url(img2html_get_theme_option('twitter_url')); }
  if (!$ig) { $ig = esc_url(img2html_get_theme_option('instagram_url')); }
  if (!$in) { $in = esc_url(img2html_get_theme_option('linkedin_url')); }
}
$prefix = function_exists('img2html_bem_prefix') ? img2html_bem_prefix() : 'img2html';
$base = $prefix.'-social-links';
?>
<ul class="<?php echo esc_attr($base); ?>">
  <?php if ($fb): ?><li class="<?php echo esc_attr($base.'__item'); ?>"><a href="<?php echo $fb; ?>" target="_blank" rel="noopener" class="<?php echo esc_attr($base.'__link'); ?>">Facebook</a></li><?php endif; ?>
  <?php if ($tw): ?><li class="<?php echo esc_attr($base.'__item'); ?>"><a href="<?php echo $tw; ?>" target="_blank" rel="noopener" class="<?php echo esc_attr($base.'__link'); ?>">Twitter</a></li><?php endif; ?>
  <?php if ($ig): ?><li class="<?php echo esc_attr($base.'__item'); ?>"><a href="<?php echo $ig; ?>" target="_blank" rel="noopener" class="<?php echo esc_attr($base.'__link'); ?>">Instagram</a></li><?php endif; ?>
  <?php if ($in): ?><li class="<?php echo esc_attr($base.'__item'); ?>"><a href="<?php echo $in; ?>" target="_blank" rel="noopener" class="<?php echo esc_attr($base.'__link'); ?>">LinkedIn</a></li><?php endif; ?>
</ul>

