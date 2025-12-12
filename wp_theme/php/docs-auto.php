<?php
if (!defined('ABSPATH')) { exit; }

function img2html_generate_docs(){
  if (!current_user_can('manage_options')) return ['written'=>[]];
  $base = get_theme_file_path('');
  $docs_dir = $base.'/docs';
  if (!is_dir($docs_dir)) wp_mkdir_p($docs_dir);
  $written = [];
  $theme_path = get_theme_file_path('theme.json');
  $theme = file_exists($theme_path) ? json_decode(file_get_contents($theme_path), true) : [];
  $settings = isset($theme['settings']) ? $theme['settings'] : [];
  $mk = [];
  $mk[] = '# Guía del Tema';
  $mk[] = '## Layout';
  $mk[] = '- ContentSize: '.esc_html(isset($settings['layout']['contentSize'])?$settings['layout']['contentSize']:'');
  $mk[] = '- WideSize: '.esc_html(isset($settings['layout']['wideSize'])?$settings['layout']['wideSize']:'');
  $mk[] = '## Tipografías';
  if (!empty($settings['typography']['fontFamilies'])){
    foreach ($settings['typography']['fontFamilies'] as $ff){
      $mk[] = '- '.esc_html(isset($ff['name'])?$ff['name']:'').' ('.esc_html(isset($ff['slug'])?$ff['slug']:'').')';
    }
  }
  $mk[] = '## Colores';
  if (!empty($settings['color']['palette'])){
    foreach ($settings['color']['palette'] as $c){ $mk[] = '- '.esc_html(isset($c['name'])?$c['name']:'').': '.esc_html(isset($c['color'])?$c['color']:''); }
  }
  $mk[] = '## Espaciado';
  if (!empty($settings['spacing']['spacingSizes'])){
    foreach ($settings['spacing']['spacingSizes'] as $s){ $mk[] = '- '.esc_html(isset($s['name'])?$s['name']:'').': '.esc_html(isset($s['size'])?$s['size']:''); }
  }
  $theme_md = implode("\n", $mk);
  file_put_contents($docs_dir.'/THEME_GUIDE.md', $theme_md);
  $written[] = 'THEME_GUIDE.md';

  $pat_dir = get_theme_file_path('patterns');
  $pat_md = [];
  $pat_md[] = '# Guía de Patrones';
  if (is_dir($pat_dir)){
    $files = array_merge(glob($pat_dir.'/*.html'), glob($pat_dir.'/*.php'));
    foreach ($files as $file){
      $slug = basename($file);
      $name = preg_replace('/\.(html|php)$/','', $slug);
      $pat_md[] = '## '.esc_html(ucwords(str_replace('-', ' ', $name)));
      $pat_md[] = '- Slug: `img2html/'.esc_html(sanitize_title($name)).'`';
      $pat_md[] = '- Uso: inserta desde Patrones en el editor del sitio';
    }
  }
  file_put_contents($docs_dir.'/PATTERNS_GUIDE.md', implode("\n", $pat_md));
  $written[] = 'PATTERNS_GUIDE.md';

  $ext_md = [];
  $ext_md[] = '# Cómo Extender';
  $ext_md[] = '- Añade estilos de bloque en `php/block-styles.php`';
  $ext_md[] = '- Añade CSS para `is-style-*` en `assets/components/img2html-block-styles.css`';
  $ext_md[] = '- Crea nuevos bloques en `blocks/` con `block.json` y `render.php`';
  $ext_md[] = '- Registra assets en `blocks-manifest.php`';
  file_put_contents($docs_dir.'/EXTEND.md', implode("\n", $ext_md));
  $written[] = 'EXTEND.md';

  $compose_md = [];
  $compose_md[] = '# Cómo Combinar Bloques';
  $report = get_option('img2html_auto_patterns_report');
  if (is_array($report) && !empty($report['seq'])){
    $compose_md[] = '## Secuencias frecuentes';
    foreach ($report['seq'] as $sig=>$count){ $compose_md[] = '- '.esc_html($sig).' ('.$count.')'; }
  }
  if (is_array($report) && !empty($report['grp'])){
    $compose_md[] = '## Grupos frecuentes';
    foreach ($report['grp'] as $sig=>$count){ $compose_md[] = '- '.esc_html($sig).' ('.$count.')'; }
  }
  file_put_contents($docs_dir.'/COMPOSE.md', implode("\n", $compose_md));
  $written[] = 'COMPOSE.md';

  $style_md = [];
  $style_md[] = '# Recomendaciones de Estilo';
  $style_md[] = '- Usa paleta y tipografías definidas en `theme.json`';
  $style_md[] = '- Prefiere `layout: constrained` para grupos';
  $style_md[] = '- Usa `margin` y `padding` según presets de spacing';
  $style_md[] = '- Evita duplicar estilos entre block styles y CSS de bloques';
  file_put_contents($docs_dir.'/STYLE.md', implode("\n", $style_md));
  $written[] = 'STYLE.md';

  return ['written'=>$written];
}

add_action('admin_post_img2html_generate_docs', function(){
  if (!current_user_can('manage_options')) wp_die('');
  check_admin_referer('img2html_generate_docs');
  $res = img2html_generate_docs();
  wp_redirect(add_query_arg(['page'=>'img2html_docs','w'=>count($res['written'])], admin_url('themes.php')));
  exit;
});

function img2html_publish_docs_page(){
  if (!current_user_can('manage_options')) return 0;
  $docs_dir = get_theme_file_path('docs');
  $files = ['THEME_GUIDE.md','PATTERNS_GUIDE.md','EXTEND.md','COMPOSE.md','STYLE.md'];
  $sections = [];
  foreach ($files as $f){
    $p = $docs_dir.'/'.$f;
    if (file_exists($p)){
      $title = ucwords(str_replace(['_','-','.md'],' ', $f));
      $content = file_get_contents($p);
      $content = esc_html($content);
      $sections[] = '<!-- wp:heading --><h2>'.$title.'</h2><!-- /wp:heading -->'.'<!-- wp:preformatted --><pre class="wp-block-preformatted">'.$content.'</pre><!-- /wp:preformatted -->';
    }
  }
  $body = implode('', $sections);
  if (!$body) return 0;
  $wrap = '<!-- wp:group {"layout":{"type":"constrained"}} --><div class="wp-block-group">'.'<!-- wp:heading --><h1>Documentación del Tema</h1><!-- /wp:heading -->'.$body.'</div><!-- /wp:group -->';
  $existing = get_page_by_path('theme-docs');
  $postarr = [
    'post_title' => 'Documentación del Tema',
    'post_name' => 'theme-docs',
    'post_status' => 'publish',
    'post_type' => 'page',
    'post_content' => $wrap
  ];
  if ($existing){
    $postarr['ID'] = $existing->ID;
    wp_update_post($postarr);
    return intval($existing->ID);
  } else {
    return wp_insert_post($postarr);
  }
}

add_action('admin_post_img2html_publish_docs_page', function(){
  if (!current_user_can('manage_options')) wp_die('');
  check_admin_referer('img2html_publish_docs');
  $id = img2html_publish_docs_page();
  $url = $id ? get_permalink($id) : ''; 
  wp_redirect(add_query_arg(['page'=>'img2html_docs','published'=>$id,'permalink'=>$url], admin_url('themes.php')));
  exit;
});
