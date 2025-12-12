<?php
function img2html_register_patterns(){
  register_block_pattern_category('img2html', ['label'=>'Img2HTML']);
  $dir = get_theme_file_path('patterns');
  if (!is_dir($dir)) return;
  register_block_pattern_category('img2html-sections', ['label'=>'Img2HTML Sections']);
  $files = array_merge(glob($dir.'/*.html'), glob($dir.'/*.php'));
  $registered_categories = ['img2html' => true];
  foreach ($files as $file){
    $ext = pathinfo($file, PATHINFO_EXTENSION);
    $slug = basename($file, '.'.$ext);
    $content_raw = file_get_contents($file);
    if (!$content_raw) continue;
    $title = ucwords(str_replace('-', ' ', $slug));
    $description = 'Patrón img2html: '.$title;
    $categories = ['img2html'];
    if ($ext === 'php'){
      if (preg_match('/\*\s*Title:\s*(.*?)\n/s', $content_raw, $m)) $title = trim($m[1]);
      if (preg_match('/\*\s*Description:\s*(.*?)\n/s', $content_raw, $m)) $description = trim($m[1]);
      if (preg_match('/\*\s*Categories:\s*(.*?)\n/s', $content_raw, $m)){
        $cats = array_map('trim', preg_split('/[,\s]+/', trim($m[1])));
        $categories = array_filter($cats);
      }
      $content = preg_replace('/^<\?php[\s\S]*?\?>/','', $content_raw, 1);
    } else {
      $content = $content_raw;
    }
    foreach ($categories as $cat){
      if ($cat && !isset($registered_categories[$cat])){
        register_block_pattern_category($cat, ['label'=>ucwords(str_replace('-', ' ', $cat))]);
        $registered_categories[$cat] = true;
      }
    }
    register_block_pattern('img2html/'.$slug,[
      'title'=>$title,
      'description'=>$description,
      'content'=>$content,
      'categories'=>$categories
    ]);
  }
}
add_action('init','img2html_register_patterns');

// Crear patrones sincronizados (reusable blocks) desde archivos prefijados 'synced-*.html'
function img2html_seed_synced_patterns(){
  $dir = get_theme_file_path('patterns');
  if (!is_dir($dir)) return;
  $files = array_merge(glob($dir.'/synced-*.html'), glob($dir.'/*.php'));
  foreach ($files as $file){
    $ext = pathinfo($file, PATHINFO_EXTENSION);
    $content_raw = file_get_contents($file);
    if (!$content_raw) continue;
    $is_php = ($ext === 'php');
    $sync_status = '';
    $title = '';
    if ($is_php){
      if (preg_match('/\*\s*Sync Status:\s*(.*?)\n/s', $content_raw, $m)) $sync_status = trim($m[1]);
      if (preg_match('/\*\s*Title:\s*(.*?)\n/s', $content_raw, $m)) $title = trim($m[1]);
    }
    if (!$is_php){
      $sync_status = 'synced';
    }
    if (strtolower($sync_status) !== 'synced') continue;
    $slug = basename($file, '.'.$ext);
    if (!$title) $title = ucwords(str_replace('-', ' ', $slug));
    $content = $is_php ? preg_replace('/^<\?php[\s\S]*?\?>/','', $content_raw, 1) : $content_raw;
    $exists = get_page_by_title($title, OBJECT, 'wp_block');
    if ($exists) continue;
    wp_insert_post([
      'post_title'   => $title,
      'post_content' => $content,
      'post_status'  => 'publish',
      'post_type'    => 'wp_block'
    ]);
  }
}
add_action('after_switch_theme','img2html_seed_synced_patterns');
