<?php
if (!defined('ABSPATH')) { exit; }
$file = isset($attributes['file']) ? sanitize_file_name($attributes['file']) : 'THEME_GUIDE.md';
$section = isset($attributes['section']) ? sanitize_text_field($attributes['section']) : '';
$show = !empty($attributes['showTitle']);
$search = (!isset($attributes['searchEnabled']) || $attributes['searchEnabled']);
$base = function_exists('img2html_bem_prefix') ? img2html_bem_prefix() : 'img2html';
$cls = $base.'-doc-viewer';
$path = get_theme_file_path('docs/'.$file);
$content = '';
if (file_exists($path)){
  $raw = file_get_contents($path);
  $ext = strtolower(pathinfo($file, PATHINFO_EXTENSION));
  if ($ext === 'md'){
    if ($section){
      $lines = preg_split('/\r?\n/', $raw);
      $capture = false; $buf = [];
      foreach ($lines as $ln){
        if (preg_match('/^##\s+(.+)$/', $ln, $m)){
          $title = trim($m[1]);
          if (!$capture && strcasecmp($title, $section) === 0){ $capture = true; continue; }
          if ($capture && strcasecmp($title, $section) !== 0){ break; }
        }
        if ($capture){ $buf[] = $ln; }
      }
      $raw = $buf ? implode("\n", $buf) : $raw;
    }
    $md = $raw;
    $lines = preg_split('/\r?\n/', $md);
    $out = '';
    $in_list = false;
    $linkify = function($line){
      $result = '';
      $offset = 0;
      while (preg_match('/\[(.*?)\]\((https?:\/\/[^\s)]+)\)/', $line, $m, PREG_OFFSET_CAPTURE, $offset)){
        $start = $m[0][1];
        $before = substr($line, $offset, $start - $offset);
        $result .= esc_html($before);
        $text = esc_html($m[1][0]);
        $url = esc_url($m[2][0]);
        $result .= '<a href="'.$url.'" rel="noopener">'.$text.'</a>';
        $offset = $start + strlen($m[0][0]);
      }
      $result .= esc_html(substr($line, $offset));
      return $result;
    };
    foreach ($lines as $ln){
      $t = trim($ln);
      if ($t === ''){ if ($in_list){ } else { $out .= ''; } continue; }
      if (preg_match('/^#{1}\s+(.*)$/', $t, $m)){
        if ($in_list){ $out .= '</ul>'; $in_list = false; }
        $out .= '<h1>'.$linkify($m[1]).'</h1>';
        continue;
      }
      if (preg_match('/^#{2}\s+(.*)$/', $t, $m)){
        if ($in_list){ $out .= '</ul>'; $in_list = false; }
        $out .= '<h2>'.$linkify($m[1]).'</h2>';
        continue;
      }
      if (preg_match('/^#{3}\s+(.*)$/', $t, $m)){
        if ($in_list){ $out .= '</ul>'; $in_list = false; }
        $out .= '<h3>'.$linkify($m[1]).'</h3>';
        continue;
      }
      if (preg_match('/^-\s+(.*)$/', $t, $m)){
        if (!$in_list){ $out .= '<ul>'; $in_list = true; }
        $out .= '<li>'.$linkify($m[1]).'</li>';
        continue;
      }
      if ($in_list){ $out .= '</ul>'; $in_list = false; }
      $out .= '<p>'.$linkify($t).'</p>';
    }
    if ($in_list){ $out .= '</ul>'; }
    $allowed = [
      'h1' => [], 'h2' => [], 'h3' => [], 'p' => [], 'ul' => [], 'li' => [],
      'a' => ['href' => true, 'rel' => true], 'span' => ['class' => true]
    ];
    $content = wp_kses($out, $allowed);
  } else {
    $body = '';
    if (preg_match('/<body[^>]*>([\s\S]*?)<\/body>/i', $raw, $m)){
      $body = $m[1];
    } else { $body = $raw; }
    $allowed = [
      'div'=>['class'=>true],'span'=>['class'=>true],'header'=>[],'nav'=>[],'main'=>[],'section'=>['id'=>true],
      'h1'=>[],'h2'=>[],'h3'=>[],'p'=>[],'a'=>['href'=>true,'rel'=>true],'code'=>[],'pre'=>[],'ul'=>[],'li'=>[],
      'table'=>[],'thead'=>[],'tbody'=>[],'tr'=>[],'th'=>[],'td'=>[]
    ];
    $content = wp_kses($body, $allowed);
  }
}
?>
<div class="<?php echo esc_attr($cls); ?>">
  <?php if ($show) { ?><div class="<?php echo esc_attr($cls.'__title'); ?>"><?php echo esc_html($file.($section? ' — '.$section : '')); ?></div><?php } ?>
  <?php if ($search) { ?>
    <div class="<?php echo esc_attr($cls.'__search'); ?>">
      <input type="search" placeholder="Buscar..." aria-label="Buscar" />
    </div>
  <?php } ?>
  <div class="<?php echo esc_attr($cls.'__content'); ?>" data-doc-viewer-content><?php echo $content; ?></div>
  <?php if ($search) { ?>
    <script>(function(){
      var root = document.currentScript && document.currentScript.parentNode ? document.currentScript.parentNode : null;
      if(!root) return; var box = root.querySelector('input[type="search"]'); var cont = root.querySelector('[data-doc-viewer-content]');
      if(!box || !cont) return; var markCls = '<?php echo esc_js($cls.'__mark'); ?>';
      function clear(){ var marks = cont.querySelectorAll('span.'+markCls); marks.forEach(function(m){ var t = document.createTextNode(m.textContent); m.parentNode.replaceChild(t, m); }); }
      function search(q){ clear(); if(!q) return; var walk = document.createTreeWalker(cont, NodeFilter.SHOW_TEXT, null); var nodes=[]; while(walk.nextNode()) nodes.push(walk.currentNode);
        nodes.forEach(function(n){ var s=n.nodeValue; var i=s.toLowerCase().indexOf(q.toLowerCase()); if(i>=0){ var before=s.slice(0,i), mid=s.slice(i,i+q.length), after=s.slice(i+q.length); var span=document.createElement('span'); span.className=markCls; span.textContent=mid; var frag=document.createDocumentFragment(); frag.appendChild(document.createTextNode(before)); frag.appendChild(span); frag.appendChild(document.createTextNode(after)); n.parentNode.replaceChild(frag,n); } }); }
      box.addEventListener('input', function(){ search(this.value.trim()); });
    })();</script>
  <?php } ?>
</div>
