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
}
add_action('init','img2html_register_block_variations');