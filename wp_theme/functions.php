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
}

// Registrar patterns del tema
function img2html_register_patterns() {
    register_block_pattern_category('img2html', array('label' => 'Img2HTML'));
    
    $patterns_dir = get_theme_file_path('patterns');
    if (is_dir($patterns_dir)) {
        $pattern_files = glob($patterns_dir . '/*.html');
        foreach ($pattern_files as $file) {
            $slug = basename($file, '.html');
            $content = file_get_contents($file);
            if ($content) {
                register_block_pattern(
                    'img2html/' . $slug,
                    array(
                        'title' => ucwords(str_replace('-', ' ', $slug)),
                        'description' => 'Patrón generado desde imágenes',
                        'content' => $content,
                        'categories' => array('img2html'),
                    )
                );
            }
        }
    }
}
add_action('init', 'img2html_register_patterns');

function img2html_register_atomic_blocks(){
  $base = get_template_directory().'/blocks';
  $groups = ['atoms','molecules'];
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
}
add_action('init','img2html_register_atomic_blocks');
