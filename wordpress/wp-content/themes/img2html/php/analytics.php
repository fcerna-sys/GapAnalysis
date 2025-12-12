<?php
function img2html_analytics_head(){
  $gtag = defined('IMG2HTML_GTAG_ID') ? constant('IMG2HTML_GTAG_ID') : get_option('img2html_gtag_id');
  if (!$gtag) return;
  echo '<script async src="https://www.googletagmanager.com/gtag/js?id='.esc_attr($gtag).'"></script>';
  echo '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)};gtag("js",new Date());gtag("config","'.esc_js($gtag).'",{anonymize_ip:true});</script>';
}
add_action('wp_head','img2html_analytics_head',20);