<?php
if (!defined('ABSPATH')) { exit; }

add_action('admin_menu', function(){
  add_theme_page('Guía del Tema','Guía del Tema','manage_options','img2html_docs', function(){
    $w = isset($_GET['w']) ? intval($_GET['w']) : 0;
    echo '<div class="wrap"><h1>Guía del Tema</h1>';
    if ($w){ echo '<div class="notice notice-success"><p>Documentos generados: '.intval($w).'</p></div>'; }
    echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';
    wp_nonce_field('img2html_generate_docs');
    echo '<input type="hidden" name="action" value="img2html_generate_docs" />';
    echo '<p><button class="button button-primary" type="submit">Generar documentación</button></p>';
    echo '</form>';
    $pub = isset($_GET['published']) ? intval($_GET['published']) : 0;
    $perma = isset($_GET['permalink']) ? esc_url($_GET['permalink']) : '';
    if ($pub){ echo '<div class="notice notice-success"><p>Página publicada: <a href="'.$perma.'" target="_blank">ver</a></p></div>'; }
    echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';
    wp_nonce_field('img2html_publish_docs');
    echo '<input type="hidden" name="action" value="img2html_publish_docs_page" />';
    echo '<p><button class="button" type="submit">Publicar página de documentación</button></p>';
    echo '</form>';
    $docs = ['THEME_GUIDE.md','PATTERNS_GUIDE.md','EXTEND.md','COMPOSE.md','STYLE.md'];
    $dir = get_theme_file_path('docs');
    echo '<h2>Archivos</h2><ul>';
    foreach ($docs as $d){
      $p = $dir.'/'.$d;
      if (file_exists($p)){
        $url = content_url(str_replace(WP_CONTENT_DIR, '', $p));
        echo '<li><a href="'.esc_url($url).'" target="_blank">'.esc_html($d).'</a></li>';
      } else {
        echo '<li>'.esc_html($d).' (pendiente)</li>';
      }
    }
    echo '</ul></div>';
  });
});
