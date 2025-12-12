<?php
function img2html_register_patterns(){
  register_block_pattern_category('img2html', ['label'=>'Img2HTML']);
  $dir = get_theme_file_path('patterns');
  if (!is_dir($dir)) return;
  foreach (glob($dir.'/*.html') as $file){
    $slug = basename($file, '.html');
    $title = ucwords(str_replace('-', ' ', $slug));
    register_block_pattern('img2html/'.$slug,[
      'title'=>$title,
      'description'=>'Patrón img2html: '.$title,
      'content'=>file_get_contents($file)
    ]);
  }
}
add_action('init','img2html_register_patterns');

// Crear patrones sincronizados (reusable blocks) desde archivos prefijados 'synced-*.html'
function img2html_seed_synced_patterns(){
  $dir = get_theme_file_path('patterns');
  if (!is_dir($dir)) return;
  $synced = glob($dir.'/synced-*.html');
  foreach ($synced as $file){
    $slug = basename($file, '.html');
    $title = ucwords(str_replace('-', ' ', $slug));
    $content = file_get_contents($file);
    if (!$content) continue;
    $exists = get_page_by_title($title, OBJECT, 'wp_block');
    if ($exists) continue;
    $post_id = wp_insert_post([
      'post_title'   => $title,
      'post_content' => $content,
      'post_status'  => 'publish',
      'post_type'    => 'wp_block'
    ]);
  }
}
add_action('after_switch_theme','img2html_seed_synced_patterns');
