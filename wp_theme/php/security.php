<?php
remove_action('wp_head','wp_generator');
remove_action('wp_head','rsd_link');
remove_action('wp_head','wlwmanifest_link');
remove_action('wp_head','wp_shortlink_wp_head');
remove_action('wp_head','wp_oembed_add_discovery_links');
remove_action('wp_head','wp_oembed_add_host_js');
add_filter('xmlrpc_enabled','__return_false');
add_filter('wp_is_application_passwords_available','__return_false');
add_filter('login_errors', function(){ return null; });