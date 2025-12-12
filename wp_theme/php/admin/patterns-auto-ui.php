<?php
if (!defined('ABSPATH')) { exit; }

add_action('admin_menu', function(){
  add_theme_page('Patrones Automáticos','Patrones Automáticos','manage_options','img2html_auto_patterns', function(){
    $created = isset($_GET['created']) ? intval($_GET['created']) : 0;
    $skipped = isset($_GET['skipped']) ? intval($_GET['skipped']) : 0;
    echo '<div class="wrap"><h1>Patrones Automáticos</h1>';
    if ($created || $skipped){
      echo '<div class="notice notice-success"><p>Generados: '.intval($created).' | Omitidos: '.intval($skipped).'</p></div>';
    }
    echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';
    wp_nonce_field('img2html_generate_patterns');
    echo '<input type="hidden" name="action" value="img2html_generate_patterns" />';
    echo '<p><button class="button button-primary" type="submit">Generar patrones</button></p>';
    echo '</form>';
    echo '</div>';
  });
});
