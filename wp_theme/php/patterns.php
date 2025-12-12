<?php
if (!defined('ABSPATH')) { exit; }
function img2html_register_patterns(){
  $prefix_raw = function_exists('img2html_bem_prefix') ? img2html_bem_prefix() : 'img2html';
  $prefix = sanitize_key($prefix_raw);
  if (!$prefix) { error_log('img2html_register_patterns: invalid prefix'); return; }
  $label = ucwords(str_replace('-', ' ', $prefix));
  register_block_pattern_category($prefix, ['label'=>sanitize_text_field($label)]);
  $dir = get_theme_file_path('patterns');
  if (!is_dir($dir)) return;
  $sections_slug = sanitize_key($prefix.'-sections');
  $label_sections = ucwords(str_replace('-', ' ', $sections_slug.' sections'));
  register_block_pattern_category($sections_slug, ['label'=>sanitize_text_field($label_sections)]);
  $files = array_merge(glob($dir.'/*.html'), glob($dir.'/*.php'));
  $registered_categories = [$prefix => true];
  foreach ($files as $file){
    $ext = pathinfo($file, PATHINFO_EXTENSION);
    $slug = sanitize_key(basename($file, '.'.$ext));
    $content_raw = file_get_contents($file);
    if (!$content_raw) continue;
    $title = ucwords(str_replace('-', ' ', $slug));
    $description = 'Patrón '.$prefix.': '.$title;
    $categories = [$prefix];
    if ($ext === 'php'){
      if (preg_match('/\*\s*Title:\s*(.*?)\n/s', $content_raw, $m)) $title = sanitize_text_field(trim($m[1]));
      if (preg_match('/\*\s*Description:\s*(.*?)\n/s', $content_raw, $m)) $description = sanitize_text_field(trim($m[1]));
      if (preg_match('/\*\s*Categories:\s*(.*?)\n/s', $content_raw, $m)){
        $cats = array_map('trim', preg_split('/[,\s]+/', trim($m[1])));
        $categories = array_filter(array_map('sanitize_key', $cats));
      }
      $content = preg_replace('/^<\?php[\s\S]*?\?>/','', $content_raw, 1);
    } else {
      $content = $content_raw;
    }
    $content = wp_kses_post($content);
    foreach ($categories as $cat){
      if ($cat && !isset($registered_categories[$cat])){
        $cat_slug = sanitize_key($cat);
        register_block_pattern_category($cat_slug, ['label'=>sanitize_text_field(ucwords(str_replace('-', ' ', $cat_slug)))]);
        $registered_categories[$cat] = true;
      }
    }
    register_block_pattern($prefix.'/'.$slug,[
      'title'=>sanitize_text_field($title),
      'description'=>sanitize_text_field($description),
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
    $exists = get_page_by_title(sanitize_text_field($title), OBJECT, 'wp_block');
    if ($exists) continue;
    wp_insert_post([
      'post_title'   => sanitize_text_field($title),
      'post_content' => wp_kses_post($content),
      'post_status'  => 'publish',
      'post_type'    => 'wp_block'
    ]);
  }
}
add_action('after_switch_theme','img2html_seed_synced_patterns');
