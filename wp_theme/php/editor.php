<?php
function img2html_editor_supports(){
  add_theme_support('title-tag');
  add_theme_support('responsive-embeds');
  add_theme_support('wp-block-styles');
  add_theme_support('align-wide');
  add_theme_support('html5',["search-form","comment-form","comment-list","gallery","caption","script","style"]);
  add_theme_support('appearance-tools');
}
add_action('after_setup_theme','img2html_editor_supports');