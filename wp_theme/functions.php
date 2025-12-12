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

// Registrar patrones sincronizados desde archivos PHP con metadata
function img2html_register_synced_patterns() {
    $patterns_dir = get_theme_file_path('patterns');
    if (!is_dir($patterns_dir)) return;

    // Definir categorías comunes
    register_block_pattern_category('img2html-header', array('label' => __('Header', 'img2html')));
    register_block_pattern_category('img2html-footer', array('label' => __('Footer', 'img2html')));
    register_block_pattern_category('img2html-call-to-action', array('label' => __('Call to Action', 'img2html')));
    register_block_pattern_category('img2html-hero', array('label' => __('Hero', 'img2html')));
    register_block_pattern_category('img2html-cards', array('label' => __('Cards', 'img2html')));
    register_block_pattern_category('img2html-testimonials', array('label' => __('Testimonials', 'img2html')));

    foreach (glob($patterns_dir . '/*.php') as $file) {
        $slug = basename($file, '.php');
        $content = file_get_contents($file);
        if (!$content) continue;

        // Extraer contenido HTML después de ?>
        $html_content = preg_replace('/.*?\?>/s', '', $content);

        // Extraer metadatos del encabezado
        preg_match('/Title:\s*(.+)/', $content, $title_match);
        preg_match('/Description:\s*(.+)/', $content, $desc_match);
        preg_match('/Categories:\s*(.+)/', $content, $cat_match);
        preg_match('/Sync Status:\s*(synced|unsynced)/i', $content, $sync_match);

        $title = isset($title_match[1]) ? trim($title_match[1]) : ucwords(str_replace('-', ' ', $slug));
        $description = isset($desc_match[1]) ? trim($desc_match[1]) : 'Patrón reutilizable';
        $cat_string = isset($cat_match[1]) ? trim($cat_match[1]) : 'img2html';
        $categories = array_map('trim', explode(',', $cat_string));
        $is_synced = isset($sync_match[1]) && strtolower($sync_match[1]) === 'synced';

        register_block_pattern(
            'img2html/' . $slug,
            array(
                'title' => $title,
                'description' => $description,
                'content' => trim($html_content),
                'categories' => $categories,
                'syncStatus' => $is_synced ? 'synced' : 'unsynced',
            )
        );
    }
}
add_action('init', 'img2html_register_synced_patterns', 20);
