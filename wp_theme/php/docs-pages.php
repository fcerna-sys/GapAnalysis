<?php
function img2html_create_docs_pages(){
  $pages = [
    [ 'title' => 'Component Library', 'slug' => 'component-library', 'template' => 'component-library' ],
    [ 'title' => 'Pattern Preview',   'slug' => 'pattern-preview',   'template' => 'pattern-preview' ],
    [ 'title' => 'Style Guide',       'slug' => 'styleguide',        'template' => 'styleguide' ],
    [ 'title' => 'Atomic Index',      'slug' => 'atomic-index',      'template' => 'atomic-index' ],
  ];
  foreach ($pages as $p){
    $slug = sanitize_title($p['slug']);
    $existing = get_page_by_path($slug);
    if ($existing && $existing->post_type === 'page'){
      update_post_meta($existing->ID, '_wp_page_template', $p['template']);
      continue;
    }
    $post_id = wp_insert_post([
      'post_title'   => sanitize_text_field($p['title']),
      'post_name'    => $slug,
      'post_type'    => 'page',
      'post_status'  => 'publish',
      'post_content' => ''
    ], true);
    if (!is_wp_error($post_id)){
      update_post_meta($post_id, '_wp_page_template', $p['template']);
    }
  }
}
add_action('after_switch_theme','img2html_create_docs_pages');
