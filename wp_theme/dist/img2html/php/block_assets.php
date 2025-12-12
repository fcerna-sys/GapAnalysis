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
        $rel_min = preg_replace('/\.css$/', '.min.css', $rel);
        $path_min = get_theme_file_path($rel_min);
        $use_rel = file_exists($path_min) ? $rel_min : $rel;
        $uri = get_theme_file_uri($use_rel);
        $path = get_theme_file_path($use_rel);
        if (file_exists($path)){
          $ver = $version ? $version : filemtime($path);
          wp_enqueue_style('img2html-block-'.md5($block.$use_rel), $uri, $deps_style, $ver);
        }
      }
      foreach ($scripts as $rel){
        $rel_min = preg_replace('/\.js$/', '.min.js', $rel);
        $path_min = get_theme_file_path($rel_min);
        $use_rel = file_exists($path_min) ? $rel_min : $rel;
        $uri = get_theme_file_uri($use_rel);
        $path = get_theme_file_path($use_rel);
        $async = !empty($cfg['async']);
        $defer = !empty($cfg['defer']);
        if (file_exists($path)){
          $ver = $version ? $version : filemtime($path);
          $handle = 'img2html-block-'.md5($block.$use_rel);
          wp_enqueue_script($handle, $uri, $deps_script, $ver, true);
          if ($async) wp_script_add_data($handle, 'async', true);
          if ($defer) wp_script_add_data($handle, 'defer', true);
        }
      }
    }

    $components_dir = get_theme_file_path('assets/components');
    if (is_dir($components_dir)){
      foreach (glob($components_dir.'/*.css') as $css){
        if (preg_match('/\.min\.css$/', $css)) continue;
        $min = preg_replace('/\.css$/','.min.css',$css);
        $use = file_exists($min) ? $min : $css;
        $rel = str_replace(get_theme_file_path(''), '', $use);
        $uri = get_theme_file_uri('assets/components/'.basename($use));
        wp_enqueue_style('img2html-component-'.md5($rel), $uri, [], filemtime($use));
      }
      foreach (glob($components_dir.'/*.js') as $js){
        if (preg_match('/\.min\.js$/', $js)) continue;
        $min = preg_replace('/\.js$/','.min.js',$js);
        $use = file_exists($min) ? $min : $js;
        $rel = str_replace(get_theme_file_path(''), '', $use);
        $uri = get_theme_file_uri('assets/components/'.basename($use));
        wp_enqueue_script('img2html-component-'.md5($rel), $uri, [], filemtime($use), true);
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
          $rel_min = preg_replace('/\.css$/', '.min.css', $rel);
          $path_min = get_theme_file_path($rel_min);
          $use_rel = file_exists($path_min) ? $rel_min : $rel;
          $uri = get_theme_file_uri($use_rel);
          $path = get_theme_file_path($use_rel);
          if (file_exists($path)){
            $ver = $version ? $version : filemtime($path);
            wp_enqueue_style('img2html-block-'.md5($block.$use_rel), $uri, $deps_style, $ver);
          }
        }
        foreach ($scripts as $rel){
          $rel_min = preg_replace('/\.js$/', '.min.js', $rel);
          $path_min = get_theme_file_path($rel_min);
          $use_rel = file_exists($path_min) ? $rel_min : $rel;
          $uri = get_theme_file_uri($use_rel);
          $path = get_theme_file_path($use_rel);
          $async = !empty($cfg['async']);
          $defer = !empty($cfg['defer']);
          if (file_exists($path)){
            $ver = $version ? $version : filemtime($path);
            $handle = 'img2html-block-'.md5($block.$use_rel);
            wp_enqueue_script($handle, $uri, $deps_script, $ver, true);
            if ($async) wp_script_add_data($handle, 'async', true);
            if ($defer) wp_script_add_data($handle, 'defer', true);
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
          $rel_min = preg_replace('/\.css$/', '.min.css', $rel);
          $path_min = get_theme_file_path($rel_min);
          $use_rel = file_exists($path_min) ? $rel_min : $rel;
          $uri = get_theme_file_uri($use_rel);
          $path = get_theme_file_path($use_rel);
          if (file_exists($path)){
            $ver = $version ? $version : filemtime($path);
            wp_enqueue_style('img2html-block-'.md5($name.$use_rel), $uri, $deps_style, $ver);
          }
        }
        foreach ($scripts as $rel){
          $rel_min = preg_replace('/\.js$/', '.min.js', $rel);
          $path_min = get_theme_file_path($rel_min);
          $use_rel = file_exists($path_min) ? $rel_min : $rel;
          $uri = get_theme_file_uri($use_rel);
          $path = get_theme_file_path($use_rel);
          if (file_exists($path)){
            $ver = $version ? $version : filemtime($path);
            $handle = 'img2html-block-'.md5($name.$use_rel);
            wp_enqueue_script($handle, $uri, $deps_script, $ver, true);
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
      // Evitar duplicidad: saltar componentes cubiertos por style.css del bloque
      $skip_map = [
        'img2html/organism-hero' => ['img2html-hero'],
        'img2html/molecule-card' => ['img2html-card'],
        'img2html/molecule-testimonial' => ['img2html-testimonial'],
        'img2html/molecule-features-list' => ['img2html-features-list'],
        'img2html/molecule-team-member' => ['img2html-team-member'],
        'img2html/atom-button' => ['img2html-button'],
        'img2html/atom-container' => ['img2html-container'],
        'img2html/atom-icon' => ['img2html-icon'],
        'img2html/atom-paragraph' => ['img2html-paragraph'],
        'img2html/atom-input' => ['img2html-input'],
        'img2html/atom-badge' => ['img2html-badge'],
        'img2html/atom-link' => ['img2html-link']
      ];
      foreach ($classes as $cls){
        if ($name && isset($skip_map[$name])){
          foreach ($skip_map[$name] as $skip_base){
            if (strpos($cls, $skip_base) === 0) { continue 1; }
          }
        }
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
          $css_rel_min = preg_replace('/\.css$/', '.min.css', $css_rel);
          $css_path_min = get_theme_file_path($css_rel_min);
          $css_use_rel = file_exists($css_path_min) ? $css_rel_min : $css_rel;
          $css_use_path = file_exists($css_path_min) ? $css_path_min : $css_path;
          wp_enqueue_style('img2html-component-'.md5($base.$css_use_rel), get_theme_file_uri($css_use_rel), [], filemtime($css_use_path));
        }
        if (file_exists($js_path)){
          $js_rel_min = preg_replace('/\.js$/', '.min.js', $js_rel);
          $js_path_min = get_theme_file_path($js_rel_min);
          $js_use_rel = file_exists($js_path_min) ? $js_rel_min : $js_rel;
          $js_use_path = file_exists($js_path_min) ? $js_path_min : $js_path;
          wp_enqueue_script('img2html-component-'.md5($base.$js_use_rel), get_theme_file_uri($js_use_rel), [], filemtime($js_use_path), true);
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
