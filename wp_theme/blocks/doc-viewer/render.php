<?php
if (!defined('ABSPATH')) { exit; }
$file = isset($attributes['file']) ? sanitize_file_name($attributes['file']) : 'THEME_GUIDE.md';
$section = isset($attributes['section']) ? sanitize_text_field($attributes['section']) : '';
$show = !empty($attributes['showTitle']);
$base = function_exists('img2html_bem_prefix') ? img2html_bem_prefix() : 'img2html';
$cls = $base.'-doc-viewer';
$path = get_theme_file_path('docs/'.$file);
$content = '';
if (file_exists($path)){
  $raw = file_get_contents($path);
  if ($section){
    $lines = preg_split('/\r?\n/', $raw);
    $capture = false; $buf = [];
    foreach ($lines as $ln){
      if (preg_match('/^##\s+(.+)$/', $ln, $m)){
        $title = trim($m[1]);
        if (!$capture && strcasecmp($title, $section) === 0){ $capture = true; continue; }
        if ($capture && strcasecmp($title, $section) !== 0){ break; }
      }
      if ($capture){ $buf[] = $ln; }
    }
    $raw = $buf ? implode("\n", $buf) : $raw;
  }
  $md = $raw;
  $lines = preg_split('/\r?\n/', $md);
  $out = '';
  $in_list = false;
  $linkify = function($line){
    $result = '';
    $offset = 0;
    while (preg_match('/\[(.*?)\]\((https?:\/\/[^\s)]+)\)/', $line, $m, PREG_OFFSET_CAPTURE, $offset)){
      $start = $m[0][1];
      $before = substr($line, $offset, $start - $offset);
      $result .= esc_html($before);
      $text = esc_html($m[1][0]);
      $url = esc_url($m[2][0]);
      $result .= '<a href="'.$url.'" rel="noopener">'.$text.'</a>';
      $offset = $start + strlen($m[0][0]);
    }
    $result .= esc_html(substr($line, $offset));
    return $result;
  };
  foreach ($lines as $ln){
    $t = trim($ln);
    if ($t === ''){ if ($in_list){ /* keep */ } else { $out .= ''; } continue; }
    if (preg_match('/^#{1}\s+(.*)$/', $t, $m)){
      if ($in_list){ $out .= '</ul>'; $in_list = false; }
      $out .= '<h1>'.$linkify($m[1]).'</h1>';
      continue;
    }
    if (preg_match('/^#{2}\s+(.*)$/', $t, $m)){
      if ($in_list){ $out .= '</ul>'; $in_list = false; }
      $out .= '<h2>'.$linkify($m[1]).'</h2>';
      continue;
    }
    if (preg_match('/^#{3}\s+(.*)$/', $t, $m)){
      if ($in_list){ $out .= '</ul>'; $in_list = false; }
      $out .= '<h3>'.$linkify($m[1]).'</h3>';
      continue;
    }
    if (preg_match('/^-\s+(.*)$/', $t, $m)){
      if (!$in_list){ $out .= '<ul>'; $in_list = true; }
      $out .= '<li>'.$linkify($m[1]).'</li>';
      continue;
    }
    if ($in_list){ $out .= '</ul>'; $in_list = false; }
    $out .= '<p>'.$linkify($t).'</p>';
  }
  if ($in_list){ $out .= '</ul>'; }
  $allowed = [
    'h1' => [], 'h2' => [], 'h3' => [], 'p' => [], 'ul' => [], 'li' => [],
    'a' => ['href' => true, 'rel' => true]
  ];
  $content = wp_kses($out, $allowed);
}
?>
<div class="<?php echo esc_attr($cls); ?>">
  <?php if ($show) { ?><div class="<?php echo esc_attr($cls.'__title'); ?>"><?php echo esc_html($file.($section? ' — '.$section : '')); ?></div><?php } ?>
  <div class="<?php echo esc_attr($cls.'__content'); ?>"><?php echo $content; ?></div>
</div>
