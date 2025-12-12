<?php
function img2html_skip_link(){
  echo '<a class="skip-link" href="#main-content">Saltar al contenido</a>';
}
add_action('wp_body_open','img2html_skip_link');