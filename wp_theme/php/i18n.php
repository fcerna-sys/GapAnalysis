<?php
function img2html_load_textdomain(){
  load_theme_textdomain('img2html', get_theme_file_path('languages'));
}
add_action('after_setup_theme','img2html_load_textdomain');