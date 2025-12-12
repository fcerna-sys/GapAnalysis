<?php
if (!defined('ABSPATH')) { exit; }

function img2html_register_block_styles(){
  $styles = [
    'core/paragraph' => [
      ['name'=>'lead','label'=>'Lead'],
      ['name'=>'muted','label'=>'Muted']
    ],
    'core/button' => [
      ['name'=>'outline','label'=>'Outline'],
      ['name'=>'ghost','label'=>'Ghost'],
      ['name'=>'pill','label'=>'Pill']
    ],
    'core/navigation' => [
      ['name'=>'underline','label'=>'Underline']
    ],
    'img2html/classic-menu' => [
      ['name'=>'underline','label'=>'Underline'],
      ['name'=>'pill','label'=>'Pill'],
      ['name'=>'ghost','label'=>'Ghost'],
      ['name'=>'compact','label'=>'Compact']
    ]
  ];
  foreach ($styles as $block=>$defs){
    foreach ($defs as $def){
      register_block_style($block, [
        'name'  => sanitize_key($def['name']),
        'label' => sanitize_text_field($def['label'])
      ]);
    }
  }
}
add_action('init','img2html_register_block_styles');
