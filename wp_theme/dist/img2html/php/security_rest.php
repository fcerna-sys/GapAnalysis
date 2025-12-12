<?php
function img2html_harden_rest($endpoints){
  if (!is_user_logged_in()){
    unset($endpoints['/wp/v2/users']);
    foreach ($endpoints as $key => $_){
      if (strpos($key,'/wp/v2/users/') === 0){ unset($endpoints[$key]); }
    }
  }
  return $endpoints;
}
add_filter('rest_endpoints','img2html_harden_rest');