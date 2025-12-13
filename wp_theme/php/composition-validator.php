<?php
if (!defined('ABSPATH')) { exit; }

function img2html_is_atom($name){ return is_string($name) && strpos($name, 'img2html/atom-') === 0; }
function img2html_is_molecule($name){ return is_string($name) && strpos($name, 'img2html/molecule-') === 0; }
function img2html_is_organism($name){ return is_string($name) && strpos($name, 'img2html/organism-') === 0; }
function img2html_is_core_html($name){ return $name === 'core/html'; }
function img2html_is_core_block($name){ return is_string($name) && strpos($name, 'core/') === 0; }

function img2html_validate_block_tree($blocks){
  $violations = [];
  $walk = function($node, $parentType = null) use (&$walk, &$violations){
    $name = isset($node['blockName']) ? $node['blockName'] : '';
    $children = isset($node['innerBlocks']) ? (array)$node['innerBlocks'] : [];
    $type = img2html_is_atom($name) ? 'atom' : (img2html_is_molecule($name) ? 'molecule' : (img2html_is_organism($name) ? 'organism' : 'other'));
    if ($type === 'atom' && !empty($children)){
      $violations[] = ['severity'=>'error','rule'=>'atom_no_children','message'=>'Átomo con bloques internos','block'=>$name];
    }
    if ($type === 'molecule'){
      foreach ($children as $ch){
        $chName = isset($ch['blockName']) ? $ch['blockName'] : '';
        if (!img2html_is_atom($chName)){
          $violations[] = ['severity'=>'error','rule'=>'molecule_children_atoms_only','message'=>'Molécula con hijo no átomo','block'=>$name,'child'=>$chName];
        }
        if (img2html_is_core_html($chName)){
          $violations[] = ['severity'=>'error','rule'=>'no_core_html','message'=>'HTML directo dentro de molécula','block'=>$name];
        }
      }
    }
    if ($type === 'organism'){
      foreach ($children as $ch){
        $chName = isset($ch['blockName']) ? $ch['blockName'] : '';
        if (!img2html_is_molecule($chName) && !img2html_is_atom($chName)){
          $violations[] = ['severity'=>'error','rule'=>'organism_children_molecules_or_atoms','message'=>'Organismo con hijo inválido','block'=>$name,'child'=>$chName];
        }
        if (img2html_is_core_html($chName)){
          $violations[] = ['severity'=>'error','rule'=>'no_core_html','message'=>'HTML directo dentro de organismo','block'=>$name];
        }
      }
    }
    if (img2html_is_core_html($name)){
      $violations[] = ['severity'=>'error','rule'=>'no_core_html','message'=>'HTML directo en contenido','block'=>$name];
    }
    foreach ($children as $ch){ $walk($ch, $type); }
  };
  foreach ($blocks as $b){ $walk($b, null); }
  return $violations;
}

function img2html_validate_composition($post_id, $content){
  $blocks = function_exists('parse_blocks') ? parse_blocks($content) : [];
  $violations = img2html_validate_block_tree($blocks);
  $summary = [
    'post_id' => intval($post_id),
    'count' => count($violations),
    'violations' => $violations,
    'ok' => count($violations) === 0,
    'checked_at' => time()
  ];
  update_post_meta($post_id, 'img2html_composition_report', wp_json_encode($summary));
  return $summary;
}

add_action('save_post', function($post_id, $post, $update){
  if (wp_is_post_autosave($post_id) || wp_is_post_revision($post_id)) return;
  $content = isset($post->post_content) ? $post->post_content : '';
  img2html_validate_composition($post_id, $content);
}, 10, 3);

add_action('admin_notices', function(){
  $screen = function_exists('get_current_screen') ? get_current_screen() : null;
  if (!$screen || $screen->base !== 'post') return;
  $post_id = isset($_GET['post']) ? intval($_GET['post']) : 0;
  if (!$post_id) return;
  $raw = get_post_meta($post_id, 'img2html_composition_report', true);
  if (!$raw) return;
  $rep = json_decode($raw, true);
  if (!is_array($rep)) return;
  $count = isset($rep['count']) ? intval($rep['count']) : 0;
  if ($count > 0){
    $items = array_slice((array)$rep['violations'], 0, 5);
    $list = '';
    foreach ($items as $v){
      $msg = isset($v['message']) ? $v['message'] : 'Violación';
      $blk = isset($v['block']) ? $v['block'] : '';
      $child = isset($v['child']) ? $v['child'] : '';
      $list .= '<li>'.esc_html($msg).($blk?' — '.$blk:'').($child?' → '.$child:'').'</li>';
    }
    echo '<div class="notice notice-error"><p><strong>Atomic Design:</strong> Se detectaron '.$count.' violaciones de composición.</p><ul>'.$list.'</ul></div>';
  } else {
    echo '<div class="notice notice-success is-dismissible"><p><strong>Atomic Design:</strong> Composición válida.</p></div>';
  }
});

