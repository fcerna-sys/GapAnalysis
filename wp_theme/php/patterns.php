<?php
function img2html_register_patterns(){
  register_block_pattern_category('img2html', ['label'=>'Img2HTML']);
  $dir = get_theme_file_path('patterns');
  if (!is_dir($dir)) return;
  foreach (glob($dir.'/*.html') as $file){
    $slug = basename($file, '.html');
    register_block_pattern('img2html/'.$slug,[
      'title'=>ucwords(str_replace('-', ' ', $slug)),
      'content'=>file_get_contents($file)
    ]);
  }
}
add_action('init','img2html_register_patterns');