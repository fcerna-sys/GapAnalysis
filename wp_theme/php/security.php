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

function img2html_secure_upload_mimes($mimes){
  unset($mimes['svg']);
  unset($mimes['svgz']);
  return $mimes;
}
add_filter('upload_mimes','img2html_secure_upload_mimes');

function img2html_upload_prefilter($file){
  $name = isset($file['name']) ? $file['name'] : '';
  $tmp = isset($file['tmp_name']) ? $file['tmp_name'] : '';
  $ext = strtolower(pathinfo($name, PATHINFO_EXTENSION));
  $danger = ['php','phtml','pht','phar','shtml','cgi','pl'];
  if (in_array($ext, $danger, true)){
    $file['error'] = 'Tipo de archivo no permitido.';
    return $file;
  }
  if (!is_uploaded_file($tmp)){
    $file['error'] = 'Carga inválida.';
    return $file;
  }
  $allowed = get_allowed_mime_types();
  $check = wp_check_filetype_and_ext($tmp, $name, $allowed);
  if (empty($check['type']) || empty($check['ext'])){
    $file['error'] = 'Extensión o tipo de archivo no válidos.';
    return $file;
  }
  $img_ext = ['jpg','jpeg','png','gif','webp','bmp'];
  if (in_array($check['ext'], $img_ext, true)){
    if (!@getimagesize($tmp)){
      $file['error'] = 'Imagen inválida.';
      return $file;
    }
  }
  $sample = @file_get_contents($tmp, false, null, 0, 4096);
  if ($sample !== false){
    if (preg_match('/<\?php|<script\b|onload=|onerror=|base64,|data:\s*text\/html/i', $sample)){
      $file['error'] = 'Contenido potencialmente peligroso.';
      return $file;
    }
  }
  return $file;
}
add_filter('wp_handle_upload_prefilter','img2html_upload_prefilter');

function img2html_harden_uploads_dir(){
  $u = wp_upload_dir();
  $base = isset($u['basedir']) ? $u['basedir'] : null;
  if (!$base || !is_dir($base)) return;
  $htaccess = $base.'/.htaccess';
  $webconfig = $base.'/web.config';
  $hta = "<IfModule mod_php7.c>\n  php_admin_flag engine off\n</IfModule>\n<IfModule mod_php8.c>\n  php_admin_flag engine off\n</IfModule>\n<FilesMatch \"\\.(php|phtml|pht|phar|shtml|cgi|pl)$\">\n  Require all denied\n</FilesMatch>\nOptions -ExecCGI\n";
  $wconf = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<configuration>\n  <system.webServer>\n    <security>\n      <requestFiltering>\n        <fileExtensions>\n          <add fileExtension=\".php\" allowed=\"false\" />\n          <add fileExtension=\".phtml\" allowed=\"false\" />\n          <add fileExtension=\".pht\" allowed=\"false\" />\n          <add fileExtension=\".phar\" allowed=\"false\" />\n          <add fileExtension=\".shtml\" allowed=\"false\" />\n          <add fileExtension=\".cgi\" allowed=\"false\" />\n          <add fileExtension=\".pl\" allowed=\"false\" />\n        </fileExtensions>\n      </requestFiltering>\n    </security>\n  </system.webServer>\n</configuration>\n";
  if (!file_exists($htaccess)) @file_put_contents($htaccess, $hta);
  if (!file_exists($webconfig)) @file_put_contents($webconfig, $wconf);
}
add_action('after_switch_theme','img2html_harden_uploads_dir');

add_filter('sanitize_file_name', function($filename){
  $filename = remove_accents($filename);
  $filename = preg_replace('/[^a-zA-Z0-9_\.-]/', '-', $filename);
  $filename = preg_replace('/-+/', '-', $filename);
  return strtolower(trim($filename, '-'));
}, 10);

add_action('send_headers', function(){
  if (is_admin()) return;
  header('X-Frame-Options: SAMEORIGIN');
  header('X-Content-Type-Options: nosniff');
  header('Referrer-Policy: strict-origin-when-cross-origin');
  header('Permissions-Policy: geolocation=(), microphone=(), camera=()');
  if (is_ssl()) header('Strict-Transport-Security: max-age=31536000; includeSubDomains');
});
