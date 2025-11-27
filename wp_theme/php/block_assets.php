<?php
function img2html_enqueue_block_manifest_assets(){
  $manifest_path = get_theme_file_path('blocks-manifest.php');
  if (!file_exists($manifest_path)) return;
  $manifest = include $manifest_path;
  if (!is_array($manifest)) return;

  $version_of = function($rel){
    $path = get_theme_file_path($rel);
    return file_exists($path) ? filemtime($path) : null;
  };

  $enqueue_for_editor = function() use ($manifest){
    foreach ($manifest as $block => $cfg){
      $styles = isset($cfg['style']) ? (array)$cfg['style'] : [];
      $scripts = isset($cfg['script']) ? (array)$cfg['script'] : [];
      $deps_style = isset($cfg['deps_style']) ? (array)$cfg['deps_style'] : [];
      $deps_script = isset($cfg['deps_script']) ? (array)$cfg['deps_script'] : [];
      $version = isset($cfg['version']) ? $cfg['version'] : null;
      foreach ($styles as $rel){
        $uri = get_theme_file_uri($rel);
        $path = get_theme_file_path($rel);
        if (file_exists($path)){
          $ver = $version ? $version : filemtime($path);
          wp_enqueue_style('img2html-block-'.md5($block.$rel), $uri, $deps_style, $ver);
        }
      }
      foreach ($scripts as $rel){
        $uri = get_theme_file_uri($rel);
        $path = get_theme_file_path($rel);
        if (file_exists($path)){
          $ver = $version ? $version : filemtime($path);
          wp_enqueue_script('img2html-block-'.md5($block.$rel), $uri, $deps_script, $ver, true);
        }
      }
    }
  };

  $enqueue_for_front = function() use ($manifest){
    if (!is_singular()) return;
    global $post;
    if (!$post) return;
    $content = $post->post_content;
    foreach ($manifest as $block => $cfg){
      if (has_block($block, $content)){
        $styles = isset($cfg['style']) ? (array)$cfg['style'] : [];
        $scripts = isset($cfg['script']) ? (array)$cfg['script'] : [];
        $deps_style = isset($cfg['deps_style']) ? (array)$cfg['deps_style'] : [];
        $deps_script = isset($cfg['deps_script']) ? (array)$cfg['deps_script'] : [];
        $version = isset($cfg['version']) ? $cfg['version'] : null;
        foreach ($styles as $rel){
          $uri = get_theme_file_uri($rel);
          $path = get_theme_file_path($rel);
          if (file_exists($path)){
            $ver = $version ? $version : filemtime($path);
            wp_enqueue_style('img2html-block-'.md5($block.$rel), $uri, $deps_style, $ver);
          }
        }
        foreach ($scripts as $rel){
          $uri = get_theme_file_uri($rel);
          $path = get_theme_file_path($rel);
          if (file_exists($path)){
            $ver = $version ? $version : filemtime($path);
            wp_enqueue_script('img2html-block-'.md5($block.$rel), $uri, $deps_script, $ver, true);
          }
        }
      }
    }
  };

  if (!is_admin()){
    $enqueue_on_render = function($content, $block) use ($manifest){
      $name = isset($block['blockName']) ? $block['blockName'] : null;
      if (!$name || !isset($manifest[$name])) return $content;
      $cfg = $manifest[$name];
      $styles = isset($cfg['style']) ? (array)$cfg['style'] : [];
      $scripts = isset($cfg['script']) ? (array)$cfg['script'] : [];
      $deps_style = isset($cfg['deps_style']) ? (array)$cfg['deps_style'] : [];
      $deps_script = isset($cfg['deps_script']) ? (array)$cfg['deps_script'] : [];
      $version = isset($cfg['version']) ? $cfg['version'] : null;
      foreach ($styles as $rel){
        $uri = get_theme_file_uri($rel);
        $path = get_theme_file_path($rel);
        if (file_exists($path)){
          $ver = $version ? $version : filemtime($path);
          wp_enqueue_style('img2html-block-'.md5($name.$rel), $uri, $deps_style, $ver);
        }
      }
      foreach ($scripts as $rel){
        $uri = get_theme_file_uri($rel);
        $path = get_theme_file_path($rel);
        if (file_exists($path)){
          $ver = $version ? $version : filemtime($path);
          wp_enqueue_script('img2html-block-'.md5($name.$rel), $uri, $deps_script, $ver, true);
        }
      }
      return $content;
    };
    add_filter('render_block', $enqueue_on_render, 10, 2);
  }

  add_action('enqueue_block_editor_assets', $enqueue_for_editor);
  add_action('wp_enqueue_scripts', $enqueue_for_front);
}
add_action('init','img2html_enqueue_block_manifest_assets');