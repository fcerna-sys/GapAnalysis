<?php
/**
 * Functions and definitions
 * 
 * @package img2html
 */

// Cargar archivos PHP adicionales
$dir = get_theme_file_path('php');
if (is_dir($dir)){
  foreach (glob($dir.'/*.php') as $file){
    require_once $file;
  }
  $sub = $dir.'/menu';
  if (is_dir($sub)){
    foreach (glob($sub.'/*.php') as $file){
      require_once $file;
    }
  }
}

// Registrar patterns del tema
function img2html_register_patterns() {
    register_block_pattern_category('img2html', array('label' => sanitize_text_field('Img2HTML')));
    
    $patterns_dir = get_theme_file_path('patterns');
    if (is_dir($patterns_dir)) {
        $pattern_files = glob($patterns_dir . '/*.html');
        foreach ($pattern_files as $file) {
            $slug = basename($file, '.html');
            $slug = sanitize_title($slug);
            $content = file_get_contents($file);
            if ($content) {
                $content = wp_kses_post($content);
                register_block_pattern(
                    'img2html/' . $slug,
                    array(
                        'title' => sanitize_text_field(ucwords(str_replace('-', ' ', $slug))),
                        'description' => sanitize_text_field('Patrón generado desde imágenes'),
                        'content' => $content,
                        'categories' => array('img2html'),
                    )
                );
            }
        }
    }
}
add_action('init', 'img2html_register_patterns');

// Registrar menús del tema
function img2html_register_menus(){
  register_nav_menus([
    'primary_menu'   => __('Menú Principal', 'img2html'),
    'secondary_menu' => __('Menú Secundario', 'img2html'),
    'footer_menu'    => __('Menú Footer', 'img2html'),
  ]);
}
add_action('init','img2html_register_menus');

function img2html_register_atomic_blocks(){
  $base = get_template_directory().'/blocks';
  $groups = ['atoms','molecules','organisms'];
  foreach ($groups as $grp){
    $dir = $base.'/'.$grp;
    if (is_dir($dir)){
      foreach (glob($dir.'/*', GLOB_ONLYDIR) as $blockDir){
        $blockJson = $blockDir.'/block.json';
        if (file_exists($blockJson)){
          register_block_type($blockDir);
        }
      }
    }
  }
  // Registrar también bloques en la raíz de /blocks (ej. /blocks/cta, /blocks/card, /blocks/hero)
  foreach (glob($base.'/*', GLOB_ONLYDIR) as $blockDir){
    $name = basename($blockDir);
    if (in_array($name, $groups, true)) continue; // ya procesados
    $blockJson = $blockDir.'/block.json';
    if (file_exists($blockJson)){
      register_block_type($blockDir);
    }
  }
}
add_action('init','img2html_register_atomic_blocks');



// Inyectar Critical CSS inline
function img2html_critical_css() {
    $path = get_theme_file_path('assets/css/critical.css');
    $path_min = get_theme_file_path('assets/css/critical.min.css');
    $use = file_exists($path_min) ? $path_min : $path;
    if (file_exists($use)) {
        $critical_css = file_get_contents($use);
        echo '<style id="img2html-critical-css">' . $critical_css . '</style>';
    }
}
add_action('wp_head', 'img2html_critical_css', 1);
