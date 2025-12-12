<?php
if (!defined('ABSPATH')) { exit; }
$loc = isset($attributes['location']) ? sanitize_key($attributes['location']) : 'primary_menu';
$menu_class = isset($attributes['menuClass']) ? sanitize_html_class($attributes['menuClass']) : 'menu-principal';
$depth = isset($attributes['depth']) ? max(1, intval($attributes['depth'])) : 3;
$menu_id = isset($attributes['menuId']) ? intval($attributes['menuId']) : 0;
$menu_style = isset($attributes['menuStyle']) ? sanitize_key($attributes['menuStyle']) : 'default';
if ($menu_style === 'compact-pill') {
  $menu_class .= ' menu--pill menu--compact';
} else if ($menu_style === 'compact-ghost') {
  $menu_class .= ' menu--ghost menu--compact';
} else if ($menu_style === 'compact-underline') {
  $menu_class .= ' menu--underline menu--compact';
} else if ($menu_style && $menu_style !== 'default') {
  $menu_class .= ' menu--'.$menu_style;
}
$compact = !empty($attributes['compact']);
if ($compact && strpos($menu_class, 'menu--compact') === false) { $menu_class .= ' menu--compact'; }
if (!class_exists('Img2HTML_Walker_Nav_Menu')){
  require_once get_theme_file_path('php/menu/class-app-walker.php');
}
if ($menu_id > 0){
  $obj = wp_get_nav_menu_object($menu_id);
  if (!$obj){
    echo '<div class="img2html-classic-menu__notice">Menú no encontrado</div>';
  } else {
    wp_nav_menu([
      'menu'           => $menu_id,
      'menu_class'     => $menu_class,
      'container'      => false,
      'depth'          => $depth,
      'walker'         => new Img2HTML_Walker_Nav_Menu()
    ]);
  }
} else if (!has_nav_menu($loc)){
  echo '<div class="img2html-classic-menu__notice">Asigna un menú a la ubicación seleccionada</div>';
} else {
  wp_nav_menu([
    'theme_location' => $loc,
    'menu_class'     => $menu_class,
    'container'      => false,
    'depth'          => $depth,
    'walker'         => new Img2HTML_Walker_Nav_Menu()
  ]);
}
