<?php
function img2html_woocommerce_support(){
  add_theme_support('woocommerce');
}
add_action('after_setup_theme','img2html_woocommerce_support');