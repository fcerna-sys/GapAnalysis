<?php
if (!defined('ABSPATH')) { exit; }

add_action('admin_menu', function(){
  add_theme_page('Performance','Performance','manage_options','img2html_performance', function(){
    echo '<div class="wrap"><h1>Performance del Tema</h1>';
    // Notices
    if (isset($_GET['minified'])){
      echo '<div class="notice notice-success"><p>Minificado ejecutado.</p></div>';
    }
    if (isset($_GET['purged'])){
      $msg = isset($_GET['msg']) ? sanitize_text_field($_GET['msg']) : '';
      $before = isset($_GET['before']) ? sanitize_text_field($_GET['before']) : '';
      $after = isset($_GET['after']) ? sanitize_text_field($_GET['after']) : '';
      echo '<div class="notice notice-info"><p>Purge ejecutado. '.$msg.'</p><p><strong>Antes:</strong> '.$before.' &nbsp; <strong>Después:</strong> '.$after.'</p></div>';
    }
    if (isset($_GET['built'])){
      $msg = isset($_GET['msg']) ? sanitize_text_field($_GET['msg']) : '';
      echo '<div class="notice notice-info"><p>Build ejecutado. '.$msg.'</p></div>';
    }

    // Resumen de tamaños
    if (function_exists('img2html_assets_sizes')){
      $sizes = img2html_assets_sizes();
      echo '<h2>Tamaños CSS</h2>';
      echo '<p><strong>Total:</strong> '.esc_html($sizes['total']).'</p>';
      if (!empty($sizes['groups'])){
        foreach ($sizes['groups'] as $label=>$group){
          echo '<h3>'.esc_html($label).'</h3>';
          echo '<table class="widefat"><thead><tr><th>Archivo</th><th>Tamaño</th></tr></thead><tbody>';
          foreach ($group['files'] as $row){
            echo '<tr><td>'.esc_html($row['file']).'</td><td>'.esc_html($row['size']).'</td></tr>';
          }
          echo '</tbody></table>';
          echo '<p><em>Total '.esc_html($label).':</em> '.esc_html($group['total']).'</p>';
        }
      }
    }

    // Acciones
    echo '<h2>Acciones</h2>';
    echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';
    wp_nonce_field('img2html_minify_assets');
    echo '<input type="hidden" name="action" value="img2html_minify_assets" />';
    echo '<p><button class="button button-primary" type="submit">Minify</button></p>';
    echo '</form>';

    echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';
    wp_nonce_field('img2html_purge_assets');
    echo '<input type="hidden" name="action" value="img2html_purge_assets" />';
    echo '<p><button class="button" type="submit">Purge</button></p>';
    echo '</form>';

    echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';
    wp_nonce_field('img2html_build_assets');
    echo '<input type="hidden" name="action" value="img2html_build_assets" />';
    echo '<p><button class="button" type="submit">Build</button></p>';
    echo '</form>';

    echo '</div>';
  });
});
