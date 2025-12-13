<?php
function img2html_register_block_variations(){
  register_block_variation('core/button',[
    'name'=>'button-cta',
    'title'=>'CTA primario',
    'attributes'=>[
      'className'=>'is-style-pill',
      'backgroundColor'=>'primary'
    ]
  ]);
  register_block_variation('core/table',[
    'name'=>'table-striped',
    'title'=>'Tabla rayada',
    'attributes'=>[
      'className'=>'is-style-striped'
    ]
  ]);
  register_block_variation('core/image',[
    'name'=>'image-rounded',
    'title'=>'Imagen redondeada',
    'attributes'=>[
      'className'=>'is-style-rounded'
    ]
  ]);
  register_block_variation('core/group',[
    'name'=>'group-card',
    'title'=>'Grupo tarjeta',
    'attributes'=>[
      'className'=>'is-style-card'
    ]
  ]);

  // Custom: Hero
  register_block_variation('img2html/organism-hero',[
    'name'=>'hero-centered',
    'title'=>'Hero centrado',
    'attributes'=>[
      'align'=>'center'
    ]
  ]);
  register_block_variation('img2html/organism-hero',[
    'name'=>'hero-image-left',
    'title'=>'Hero imagen izquierda',
    'attributes'=>[
      'className'=>'img2html-hero--image-left'
    ]
  ]);
  register_block_variation('img2html/organism-hero',[
    'name'=>'hero-image-right',
    'title'=>'Hero imagen derecha',
    'attributes'=>[
      'className'=>'img2html-hero--image-right'
    ]
  ]);

  // Custom: CTA
  register_block_variation('img2html/cta',[
    'name'=>'cta-gradient',
    'title'=>'CTA gradiente',
    'attributes'=>[
      'backgroundStyle'=>'gradient'
    ]
  ]);
  register_block_variation('img2html/cta',[
    'name'=>'cta-solid',
    'title'=>'CTA sólido',
    'attributes'=>[
      'backgroundStyle'=>'solid'
    ]
  ]);
  register_block_variation('img2html/cta',[
    'name'=>'cta-minimal',
    'title'=>'CTA minimal',
    'attributes'=>[
      'backgroundStyle'=>'minimal'
    ]
  ]);

  // Custom: Cards Grid
  register_block_variation('img2html/cards-grid',[
    'name'=>'cards-grid-3',
    'title'=>'Cards cuadrícula (3 columnas)',
    'attributes'=>[
      'columns'=>3
    ]
  ]);
  register_block_variation('img2html/cards-grid',[
    'name'=>'cards-list',
    'title'=>'Cards lista',
    'attributes'=>[
      'columns'=>1
    ]
  ]);
  register_block_variation('img2html/cards-grid',[
    'name'=>'cards-carousel',
    'title'=>'Cards carrusel',
    'attributes'=>[
      'className'=>'img2html-cards-grid--carousel'
    ]
  ]);

  // Custom: Atom Button
  register_block_variation('img2html/atom-button',[
    'name'=>'button-solid',
    'title'=>'Botón sólido',
    'attributes'=>[
      'variant'=>'primary'
    ]
  ]);
  register_block_variation('img2html/atom-button',[
    'name'=>'button-ghost',
    'title'=>'Botón ghost',
    'attributes'=>[
      'variant'=>'ghost'
    ]
  ]);
  register_block_variation('img2html/atom-button',[
    'name'=>'button-outline',
    'title'=>'Botón outline',
    'attributes'=>[
      'variant'=>'outline'
    ]
  ]);
}
add_action('init','img2html_register_block_variations');
