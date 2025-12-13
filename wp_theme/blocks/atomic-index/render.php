<?php
if (!defined('ABSPATH')) { exit; }
$showAtoms = isset($attributes['showAtoms']) ? (bool)$attributes['showAtoms'] : true;
$showMolecules = isset($attributes['showMolecules']) ? (bool)$attributes['showMolecules'] : true;
$showOrganisms = isset($attributes['showOrganisms']) ? (bool)$attributes['showOrganisms'] : true;
$query = isset($attributes['query']) ? sanitize_text_field($attributes['query']) : '';
$limit = isset($attributes['limitPerGroup']) ? intval($attributes['limitPerGroup']) : 0;
$groups = array_filter([
  $showAtoms ? 'atoms' : null,
  $showMolecules ? 'molecules' : null,
  $showOrganisms ? 'organisms' : null,
]);
$base_dir = get_theme_file_path('blocks');
$bem_prefix = function_exists('img2html_bem_prefix') ? img2html_bem_prefix() : 'img2html';
$wrap_cls = $bem_prefix.'-atomic-index';
$tpl = isset($attributes['cardTemplate']) ? sanitize_key($attributes['cardTemplate']) : 'compact';
$wrap_cls .= $tpl ? ' '.$wrap_cls.'--'.$tpl : '';
$out = '';
foreach ($groups as $grp){
  $dir = $base_dir.'/'.$grp;
  if (!is_dir($dir)) continue;
  $items = [];
  $dirs = glob($dir.'/*', GLOB_ONLYDIR);
  foreach ($dirs as $bdir){
    $bj = $bdir.'/block.json';
    $slug = basename($bdir);
    $name = $slug;
    $block_name = 'img2html/'.($grp === 'atoms' ? 'atom-' : ($grp === 'molecules' ? 'molecule-' : 'organism-')).$slug;
    if (file_exists($bj)){
      $data = json_decode(file_get_contents($bj), true);
      if (is_array($data) && isset($data['title'])) $name = $data['title'];
      if (isset($data['name'])) $block_name = $data['name'];
    }
    $has_render = file_exists($bdir.'/render.php');
    $has_style = file_exists($bdir.'/style.css');
    if (!empty($attributes['onlyComplete']) && (!$has_render || !$has_style)) continue;
    if ($query){
      $hay = strtolower($name.' '.$slug.' '.$block_name);
      if (strpos($hay, strtolower($query)) === false) continue;
    }
    $mtime = file_exists($bj) ? filemtime($bj) : filemtime($bdir);
    $items[] = ['title'=>$name,'slug'=>$slug,'full'=>$block_name,'mtime'=>$mtime];
  }
  if (!$items) continue;
  if (!empty($attributes['order']) && $attributes['order'] === 'mtime'){
    usort($items, function($a,$b){ return $b['mtime'] <=> $a['mtime']; });
  } else {
    usort($items, function($a,$b){ return strcasecmp($a['title'], $b['title']); });
  }
  if ($limit > 0) $items = array_slice($items, 0, $limit);
  $out .= '<section class="'.$wrap_cls.'__section">';
  $out .= '<h2 class="'.$wrap_cls.'__heading">'.esc_html(ucfirst($grp)).'</h2>';
  $out .= '<div class="'.$wrap_cls.'__grid">';
  foreach ($items as $it){
    $out .= '<div class="'.$wrap_cls.'__card">';
    if (!isset($attributes['showTitle']) || $attributes['showTitle']){
      $title_src = isset($attributes['titleSource']) ? sanitize_key($attributes['titleSource']) : 'title';
      $display = $it['title'];
      if ($title_src === 'slug') $display = $it['slug'];
      if ($title_src === 'name') $display = $it['full'];
      $out .= '<div class="'.$wrap_cls.'__card-title">'.esc_html($display).'</div>';
      if (!empty($attributes['showSubtitleTechnical']) && $title_src === 'title'){
        $out .= '<div class="'.$wrap_cls.'__card-subtitle">'.esc_html($it['slug']).'</div>';
      }
    }
    if ($tpl !== 'minimal' && $it['full'] !== 'img2html/atomic-index'){
      $rendered = render_block([ 'blockName' => $it['full'], 'attrs' => [] ]);
      $out .= '<div class="'.$wrap_cls.'__card-body">'.$rendered.'</div>';
    }
    $out .= '</div>';
  }
  $out .= '</div>';
  $out .= '</section>';
}
echo '<div class="'.esc_attr($wrap_cls).'">'.$out.'</div>';
