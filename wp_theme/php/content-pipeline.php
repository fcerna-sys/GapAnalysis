<?php
if (!defined('ABSPATH')) { exit; }

function img2html_content_admin_menu(){
  add_theme_page('Img2HTML Content', 'Content', 'manage_options', 'img2html_content', 'img2html_content_admin_page');
}
add_action('admin_menu','img2html_content_admin_menu');

function img2html_read_content_json(){
  $path = get_theme_file_path('content/content.json');
  if (!file_exists($path)) return [];
  $data = json_decode(file_get_contents($path), true);
  return is_array($data) ? $data : [];
}

function img2html_theme_palette_slugs(){
  $path = get_theme_file_path('theme.json');
  if (!file_exists($path)) return [];
  $json = json_decode(file_get_contents($path), true);
  $out = [];
  if (is_array($json) && isset($json['settings']['color']['palette']) && is_array($json['settings']['color']['palette'])){
    foreach ($json['settings']['color']['palette'] as $p){
      if (isset($p['slug'])) $out[] = $p['slug'];
    }
  }
  return $out;
}

function img2html_validate_content_json($data){
  $errors = [];
  $warnings = [];
  if (!is_array($data)) { $errors[] = 'JSON inválido'; return ['errors'=>$errors,'warnings'=>$warnings]; }
  $pages = isset($data['pages']) ? (array)$data['pages'] : [];
  $media = isset($data['media']) ? (array)$data['media'] : [];
  $media_files = [];
  foreach ($media as $m){ if (!empty($m['file'])) $media_files[] = $m['file']; }
  $theme_dir_name = basename(get_template_directory());
  $img_dir = get_theme_file_path('content/images');
  $palette_slugs = img2html_theme_palette_slugs();
  $slugs = [];
  foreach ($pages as $p){
    $slug = isset($p['slug']) ? sanitize_title($p['slug']) : '';
    $title = isset($p['title']) ? sanitize_text_field($p['title']) : '';
    if (!$slug) $errors[] = 'Página sin slug';
    if (!$title) $warnings[] = 'Página '.$slug.' sin título';
    if ($slug){ if (isset($slugs[$slug])){ $errors[] = 'Slug duplicado: '.$slug; } else { $slugs[$slug]=true; } }
    $blocks = isset($p['blocks']) ? (array)$p['blocks'] : [];
    foreach ($blocks as $b){
      $type = isset($b['type']) ? $b['type'] : '';
      if (!$type){ $errors[] = 'Bloque sin tipo en '.$slug; continue; }
      if (!in_array($type, ['hero','card-grid','features-list','testimonial','team-member','pricing-feature'], true)){
        $warnings[] = 'Tipo no soportado: '.$type.' en '.$slug;
      }
      if ($type === 'hero'){
        $d = isset($b['data']) ? (array)$b['data'] : [];
        if (empty($d['title']) && empty($d['subtitle']) && empty($d['image'])) $warnings[] = 'Hero vacío en '.$slug;
        if (!empty($d['image'])){
          $f = $d['image'];
          if (!in_array($f, $media_files, true)) $warnings[] = 'Hero imagen no declarada en media: '.$f;
          if (!file_exists($img_dir.'/'.$f)) $warnings[] = 'Archivo de imagen faltante: '.$f;
        }
      }
      if ($type === 'card-grid'){
        $items = isset($b['items']) ? (array)$b['items'] : [];
        if (!$items) $warnings[] = 'Card-grid sin items en '.$slug;
        foreach ($items as $it){ if (!empty($it['image']) && !file_exists($img_dir.'/'.$it['image'])) $warnings[] = 'Imagen faltante: '.$it['image']; }
      }
      if ($type === 'features-list'){
        $items = isset($b['items']) ? (array)$b['items'] : [];
        if (!$items) $warnings[] = 'Features-list sin items en '.$slug;
        foreach ($items as $it){
          if (!empty($it['iconColor']) && !in_array($it['iconColor'], $palette_slugs, true)){
            $warnings[] = 'iconColor no existe en palette: '.$it['iconColor'].' en '.$slug;
          }
        }
      }
      if ($type === 'testimonial'){
        if (empty($b['quote'])) $warnings[] = 'Testimonial sin quote en '.$slug;
      }
      if ($type === 'team-member'){
        $items = isset($b['items']) ? (array)$b['items'] : [];
        if (!$items) $warnings[] = 'Team-member sin items en '.$slug;
        foreach ($items as $it){ if (!empty($it['image']) && !file_exists($img_dir.'/'.$it['image'])) $warnings[] = 'Imagen faltante: '.$it['image']; }
      }
      if ($type === 'pricing-feature'){
        $plans = isset($b['plans']) ? (array)$b['plans'] : [];
        if (!$plans) $warnings[] = 'Pricing-feature sin planes en '.$slug;
      }
    }
  }
  return ['errors'=>$errors,'warnings'=>$warnings];
}

function img2html_generate_import_scripts(){
  $data = img2html_read_content_json();
  $pages = isset($data['pages']) ? (array)$data['pages'] : [];
  $media = isset($data['media']) ? (array)$data['media'] : [];
  $theme_dir_name = basename(get_template_directory());
  $theme_rel_images = 'wp-content/themes/'.$theme_dir_name.'/content/images';
  $tools_dir = get_theme_file_path('tools');
  if (!is_dir($tools_dir)) wp_mkdir_p($tools_dir);
  $blocks_dir = $tools_dir.'/blocks';
  if (!is_dir($blocks_dir)) wp_mkdir_p($blocks_dir);

  $var_name = function($file){ return 'ID_'.preg_replace('/[^a-zA-Z0-9]+/','_', strtolower($file)); };

  $sh = "#!/usr/bin/env bash\nset -e\n";
  foreach ($media as $m){
    $file = isset($m['file']) ? $m['file'] : '';
    $title = isset($m['title']) ? $m['title'] : $file;
    if (!$file) continue;
    $vn = $var_name($file);
    $sh .= "$vn=$(wp media import '$theme_rel_images/$file' --title='$title' --porcelain)\n";
  }
  foreach ($pages as $p){
    $slug = isset($p['slug']) ? sanitize_title($p['slug']) : '';
    $title = isset($p['title']) ? sanitize_text_field($p['title']) : $slug;
    $blocks = isset($p['blocks']) ? (array)$p['blocks'] : [];
    if (!$slug) continue;
    $here = "cat > $blocks_dir/$slug.blocks.html <<EOF\n";
    $here .= img2html_build_blocks_html($blocks, $var_name);
    $here .= "\nEOF\n";
    $sh .= $here;
    $sh .= "wp post create --post_type=page --post_title='$title' --post_name='$slug' --post_status=publish --post_content=\"$(cat $blocks_dir/$slug.blocks.html)\"\n";
  }
  file_put_contents($tools_dir.'/import-content.sh', $sh);

  $ps = "#requires -Version 5.1\n$ErrorActionPreference = 'Stop'\n";
  foreach ($media as $m){
    $file = isset($m['file']) ? $m['file'] : '';
    $title = isset($m['title']) ? $m['title'] : $file;
    if (!$file) continue;
    $vn = $var_name($file);
    $ps .= '$'.$vn." = (wp media import '$theme_rel_images/$file' --title='$title' --porcelain)\n";
  }
  foreach ($pages as $p){
    $slug = isset($p['slug']) ? sanitize_title($p['slug']) : '';
    $title = isset($p['title']) ? sanitize_text_field($p['title']) : $slug;
    $blocks = isset($p['blocks']) ? (array)$p['blocks'] : [];
    if (!$slug) continue;
    $html = img2html_build_blocks_html($blocks, $var_name);
    $ps .= "$blocks = @\"\n$html\n\"@\n";
    $ps .= "$blocks | Out-File -Encoding UTF8 '$blocks_dir/$slug.blocks.html'\n";
    $ps .= "wp post create --post_type=page --post_title '$title' --post_name '$slug' --post_status publish --post_content (Get-Content '$blocks_dir/$slug.blocks.html' -Raw)\n";
  }
  file_put_contents($tools_dir.'/import-content.ps1', $ps);

  return [ 'sh' => $tools_dir.'/import-content.sh', 'ps1' => $tools_dir.'/import-content.ps1' ];
}

function img2html_build_blocks_html($blocks, $var_name){
  $out = '';
  $out .= '<!-- wp:group {"layout":{"type":"constrained"}} -->\n';
  $out .= '<div class="wp-block-group">\n';
  foreach ($blocks as $b){
    $type = isset($b['type']) ? $b['type'] : '';
    if ($type === 'hero'){
      $d = isset($b['data']) ? (array)$b['data'] : [];
      $title = isset($d['title']) ? $d['title'] : '';
      $subtitle = isset($d['subtitle']) ? $d['subtitle'] : '';
      $cta_text = isset($d['cta_text']) ? $d['cta_text'] : '';
      $cta_url = isset($d['cta_url']) ? $d['cta_url'] : '#';
      $image = isset($d['image']) ? $d['image'] : '';
      $imgVar = $image ? $var_name($image) : '';
      $out .= '<!-- wp:group -->\n<div class="wp-block-group">\n';
      if ($title){ $out .= '<!-- wp:img2html/atom-heading {"text":"'.htmlspecialchars($title,ENT_QUOTES).'","level":2} /-->\n'; }
      if ($subtitle){ $out .= '<!-- wp:img2html/atom-paragraph {"text":"'.htmlspecialchars($subtitle,ENT_QUOTES).'"} /-->\n'; }
      if ($cta_text){ $out .= '<!-- wp:img2html/atom-button {"text":"'.htmlspecialchars($cta_text,ENT_QUOTES).'","url":"'.htmlspecialchars($cta_url,ENT_QUOTES).'"} /-->\n'; }
      if ($imgVar){ $out .= '<!-- wp:image {"id":$'.$imgVar.'} -->\n<figure class="wp-block-image"><img src="" /></figure><!-- /wp:image -->\n'; }
      $out .= '</div>\n';
    }
    if ($type === 'card-grid'){
      $items = isset($b['items']) ? (array)$b['items'] : [];
      $out .= '<!-- wp:columns --><div class="wp-block-columns">\n';
      foreach ($items as $it){
        $title = isset($it['title']) ? $it['title'] : '';
        $text = isset($it['text']) ? $it['text'] : '';
        $image = isset($it['image']) ? $it['image'] : '';
        $out .= '<!-- wp:column --><div class="wp-block-column">\n';
        if ($image){
          $vn = $var_name($image);
          $out .= '<!-- wp:image {"id":$'.$vn.'} --><figure class="wp-block-image"><img src="" /></figure><!-- /wp:image -->\n';
        }
        if ($title){ $out .= '<!-- wp:img2html/atom-heading {"text":"'.htmlspecialchars($title,ENT_QUOTES).'","level":3} /-->\n'; }
        if ($text){ $out .= '<!-- wp:img2html/atom-paragraph {"text":"'.htmlspecialchars($text,ENT_QUOTES).'"} /-->\n'; }
        $out .= '</div><!-- /wp:column -->\n';
      }
      $out .= '</div><!-- /wp:columns -->\n';
    }
    if ($type === 'features-list'){
      $items = isset($b['items']) ? (array)$b['items'] : [];
      $has_icon = false;
      foreach ($items as $it){ if (!empty($it['icon'])) { $has_icon = true; break; } }
      if ($has_icon){
        $out .= '<!-- wp:group {"layout":{"type":"constrained"}} --><div class="wp-block-group">\n';
        foreach ($items as $it){
          $text = isset($it['text']) ? $it['text'] : '';
          $icon = isset($it['icon']) ? $it['icon'] : 'check';
          $iconColor = isset($it['iconColor']) ? $it['iconColor'] : '';
          $iconSize = isset($it['size']) ? intval($it['size']) : 20;
          $out .= '<!-- wp:group {"layout":{"type":"flex","flexWrap":"nowrap","justifyContent":"left","verticalAlignment":"center"}} -->\n<div class="wp-block-group">\n';
          $attrs = '{"name":"'.htmlspecialchars($icon,ENT_QUOTES).'","size":'.$iconSize;
          if ($iconColor){ $attrs .= ',"color":"'.htmlspecialchars($iconColor,ENT_QUOTES).'"'; }
          $attrs .= '}';
          $out .= '<!-- wp:img2html/atom-icon '.$attrs.' /-->\n';
          $out .= '<!-- wp:img2html/atom-paragraph {"text":"'.htmlspecialchars($text,ENT_QUOTES).'"} /-->\n';
          $out .= '</div><!-- /wp:group -->\n';
        }
        $out .= '</div><!-- /wp:group -->\n';
      } else {
        $out .= '<!-- wp:list --><ul class="wp-block-list">\n';
        foreach ($items as $it){
          $text = isset($it['text']) ? $it['text'] : '';
          $out .= '<li>'.htmlspecialchars($text,ENT_QUOTES).'</li>\n';
        }
        $out .= '</ul><!-- /wp:list -->\n';
      }
    }
    if ($type === 'testimonial'){
      $quote = isset($b['quote']) ? $b['quote'] : '';
      $author = isset($b['author']) ? $b['author'] : '';
      $role = isset($b['role']) ? $b['role'] : '';
      $out .= '<!-- wp:quote --><blockquote class="wp-block-quote">\n';
      if ($quote){ $out .= '<p>'.htmlspecialchars($quote,ENT_QUOTES).'</p>\n'; }
      if ($author){ $out .= '<cite>'.htmlspecialchars($author,ENT_QUOTES).( $role? ' — '.htmlspecialchars($role,ENT_QUOTES) : '' ).'</cite>\n'; }
      $out .= '</blockquote><!-- /wp:quote -->\n';
    }
    if ($type === 'team-member'){
      $items = isset($b['items']) ? (array)$b['items'] : [];
      $out .= '<!-- wp:columns --><div class="wp-block-columns">\n';
      foreach ($items as $it){
        $name = isset($it['name']) ? $it['name'] : '';
        $bio = isset($it['bio']) ? $it['bio'] : '';
        $image = isset($it['image']) ? $it['image'] : '';
        $out .= '<!-- wp:column --><div class="wp-block-column">\n';
        if ($image){ $vn = $var_name($image); $out .= '<!-- wp:image {"id":$'.$vn.'} --><figure class="wp-block-image"><img src="" /></figure><!-- /wp:image -->\n'; }
        if ($name){ $out .= '<!-- wp:img2html/atom-heading {"text":"'.htmlspecialchars($name,ENT_QUOTES).'","level":3} /-->\n'; }
        if ($bio){ $out .= '<!-- wp:img2html/atom-paragraph {"text":"'.htmlspecialchars($bio,ENT_QUOTES).'"} /-->\n'; }
        $out .= '</div><!-- /wp:column -->\n';
      }
      $out .= '</div><!-- /wp:columns -->\n';
    }
    if ($type === 'pricing-feature'){
      $plans = isset($b['plans']) ? (array)$b['plans'] : [];
      $out .= '<!-- wp:columns --><div class="wp-block-columns">\n';
      foreach ($plans as $plan){
        $title = isset($plan['title']) ? $plan['title'] : '';
        $price = isset($plan['price']) ? $plan['price'] : '';
        $features = isset($plan['features']) ? (array)$plan['features'] : [];
        $out .= '<!-- wp:column --><div class="wp-block-column">\n';
        if ($title){ $out .= '<!-- wp:img2html/atom-heading {"text":"'.htmlspecialchars($title,ENT_QUOTES).'","level":3} /-->\n'; }
        if ($price){ $out .= '<!-- wp:img2html/atom-paragraph {"text":"'.htmlspecialchars($price,ENT_QUOTES).'"} /-->\n'; }
        if ($features){
          $out .= '<!-- wp:list --><ul class="wp-block-list">\n';
          foreach ($features as $f){ $out .= '<li>'.htmlspecialchars($f,ENT_QUOTES).'</li>\n'; }
          $out .= '</ul><!-- /wp:list -->\n';
        }
        $out .= '</div><!-- /wp:column -->\n';
      }
      $out .= '</div><!-- /wp:columns -->\n';
    }
  }
  $out .= '</div>\n<!-- /wp:group -->';
  return $out;
}

function img2html_content_admin_page(){
  if (!current_user_can('manage_options')) return;
  $data = img2html_read_content_json();
  $report = img2html_validate_content_json($data);
  $action = admin_url('admin-post.php');
  $nonce = wp_create_nonce('img2html_content_actions');
  echo '<div class="wrap"><h1>Content Pipeline</h1>';
  echo '<p>Valida y genera scripts desde content/content.json.</p>';
  echo '<h2>Validación</h2>';
  if ($report['errors']){
    echo '<div class="notice notice-error"><p>Errores:</p><ul>';
    foreach ($report['errors'] as $e){ echo '<li>'.esc_html($e).'</li>'; }
    echo '</ul></div>';
  } else { echo '<div class="notice notice-success"><p>Sin errores.</p></div>'; }
  if ($report['warnings']){
    echo '<div class="notice notice-warning"><p>Advertencias:</p><ul>';
    foreach ($report['warnings'] as $w){ echo '<li>'.esc_html($w).'</li>'; }
    echo '</ul></div>';
  }
  echo '<form method="post" action="'.$action.'">';
  echo '<input type="hidden" name="action" value="img2html_content_generate" />';
  echo '<input type="hidden" name="_wpnonce" value="'.$nonce.'" />';
  $disabled = $report['errors'] ? ' disabled' : '';
  echo '<p class="submit"><button type="submit" class="button button-primary"'.$disabled.'>Generar scripts</button></p>';
  echo '</form>';
  echo '</div>';
}

add_action('admin_post_img2html_content_generate', function(){
  if (!current_user_can('manage_options')) wp_die('');
  check_admin_referer('img2html_content_actions');
  $data = img2html_read_content_json();
  $report = img2html_validate_content_json($data);
  if ($report['errors']){
    wp_redirect(add_query_arg(['page'=>'img2html_content','gen'=>'0'], admin_url('themes.php')));
    exit;
  }
  $res = img2html_generate_import_scripts();
  wp_redirect(add_query_arg(['page'=>'img2html_content','gen'=>'1','sh'=>$res['sh'],'ps1'=>$res['ps1']], admin_url('themes.php')));
  exit;
});
