<?php
if (!defined('ABSPATH')) { exit; }
$email_attr = isset($attributes['email']) ? sanitize_email($attributes['email']) : '';
$phone_attr = isset($attributes['phone']) ? sanitize_text_field($attributes['phone']) : '';
$address_attr = isset($attributes['address']) ? sanitize_text_field($attributes['address']) : '';
if (function_exists('img2html_get_theme_option')){
  if (!$email_attr) { $email_attr = sanitize_email(img2html_get_theme_option('contact_email')); }
  if (!$phone_attr) { $phone_attr = sanitize_text_field(img2html_get_theme_option('contact_phone')); }
  if (!$address_attr) { $address_attr = sanitize_text_field(img2html_get_theme_option('contact_address')); }
}
$prefix = function_exists('img2html_bem_prefix') ? img2html_bem_prefix() : 'img2html';
$base = $prefix.'-contact-info';
?>
<div class="<?php echo esc_attr($base); ?>">
  <?php if ($email_attr): ?>
  <div class="<?php echo esc_attr($base.'__item'); ?>">
    <strong>Email:</strong> <a href="mailto:<?php echo esc_attr($email_attr); ?>" class="<?php echo esc_attr($base.'__link'); ?>"><?php echo esc_html($email_attr); ?></a>
  </div>
  <?php endif; ?>
  <?php if ($phone_attr): ?>
  <div class="<?php echo esc_attr($base.'__item'); ?>">
    <strong>Teléfono:</strong> <span class="<?php echo esc_attr($base.'__text'); ?>"><?php echo esc_html($phone_attr); ?></span>
  </div>
  <?php endif; ?>
  <?php if ($address_attr): ?>
  <div class="<?php echo esc_attr($base.'__item'); ?>">
    <strong>Dirección:</strong> <span class="<?php echo esc_attr($base.'__text'); ?>"><?php echo esc_html($address_attr); ?></span>
  </div>
  <?php endif; ?>
</div>

