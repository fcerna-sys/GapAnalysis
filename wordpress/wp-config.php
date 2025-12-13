<?php
define('DB_NAME', 'img2html');
define('DB_USER', 'root');
define('DB_PASSWORD', 'root');
define('DB_HOST', '127.0.0.1');
define('DB_CHARSET', 'utf8mb4');
define('DB_COLLATE', '');

define('AUTH_KEY', '5b5d6f8c4a1b9e7fa2c3d4e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6');
define('SECURE_AUTH_KEY', 'c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2');
define('LOGGED_IN_KEY', '9f8e7d6c5b4a3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8');
define('NONCE_KEY', 'a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7');
define('AUTH_SALT', 'e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1');
define('SECURE_AUTH_SALT', 'd0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0');
define('LOGGED_IN_SALT', 'f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e9d8c7b6a5f4');
define('NONCE_SALT', 'b6a5f4e3d2c1b0a9f8e7d6c5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6');

$table_prefix = 'wp_';

define('WP_DEBUG', false);
define('WP_HOME', 'http://127.0.0.1:8080');
define('WP_SITEURL', 'http://127.0.0.1:8080');
define('DISALLOW_FILE_EDIT', true);

if (!defined('ABSPATH')) {
    define('ABSPATH', __DIR__ . '/');
}
require_once ABSPATH . 'wp-settings.php';
