<?php
if (!defined('ABSPATH')) { exit; }
add_action('enqueue_block_editor_assets', function(){
  $dir = get_theme_file_path('docs');
  $list = [];
  if (is_dir($dir)){
    foreach (glob($dir.'/*.md') as $p){
      $name = basename($p);
      $list[] = ['label'=>sanitize_text_field($name), 'value'=>sanitize_text_field($name)];
    }
  }
  if (!$list){
    $list = [
      ['label'=>'THEME_GUIDE.md','value'=>'THEME_GUIDE.md'],
      ['label'=>'PATTERNS_GUIDE.md','value'=>'PATTERNS_GUIDE.md'],
      ['label'=>'EXTEND.md','value'=>'EXTEND.md'],
      ['label'=>'COMPOSE.md','value'=>'COMPOSE.md'],
      ['label'=>'STYLE.md','value'=>'STYLE.md']
    ];
  }
  $json = wp_json_encode($list);
  $script = 'window.IMG2HTML_DOCS = '.$json.';';
  wp_add_inline_script('wp-blocks', $script, 'before');
});
