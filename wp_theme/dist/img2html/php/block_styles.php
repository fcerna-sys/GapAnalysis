<?php
function img2html_register_block_styles(){
  register_block_style('core/table',['name'=>'striped','label'=>'Striped']);
  register_block_style('core/table',['name'=>'compact','label'=>'Compacta']);
  register_block_style('core/button',['name'=>'pill','label'=>'Pill']);
  register_block_style('core/button',['name'=>'ghost','label'=>'Ghost']);
  register_block_style('core/image',['name'=>'rounded','label'=>'Redondeada']);
  register_block_style('core/group',['name'=>'card','label'=>'Card']);
  register_block_style('core/quote',['name'=>'highlight','label'=>'Destacada']);
}
add_action('init','img2html_register_block_styles');