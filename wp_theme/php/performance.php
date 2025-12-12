<?php
function img2html_minify_css($css){
  $css = preg_replace('/\/\*[\s\S]*?\*\//','',$css);
  $css = preg_replace('/\s+/',' ', $css);
  $css = preg_replace('/\s*([{};:,>])\s*/','\1', $css);
  $css = str_replace(';}', '}', $css);
  return trim($css);
}
function img2html_minify_js($js){
  $js = preg_replace('/(^|[^:])\/\/.*$/m','\1', $js);
  $js = preg_replace('/\/\*[\s\S]*?\*\//','', $js);
  $js = preg_replace('/\s+/',' ', $js);
  return trim($js);
}
function img2html_generate_minified_assets(){
  $base = get_theme_file_path('assets');
  if (!is_dir($base)) return;
  $dirs = [$base.'/blocks', $base.'/components'];
  foreach ($dirs as $dir){
    if (!is_dir($dir)) continue;
    foreach (glob($dir.'/*.css') as $file){
      $min = preg_replace('/\.css$/','.min.css',$file);
      if (!file_exists($min) || filemtime($file) > filemtime($min)){
        $raw = file_get_contents($file);
        if ($raw !== false){
          $out = img2html_minify_css($raw);
          file_put_contents($min, $out);
        }
      }
    }
    foreach (glob($dir.'/*.js') as $file){
      $min = preg_replace('/\.js$/','.min.js',$file);
      if (!file_exists($min) || filemtime($file) > filemtime($min)){
        $raw = file_get_contents($file);
        if ($raw !== false){
          $out = img2html_minify_js($raw);
          file_put_contents($min, $out);
        }
      }
    }
  }
}
add_action('after_switch_theme','img2html_generate_minified_assets');
