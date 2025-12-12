<?php
if (!defined('ABSPATH')) { exit; }

class Img2HTML_Walker_Nav_Menu extends Walker_Nav_Menu {
  private $mega_stack = [];
  public function start_lvl( &$output, $depth = 0, $args = [] ) {
    $indent = str_repeat("\t", $depth);
    $is_mega = !empty($this->mega_stack[$depth]);
    if ($is_mega && $depth === 0){
      $output .= "\n$indent<div class=\"mega-menu\"><ul class=\"mega-menu__list\">\n";
    } else {
      $output .= "\n$indent<ul class=\"sub-menu\">\n";
    }
  }

  public function end_lvl( &$output, $depth = 0, $args = [] ) {
    $indent = str_repeat("\t", $depth);
    $is_mega = !empty($this->mega_stack[$depth]);
    if ($is_mega && $depth === 0){
      $output .= "$indent</ul></div>\n";
    } else {
      $output .= "$indent</ul>\n";
    }
  }

  public function start_el( &$output, $item, $depth = 0, $args = [], $id = 0 ) {
    $icon   = get_post_meta( $item->ID, '_menu_icon', true );
    $badge  = get_post_meta( $item->ID, '_menu_badge', true );
    $color  = get_post_meta( $item->ID, '_menu_color', true );
    $title_alt = get_post_meta( $item->ID, '_menu_title_alt', true );
    $desc   = get_post_meta( $item->ID, '_menu_desc', true );
    $fs     = get_post_meta( $item->ID, '_menu_font_size', true );
    $fw     = get_post_meta( $item->ID, '_menu_font_weight', true );
    $ff     = get_post_meta( $item->ID, '_menu_font_family', true );
    $pad    = get_post_meta( $item->ID, '_menu_padding', true );
    $mega   = get_post_meta( $item->ID, '_menu_megamenu', true );
    $is_heading = get_post_meta( $item->ID, '_menu_is_heading', true );
    if ($depth === 0){ $this->mega_stack[0] = (bool)$mega; }

    $styles = [];
    if ($color) $styles[] = 'color:'.esc_attr($color);
    if ($fs)    $styles[] = 'font-size:'.esc_attr($fs);
    if ($fw)    $styles[] = 'font-weight:'.esc_attr($fw);
    if ($ff)    $styles[] = 'font-family:'.esc_attr($ff);
    if ($pad)   $styles[] = 'padding:'.esc_attr($pad);
    $style_attr = $styles ? ' style="'.implode(';', $styles).'"' : '';

    $classes = empty( $item->classes ) ? [] : (array) $item->classes;
    $classes[] = 'menu-item';
    if ($mega && $depth === 0) { $classes[] = 'menu-item--mega'; }
    if ($is_heading && $depth > 0) { $classes[] = 'mega-heading'; }
    $class_names = ' class="'. esc_attr( implode( ' ', array_filter( $classes ) ) ) .'"';

    $output .= '<li'. $class_names .'>';
    $atts = ' href="'. esc_url( $item->url ) .'"';
    $output .= '<a'. $atts . $style_attr .'>';

    if ( $icon ) {
      $output .= '<span class="menu-icon img2html-menu__icon '. esc_attr( $icon ) .'"></span> ';
    }

    $label = $title_alt ? $title_alt : $item->title;
    $output .= '<span class="menu-text">'. esc_html( $label ) .'</span>';

    if ( $badge ) {
      $output .= '<span class="menu-badge img2html-menu__badge">'. esc_html( $badge ) .'</span>';
    }

    if ( $desc ) {
      $output .= '<small class="menu-desc">'. esc_html( $desc ) .'</small>';
    }

    $output .= '</a>';
  }

  public function end_el( &$output, $item, $depth = 0, $args = [] ) {
    $output .= '</li>';
  }
}
