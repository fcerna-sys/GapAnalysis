<?php
if (!defined('ABSPATH')) { exit; }

function img2html_atomic_admin_menu(){
  add_theme_page('Img2HTML Atomic', 'Img2HTML Atomic', 'manage_options', 'img2html_atomic', 'img2html_atomic_admin_page');
}
add_action('admin_menu','img2html_atomic_admin_menu');

function img2html_atomic_admin_page(){
  if (!current_user_can('manage_options')) return;
  $action = admin_url('admin-post.php');
  $nonce = wp_create_nonce('img2html_scaffold_block');
  echo '<div class="wrap"><h1>Atomic Blocks</h1>';
  echo '<p>Crea nuevos bloques atómicos (Átomos, Moléculas, Organismos) con scaffolding listo.</p>';
  echo '<form method="post" action="'.$action.'">';
  echo '<input type="hidden" name="action" value="img2html_scaffold_block" />';
  echo '<input type="hidden" name="_wpnonce" value="'.$nonce.'" />';
  echo '<table class="form-table">';
  echo '<tr><th><label for="type">Tipo</label></th><td><select id="type" name="type"><option value="atoms">Átomo</option><option value="molecules">Molécula</option><option value="organisms">Organismo</option></select></td></tr>';
  echo '<tr><th><label for="name">Nombre</label></th><td><input type="text" id="name" name="name" class="regular-text" placeholder="Ej: badge, card-feature" required /></td></tr>';
  echo '</table>';
  echo '<p class="submit"><button type="submit" class="button button-primary">Crear bloque</button></p>';
  echo '</form>';
  echo '</div>';
}

function img2html_scaffold_block(){
  if (!current_user_can('manage_options')) wp_die('');
  check_admin_referer('img2html_scaffold_block');
  $type = isset($_POST['type']) ? sanitize_key($_POST['type']) : '';
  $name = isset($_POST['name']) ? sanitize_key($_POST['name']) : '';
  $valid = in_array($type, ['atoms','molecules','organisms'], true) && $name;
  if (!$valid){ wp_redirect(add_query_arg(['page'=>'img2html_atomic','error'=>1], admin_url('themes.php'))); exit; }

  $blocks_dir = get_theme_file_path('blocks');
  $dir = $blocks_dir.'/'.$type.'/'.$name;
  if (!is_dir($dir)) wp_mkdir_p($dir);

  $title = ucwords(str_replace('-', ' ', $name));
  $ns = $type === 'atoms' ? 'Átomo' : ($type === 'molecules' ? 'Molécula' : 'Organismo');
  $category = $type === 'atoms' ? 'widgets' : 'design';
  $block_name = 'img2html/'.($type === 'atoms' ? 'atom-' : ($type === 'molecules' ? 'molecule-' : 'organism-')).$name;

  $block_json = [
    '$schema' => 'https://schemas.wp.org/trunk/block.json',
    'apiVersion' => 3,
    'name' => $block_name,
    'title' => $title.' ('.$ns.')',
    'category' => $category,
    'description' => 'Bloque generado automáticamente',
    'style' => 'file:./style.css',
    'render' => 'file:./render.php',
    'attributes' => new stdClass(),
    'supports' => [
      'spacing' => [ 'margin' => true, 'padding' => true ],
      'color' => [ 'background' => true, 'text' => true ],
      'html' => false,
      'customClassName' => false
    ],
    'example' => [ 'attributes' => new stdClass() ],
    'version' => '1.0.0'
  ];
  $json_str = json_encode($block_json, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT);
  file_put_contents($dir.'/block.json', $json_str);

  $bem_block = $type === 'atoms' ? 'atom-'.$name : ($type === 'molecules' ? 'molecule-'.$name : 'organism-'.$name);
  $render = "<?php\nif (!defined('ABSPATH')) { exit; }\n\\$base = function_exists('img2html_bem') ? img2html_bem('".$bem_block."') : 'img2html-".$bem_block."';\n?><div class=\"<?php echo esc_attr(\\$base); ?>\"></div>\n";
  file_put_contents($dir.'/render.php', $render);

  $style = ".img2html-".$bem_block."{display:block;padding:var(--wp--preset--spacing--md);background:var(--wp--preset--color--background);color:var(--wp--preset--color--text);border:1px solid var(--wp--preset--color--surface);border-radius:var(--wp--preset--border-radius--small)}\n";
  file_put_contents($dir.'/style.css', $style);

  wp_redirect(add_query_arg(['page'=>'img2html_atomic','created'=>$type.'/'.$name], admin_url('themes.php')));
  exit;
}
add_action('admin_post_img2html_scaffold_block','img2html_scaffold_block');

