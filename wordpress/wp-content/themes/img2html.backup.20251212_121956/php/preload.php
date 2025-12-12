<?php
function img2html_preload_fonts(){
  $fonts_dir = get_theme_file_path('assets/fonts');
  if (!is_dir($fonts_dir)) return;
  foreach (glob($fonts_dir.'/*.woff2') as $font){
    $href = get_theme_file_uri('assets/fonts/'.basename($font));
    echo '<link rel="preload" href="'.esc_url($href).'" as="font" type="font/woff2" crossorigin>';
  }
}
add_action('wp_head','img2html_preload_fonts',1);

function img2html_preload_critical_css($html, $handle){
  $targets = [
    'assets/blocks/core-navigation.css',
    'assets/blocks/core-site-title.css'
  ];
  if (preg_match('/href="([^"]+)"/', $html, $m)){
    $href = $m[1];
    foreach ($targets as $t){
      if (strpos($href, $t) !== false){
        $preload = '<link rel="preload" href="'.esc_url($href).'" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">';
        $noscript = '<noscript>'.$html.'</noscript>';
        return $preload.$noscript;
      }
    }
  }
  return $html;
}
add_filter('style_loader_tag','img2html_preload_critical_css',10,2);
