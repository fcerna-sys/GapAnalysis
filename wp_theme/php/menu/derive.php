<?php
if (!defined('ABSPATH')) { exit; }

function img2html_theme_derive_admin_menu(){
  add_theme_page('Img2HTML Theme Derive', 'Theme Derive', 'manage_options', 'img2html_theme_derive', 'img2html_theme_derive_admin_page');
}
add_action('admin_menu','img2html_theme_derive_admin_menu');

function img2html_theme_derive_admin_page(){
  if (!current_user_can('manage_options')) return;
  $action = admin_url('admin-post.php');
  $nonce = wp_create_nonce('img2html_save_theme_derive');
  $profile = get_option('img2html_theme_profile','medium');
  echo '<div class="wrap"><h1>Theme Derive</h1>';
  echo '<p>Selecciona el perfil tipográfico y de ritmo vertical.</p>';
  echo '<form method="post" action="'.$action.'">';
  echo '<input type="hidden" name="action" value="img2html_save_theme_derive" />';
  echo '<input type="hidden" name="_wpnonce" value="'.$nonce.'" />';
  echo '<table class="form-table">';
  echo '<tr><th><label for="profile">Perfil</label></th><td><select id="profile" name="profile">';
  foreach ([['compact','Compacto'],['medium','Medio'],['ample','Amplio']] as $opt){
    $sel = $profile === $opt[0] ? ' selected' : '';
    echo '<option value="'.$opt[0].'"'.$sel.'>'.$opt[1].'</option>';
  }
  echo '</select></td></tr>';
  echo '</table>';
  echo '<p class="submit"><button type="submit" class="button button-primary">Guardar y recalcular</button></p>';
  echo '</form>';
  echo '</div>';
}

add_action('admin_post_img2html_save_theme_derive', function(){
  if (!current_user_can('manage_options')) wp_die('');
  check_admin_referer('img2html_save_theme_derive');
  $profile = isset($_POST['profile']) ? sanitize_key($_POST['profile']) : 'medium';
  if (!in_array($profile, ['compact','medium','ample'], true)) $profile = 'medium';
  update_option('img2html_theme_profile', $profile);
  update_option('img2html_theme_profile_updated', time());
  wp_redirect(add_query_arg(['page'=>'img2html_theme_derive','updated'=>1,'profile'=>$profile], admin_url('themes.php')));
  exit;
});

