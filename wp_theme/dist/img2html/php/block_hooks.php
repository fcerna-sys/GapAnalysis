<?php
function img2html_cta_after_page($content){
  if (is_singular('page') && in_the_loop() && is_main_query()){
    $cta = '<!-- wp:group {"layout":{"type":"constrained"}} --><div class="wp-block-group"><!-- wp:heading {"level":3} --><h3>¿Te interesa?</h3><!-- /wp:heading --><!-- wp:buttons --><div class="wp-block-buttons"><!-- wp:button {"backgroundColor":"primary"} --><div class="wp-block-button"><a class="wp-block-button__link has-primary-background-color has-background">Contáctanos</a></div><!-- /wp:button --></div><!-- /wp:buttons --></div><!-- /wp:group -->';
    $content .= $cta;
  }
  return $content;
}
add_filter('the_content','img2html_cta_after_page',20);