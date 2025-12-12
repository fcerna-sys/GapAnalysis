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
add_action('admin_init','img2html_generate_minified_assets');

function img2html_generate_minified_assets_once(){
  if (function_exists('get_option') && function_exists('update_option')){
    $done = get_option('img2html_min_assets_done');
    if ($done) return;
    img2html_generate_minified_assets();
    update_option('img2html_min_assets_done', time());
  }
}
add_action('init','img2html_generate_minified_assets_once');

add_filter('wp_resource_hints', function($hints, $relation_type){
  $extra = apply_filters('img2html_resource_hints', [
    'dns-prefetch' => [],
    'preconnect' => []
  ]);
  if ($relation_type === 'preconnect' && !empty($extra['preconnect'])){
    foreach ($extra['preconnect'] as $url){ $hints[] = $url; }
  }
  if ($relation_type === 'dns-prefetch' && !empty($extra['dns-prefetch'])){
    foreach ($extra['dns-prefetch'] as $url){ $hints[] = $url; }
  }
  return array_unique($hints);
}, 10, 2);

function img2html_disable_emojis(){
  remove_action('wp_head','print_emoji_detection_script',7);
  remove_action('admin_print_scripts','print_emoji_detection_script');
  remove_action('wp_print_styles','print_emoji_styles');
  remove_action('admin_print_styles','print_emoji_styles');
  remove_filter('the_content_feed','wp_staticize_emoji');
  remove_filter('comment_text_rss','wp_staticize_emoji');
  remove_filter('wp_mail','wp_staticize_emoji_for_email');
  add_filter('emoji_svg_url','__return_false');
}
add_action('init','img2html_disable_emojis');

function img2html_optimize_dashicons(){
  if (!is_admin() && !is_user_logged_in()){
    wp_deregister_style('dashicons');
  }
}
add_action('wp_enqueue_scripts','img2html_optimize_dashicons');

function img2html_assets_sizes(){
  $total = 0;
  $groups = [];
  $map = [
    'assets/css' => get_theme_file_path('assets/css'),
    'assets/components' => get_theme_file_path('assets/components'),
    'assets/blocks' => get_theme_file_path('assets/blocks')
  ];
  foreach ($map as $label=>$dir){
    $g_total = 0; $files = [];
    if (is_dir($dir)){
      foreach (glob($dir.'/*.css') as $f){
        $size = filesize($f);
        $g_total += $size; $total += $size;
        $rel = str_replace(get_theme_file_path(''), '', $f);
        $files[] = ['file'=>$rel, 'size'=>size_format($size, 2)];
      }
    }
    $groups[$label] = ['files'=>$files, 'total'=>size_format($g_total,2)];
  }
  return ['groups'=>$groups, 'total'=>size_format($total,2)];
}

add_action('admin_post_img2html_minify_assets', function(){
  if (!current_user_can('manage_options')) wp_die('');
  check_admin_referer('img2html_minify_assets');
  if (function_exists('img2html_generate_minified_assets')){
    img2html_generate_minified_assets();
  }
  wp_redirect(add_query_arg(['page'=>'img2html_performance','minified'=>1], admin_url('themes.php')));
  exit;
});

add_action('admin_post_img2html_purge_assets', function(){
  if (!current_user_can('manage_options')) wp_die('');
  check_admin_referer('img2html_purge_assets');
  $msg = '';
  $before = img2html_assets_sizes();
  $cwd = get_theme_file_path('');
  if (function_exists('shell_exec')){
    $cmd = 'npm run purge';
    $prev = getcwd(); chdir($cwd);
    $out = shell_exec($cmd.' 2>&1');
    chdir($prev);
    $msg = $out ? substr($out,0,200) : 'Sin salida';
  } else {
    $msg = 'shell_exec deshabilitado';
  }
  $after = img2html_assets_sizes();
  wp_redirect(add_query_arg([
    'page'=>'img2html_performance',
    'purged'=>1,
    'msg'=>$msg,
    'before'=>isset($before['total'])?$before['total']:'',
    'after'=>isset($after['total'])?$after['total']:'']
  , admin_url('themes.php')));
  exit;
});

add_action('admin_post_img2html_build_assets', function(){
  if (!current_user_can('manage_options')) wp_die('');
  check_admin_referer('img2html_build_assets');
  $msg = '';
  $cwd = get_theme_file_path('');
  if (function_exists('shell_exec')){
    $cmd = 'npm run build';
    $prev = getcwd(); chdir($cwd);
    $out = shell_exec($cmd.' 2>&1');
    chdir($prev);
    $msg = $out ? substr($out,0,200) : 'Sin salida';
  } else {
    $msg = 'shell_exec deshabilitado';
  }
  wp_redirect(add_query_arg(['page'=>'img2html_performance','built'=>1,'msg'=>$msg], admin_url('themes.php')));
  exit;
});
