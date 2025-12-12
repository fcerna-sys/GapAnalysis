<?php
$title = isset($attributes['title']) ? $attributes['title'] : 'Título destacado';
$subtitle = isset($attributes['subtitle']) ? $attributes['subtitle'] : 'Subtítulo breve';
$btnText = isset($attributes['buttonText']) ? $attributes['buttonText'] : 'Empezar';
$btnUrl = isset($attributes['buttonUrl']) ? $attributes['buttonUrl'] : '#';
$sticky = !empty($attributes['sticky']);
$transparent = !empty($attributes['transparent']);
$dark = !empty($attributes['darkBackground']);
$align = isset($attributes['align']) ? $attributes['align'] : 'left';
$base = function_exists('img2html_bem') ? img2html_bem('hero') : 'img2html-hero';
$btn_base = function_exists('img2html_bem') ? img2html_bem('button') : 'img2html-button';
$btn_primary = function_exists('img2html_bem') ? img2html_bem('button','primary') : 'img2html-button__primary';
$mod_cls = $base;
if ($sticky) { $mod_cls .= ' '.(function_exists('img2html_bem') ? img2html_bem('hero','', 'sticky') : $base.'--sticky'); }
if ($transparent) { $mod_cls .= ' '.(function_exists('img2html_bem') ? img2html_bem('hero','', 'transparent') : $base.'--transparent'); }
if ($dark) { $mod_cls .= ' '.(function_exists('img2html_bem') ? img2html_bem('hero','', 'dark') : $base.'--dark'); }
if ($align === 'center') { $mod_cls .= ' '.(function_exists('img2html_bem') ? img2html_bem('hero','', 'center') : $base.'--center'); }
if ($align === 'right') { $mod_cls .= ' '.(function_exists('img2html_bem') ? img2html_bem('hero','', 'right') : $base.'--right'); }
?>
<section class="<?php echo esc_attr($mod_cls); ?>">
  <h1 class="<?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('hero','title') : $base.'__title'); ?>"><?php echo esc_html($title); ?></h1>
  <p class="<?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('hero','subtitle') : $base.'__subtitle'); ?>"><?php echo esc_html($subtitle); ?></p>
  <div class="wp-block-buttons <?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('hero','actions') : $base.'__actions'); ?>">
    <div class="wp-block-button <?php echo esc_attr($btn_base.' '.$btn_primary); ?>">
      <a class="wp-block-button__link" href="<?php echo esc_url($btnUrl); ?>"><?php echo esc_html($btnText); ?></a>
    </div>
  </div>
</section>
