<?php
function img2html_send_security_headers(){
  header('X-Frame-Options: SAMEORIGIN');
  header('X-Content-Type-Options: nosniff');
  header('Referrer-Policy: strict-origin-when-cross-origin');
  header('Permissions-Policy: camera=(), microphone=(), geolocation=()');
  $csp = "default-src 'self'; img-src 'self' data: https:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; font-src 'self' https: data:; connect-src 'self' https:";
  header('Content-Security-Policy: '.$csp);
}
add_action('send_headers','img2html_send_security_headers');