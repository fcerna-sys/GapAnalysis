<?php
if (!defined('ABSPATH')) { exit; }
$title = isset($attributes['title']) ? sanitize_text_field($attributes['title']) : '¿Listo para empezar?';
$text = isset($attributes['text']) ? sanitize_text_field($attributes['text']) : 'Únete hoy y mejora tu proyecto.';
$pText = isset($attributes['primaryButtonText']) ? sanitize_text_field($attributes['primaryButtonText']) : 'Comenzar';
$pUrl = isset($attributes['primaryButtonUrl']) ? esc_url($attributes['primaryButtonUrl']) : '#';
$sText = isset($attributes['secondaryButtonText']) ? sanitize_text_field($attributes['secondaryButtonText']) : 'Saber más';
$sUrl = isset($attributes['secondaryButtonUrl']) ? esc_url($attributes['secondaryButtonUrl']) : '#';
$showSecondary = !empty($attributes['showSecondaryButton']);
$align = isset($attributes['alignment']) ? sanitize_html_class($attributes['alignment']) : 'center';
$bg = isset($attributes['backgroundStyle']) ? sanitize_html_class($attributes['backgroundStyle']) : 'primary';
$prefix = function_exists('img2html_bem_prefix') ? img2html_bem_prefix() : 'img2html';
$base = $prefix.'-cta';
?>
<div class="<?php echo esc_attr($base.' '.$base.'--align-'.$align.' '.$base.'--bg-'.$bg); ?>">
  <div class="<?php echo esc_attr($base.'__wrapper'); ?>">
    <div class="<?php echo esc_attr($base.'__content'); ?>">
    <h2 class="<?php echo esc_attr($base.'__title'); ?>"><?php echo esc_html($title); ?></h2>
    <p class="<?php echo esc_attr($base.'__description'); ?>"><?php echo esc_html($text); ?></p>
    <div class="<?php echo esc_attr($base.'__actions'); ?>">
      <a href="<?php echo $pUrl; ?>" class="<?php echo esc_attr($base.'__button '.$base.'__button--primary'); ?>"><?php echo esc_html($pText); ?></a>
      <?php if ($showSecondary): ?>
      <a href="<?php echo $sUrl; ?>" class="<?php echo esc_attr($base.'__button '.$base.'__button--secondary'); ?>"><?php echo esc_html($sText); ?></a>
      <?php endif; ?>
    </div>
  </div>
</div>
</div>
