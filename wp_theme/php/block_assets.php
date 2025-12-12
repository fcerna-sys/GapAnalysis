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

    $components_dir = get_theme_file_path('assets/components');
    if (is_dir($components_dir)){
      foreach (glob($components_dir.'/*.css') as $css){
        $rel = str_replace(get_theme_file_path(''), '', $css);
        $uri = get_theme_file_uri('assets/components/'.basename($css));
        wp_enqueue_style('img2html-component-'.md5($rel), $uri, [], filemtime($css));
      }
      foreach (glob($components_dir.'/*.js') as $js){
        $rel = str_replace(get_theme_file_path(''), '', $js);
        $uri = get_theme_file_uri('assets/components/'.basename($js));
        wp_enqueue_script('img2html-component-'.md5($rel), $uri, [], filemtime($js), true);
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
      if ($name && isset($manifest[$name])){
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
      }

      static $enqueued_components = [];
      $classes = [];
      $bem_prefix = function_exists('img2html_bem_prefix') ? img2html_bem_prefix() : 'img2html';
      if (isset($block['attrs']['className']) && is_string($block['attrs']['className'])){
        foreach (preg_split('/\s+/', $block['attrs']['className']) as $cls){
          if (strpos($cls, $bem_prefix.'-') === 0 || strpos($cls, 'img2html-') === 0) $classes[] = $cls;
        }
      }
      if (is_string($content)){
        if (preg_match_all('/class="([^"]+)"/', $content, $m)){
          foreach ($m[1] as $classAttr){
            foreach (preg_split('/\s+/', $classAttr) as $cls){
              if (strpos($cls, $bem_prefix.'-') === 0 || strpos($cls, 'img2html-') === 0) $classes[] = $cls;
            }
          }
        }
      }
      $classes = array_unique($classes);
      foreach ($classes as $cls){
        $base = preg_replace('/(__.*$|--.*$)/', '', $cls);
        if (isset($enqueued_components[$base])) continue;
        $css_rel = 'assets/components/'.$base.'.css';
        $js_rel = 'assets/components/'.$base.'.js';
        $css_path = get_theme_file_path($css_rel);
        $js_path = get_theme_file_path($js_rel);
        // Fallback a prefijo 'img2html-' si no existe el archivo para prefijo dinámico
        if (!file_exists($css_path)){
          $fallback_base = preg_replace('/^[^-]+-/', 'img2html-', $base);
          $css_rel = 'assets/components/'.$fallback_base.'.css';
          $css_path = get_theme_file_path($css_rel);
        }
        if (!file_exists($js_path)){
          $fallback_base = preg_replace('/^[^-]+-/', 'img2html-', $base);
          $js_rel = 'assets/components/'.$fallback_base.'.js';
          $js_path = get_theme_file_path($js_rel);
        }
        if (file_exists($css_path)){
          wp_enqueue_style('img2html-component-'.md5($base.$css_rel), get_theme_file_uri($css_rel), [], filemtime($css_path));
        }
        if (file_exists($js_path)){
          wp_enqueue_script('img2html-component-'.md5($base.$js_rel), get_theme_file_uri($js_rel), [], filemtime($js_path), true);
        }
        $enqueued_components[$base] = true;
      }
      return $content;
    };
    add_filter('render_block', $enqueue_on_render, 10, 2);
  }

  add_action('enqueue_block_editor_assets', $enqueue_for_editor);
  add_action('wp_enqueue_scripts', $enqueue_for_front);
}
add_action('init','img2html_enqueue_block_manifest_assets');
