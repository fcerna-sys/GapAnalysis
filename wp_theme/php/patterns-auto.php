<?php
if (!defined('ABSPATH')) { exit; }

function img2html_auto_patterns_generate($max_len = 3){
  if (!current_user_can('manage_options')) return ['created'=>0,'skipped'=>0];
  $q = new WP_Query(['post_type'=>['page','post'],'post_status'=>'publish','posts_per_page'=>200,'no_found_rows'=>true]);
  $seq_counts = [];
  $seq_samples = [];
  $grp_counts = [];
  $grp_samples = [];
  if ($q->have_posts()){
    foreach ($q->posts as $p){
      $blocks = parse_blocks($p->post_content);
      $types = array_map(function($b){ return $b['blockName']; }, $blocks);
      for($i=0;$i<count($types);$i++){
        for($len=2;$len<=$max_len;$len++){
          if ($i+$len<=count($types)){
            $slice = array_slice($blocks,$i,$len);
            $sig = 'seq:'.implode('|', array_map(function($b){ return $b['blockName']; }, $slice));
            $seq_counts[$sig] = isset($seq_counts[$sig]) ? $seq_counts[$sig]+1 : 1;
            if (!isset($seq_samples[$sig])){ $seq_samples[$sig] = serialize_blocks($slice); }
          }
        }
      }
      foreach ($blocks as $b){
        if ($b['blockName'] === 'core/group' || $b['blockName'] === 'core/columns' || $b['blockName'] === 'core/cover'){
          $child_types = [];
          if (!empty($b['innerBlocks'])){
            foreach ($b['innerBlocks'] as $ib){ $child_types[] = $ib['blockName']; }
          }
          $sig = 'grp:'.$b['blockName'].':'.implode('|',$child_types);
          $grp_counts[$sig] = isset($grp_counts[$sig]) ? $grp_counts[$sig]+1 : 1;
          if (!isset($grp_samples[$sig])){ $grp_samples[$sig] = serialize_blocks([$b]); }
        }
      }
    }
  }
  $created = 0; $skipped = 0;
  $dir = get_theme_file_path('patterns');
  if (!is_dir($dir)) wp_mkdir_p($dir);
  $min = 2;
  foreach ($seq_counts as $sig=>$count){
    if ($count < $min) continue;
    $slug = 'auto-'.sanitize_key(str_replace(['seq:','/','|'],'-', $sig));
    $file = trailingslashit($dir).$slug.'.html';
    if (file_exists($file)) { $skipped++; continue; }
    $content = '<!-- wp:group {"layout":{"type":"constrained"}} -->'.$seq_samples[$sig].'<!-- /wp:group -->';
    file_put_contents($file, $content);
    $created++;
    register_block_pattern('img2html/'.$slug, [
      'title' => ucwords(str_replace(['core/','|','seq:'],' ', $sig)),
      'description' => 'Patrón automático',
      'content' => $content,
      'categories' => [function_exists('img2html_bem_prefix')?img2html_bem_prefix():'img2html']
    ]);
  }
  foreach ($grp_counts as $sig=>$count){
    if ($count < $min) continue;
    $slug = 'auto-'.sanitize_key(str_replace(['grp:','/','|',':'],'-', $sig));
    $file = trailingslashit($dir).$slug.'.html';
    if (file_exists($file)) { $skipped++; continue; }
    $content = $grp_samples[$sig];
    file_put_contents($file, $content);
    $created++;
    register_block_pattern('img2html/'.$slug, [
      'title' => ucwords(str_replace(['core/','|','grp:'],' ', $sig)),
      'description' => 'Patrón automático',
      'content' => $content,
      'categories' => [function_exists('img2html_bem_prefix')?img2html_bem_prefix():'img2html']
    ]);
  }
  arsort($seq_counts);
  arsort($grp_counts);
  $report = [
    'seq' => array_slice($seq_counts, 0, 25, true),
    'grp' => array_slice($grp_counts, 0, 25, true),
    'max_len' => intval($max_len),
    'time' => time(),
  ];
  update_option('img2html_auto_patterns_report', $report, false);
  return ['created'=>$created,'skipped'=>$skipped];
}

add_action('admin_post_img2html_generate_patterns', function(){
  if (!current_user_can('manage_options')) wp_die('');
  check_admin_referer('img2html_generate_patterns');
  $max_len = (!empty($_POST['len4'])) ? 4 : 3;
  $res = img2html_auto_patterns_generate($max_len);
  wp_redirect(add_query_arg(['page'=>'img2html_auto_patterns','created'=>$res['created'],'skipped'=>$res['skipped']], admin_url('themes.php')));
  exit;
});
