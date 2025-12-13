<?php
if (!defined('ABSPATH')) { exit; }

function img2html_docs_admin_menu(){
  add_theme_page('Img2HTML Docs', 'Docs', 'read', 'img2html_docs', 'img2html_docs_admin_page');
}
add_action('admin_menu','img2html_docs_admin_menu');

function img2html_docs_admin_page(){
  $url = get_theme_file_uri('docs/app-overview.html');
  echo '<div class="wrap"><h1>Documentación</h1>';
  echo '<p>Referencia técnica completa del tema.</p>';
  echo '<iframe src="'.esc_url($url).'" style="width:100%;height:80vh;border:1px solid #ccd;" loading="lazy"></iframe>';
  echo '</div>';
}

