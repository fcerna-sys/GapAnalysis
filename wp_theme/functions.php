<?php
/**
 * Functions and definitions
 *
 * @package img2html
 */

// Configuración básica del tema (soportes, i18n, etc.)
function img2html_theme_setup() {
    // Cargar traducciones
    load_theme_textdomain( 'img2html', get_template_directory() . '/languages' );

    // Soporte de título automático
    add_theme_support( 'title-tag' );

    // Soporte de logo personalizado
    add_theme_support(
        'custom-logo',
        array(
            'height'      => 80,
            'width'       => 240,
            'flex-width'  => true,
            'flex-height' => true,
        )
    );

    // Imágenes destacadas
    add_theme_support( 'post-thumbnails' );

    // Alineaciones anchas
    add_theme_support( 'align-wide' );

    // Bloques y editor moderno
    add_theme_support( 'wp-block-styles' );
    add_theme_support( 'responsive-embeds' );
    add_theme_support( 'editor-styles' );

    // Marcado HTML5 para bloques y formularios
    add_theme_support(
        'html5',
        array(
            'search-form',
            'comment-form',
            'comment-list',
            'gallery',
            'caption',
            'style',
            'script',
        )
    );

    // Ready para RTL
    add_theme_support( 'rtl-language-support' );

    // Registrar menús de navegación
    register_nav_menus(
        array(
            'primary_menu'   => __( 'Menú Principal', 'img2html' ),
            'secondary_menu' => __( 'Menú Secundario', 'img2html' ),
            'footer_menu'    => __( 'Menú Footer', 'img2html' ),
        )
    );
}
add_action( 'after_setup_theme', 'img2html_theme_setup' );

// Cargar archivos PHP adicionales (helpers, CPT, hooks, etc.)
$dir = get_theme_file_path( 'php' );
if ( is_dir( $dir ) ) {
    foreach ( glob( $dir . '/*.php' ) as $file ) {
        require_once $file;
    }
    $sub = $dir . '/menu';
    if ( is_dir( $sub ) ) {
        foreach ( glob( $sub . '/*.php' ) as $file ) {
            require_once $file;
        }
    }
}

// Registrar patterns del tema (catálogo generado desde imágenes)
function img2html_register_patterns() {
    register_block_pattern_category(
        'img2html',
        array(
            'label' => sanitize_text_field( 'Img2HTML' ),
        )
    );

    $patterns_dir = get_theme_file_path( 'patterns' );
    if ( is_dir( $patterns_dir ) ) {
        $pattern_files = glob( $patterns_dir . '/*.html' );
        foreach ( $pattern_files as $file ) {
            $slug    = basename( $file, '.html' );
            $slug    = sanitize_title( $slug );
            $content = file_get_contents( $file );
            if ( $content ) {
                // Sanitizar HTML del patrón para prevenir XSS
                $content = wp_kses_post( $content );
                register_block_pattern(
                    'img2html/' . $slug,
                    array(
                        'title'       => sanitize_text_field( ucwords( str_replace( '-', ' ', $slug ) ) ),
                        'description' => sanitize_text_field( 'Patrón generado desde imágenes' ),
                        'content'     => $content,
                        'categories'  => array( 'img2html' ),
                    )
                );
            }
        }
    }
}
add_action( 'init', 'img2html_register_patterns' );

// Registrar bloques atómicos y organismos personalizados
function img2html_register_atomic_blocks() {
    $base   = get_template_directory() . '/blocks';
    $groups = array( 'atoms', 'molecules', 'organisms' );

    foreach ( $groups as $grp ) {
        $dir = $base . '/' . $grp;
        if ( is_dir( $dir ) ) {
            foreach ( glob( $dir . '/*', GLOB_ONLYDIR ) as $block_dir ) {
                $block_json = $block_dir . '/block.json';
                if ( file_exists( $block_json ) ) {
                    register_block_type( $block_dir );
                }
            }
        }
    }

    // Registrar también bloques en la raíz de /blocks (ej. /blocks/cta, /blocks/card, /blocks/hero)
    foreach ( glob( $base . '/*', GLOB_ONLYDIR ) as $block_dir ) {
        $name = basename( $block_dir );
        if ( in_array( $name, $groups, true ) ) {
            continue; // ya procesados
        }
        $block_json = $block_dir . '/block.json';
        if ( file_exists( $block_json ) ) {
            register_block_type( $block_dir );
        }
    }
}
add_action( 'init', 'img2html_register_atomic_blocks' );

// Inyectar Critical CSS inline para mejorar el rendimiento percibido
function img2html_critical_css() {
    $path     = get_theme_file_path( 'assets/css/critical.css' );
    $path_min = get_theme_file_path( 'assets/css/critical.min.css' );
    $use      = file_exists( $path_min ) ? $path_min : $path;

    if ( file_exists( $use ) ) {
        $critical_css = file_get_contents( $use );
        echo '<style id="img2html-critical-css">' . $critical_css . '</style>';
    }
}
add_action( 'wp_head', 'img2html_critical_css', 1 );
