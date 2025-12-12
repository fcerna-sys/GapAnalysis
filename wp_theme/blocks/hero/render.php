<?php
if (!defined('ABSPATH')) { exit; }
$title = isset($attributes['title']) ? sanitize_text_field($attributes['title']) : 'Título Principal';
$subtitle = isset($attributes['subtitle']) ? sanitize_text_field($attributes['subtitle']) : 'Subtítulo descriptivo';
$btnText = isset($attributes['buttonText']) ? sanitize_text_field($attributes['buttonText']) : 'Llamada a la acción';
$btnUrl = isset($attributes['buttonUrl']) ? esc_url($attributes['buttonUrl']) : '#';
$align = isset($attributes['align']) ? sanitize_html_class($attributes['align']) : 'center';
$sticky = !empty($attributes['sticky']);
$transparent = !empty($attributes['transparent']);
$dark = !empty($attributes['darkBackground']);
$prefix = function_exists('img2html_bem_prefix') ? img2html_bem_prefix() : 'img2html';
$base = $prefix.'-hero';
?>
<section class="<?php echo esc_attr($base.' '.$base.'--align-'.$align.($sticky?' '.$base.'--sticky':'').($transparent?' '.$base.'--transparent':'').($dark?' '.$base.'--dark':'')); ?>">
  <div class="<?php echo esc_attr($base.'__content'); ?>">
    <h1 class="<?php echo esc_attr($base.'__title'); ?>"><?php echo esc_html($title); ?></h1>
    <p class="<?php echo esc_attr($base.'__subtitle'); ?>"><?php echo esc_html($subtitle); ?></p>
    <a href="<?php echo $btnUrl; ?>" class="<?php echo esc_attr($base.'__button'); ?>"><?php echo esc_html($btnText); ?></a>
  </div>
</section>
