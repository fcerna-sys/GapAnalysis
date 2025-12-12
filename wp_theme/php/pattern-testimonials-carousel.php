<?php
add_action('init', function(){
    $slug = 'testimonials-carousel';
    $content = file_get_contents(get_theme_file_path('patterns/' . $slug . '.html'));
    if ($content) {
        $registry = WP_Block_Patterns_Registry::get_instance();
        if (!$registry->is_registered('img2html/' . $slug)) {
            register_block_pattern('img2html/' . $slug, array(
                'title' => 'Testimonials Carousel',
                'description' => 'Patrón',
                'content' => $content,
                'categories' => array('img2html'),
            ));
        }
    }
});
