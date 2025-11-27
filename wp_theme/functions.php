<?php
$dir = get_theme_file_path('php');
if (is_dir($dir)){
  foreach (glob($dir.'/*.php') as $file){
    require_once $file;
  }
}