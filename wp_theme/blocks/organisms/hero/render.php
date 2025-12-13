<?php
$title = isset($attributes['title']) ? $attributes['title'] : 'Título destacado';
$subtitle = isset($attributes['subtitle']) ? $attributes['subtitle'] : 'Subtítulo breve';
$btnText = isset($attributes['buttonText']) ? $attributes['buttonText'] : 'Empezar';
$btnUrl = isset($attributes['buttonUrl']) ? $attributes['buttonUrl'] : '#';
$sticky = !empty($attributes['sticky']);
$transparent = !empty($attributes['transparent']);
$dark = !empty($attributes['darkBackground']);
$align = isset($attributes['align']) ? $attributes['align'] : 'left';
$image = isset($attributes['imageUrl']) ? $attributes['imageUrl'] : '';
$imageAlt = isset($attributes['imageAlt']) ? $attributes['imageAlt'] : '';
$base = function_exists('img2html_bem') ? img2html_bem('hero') : 'img2html-hero';
$btn_base = function_exists('img2html_bem') ? img2html_bem('button') : 'img2html-button';
$btn_primary = function_exists('img2html_bem') ? img2html_bem('button','', 'primary') : 'img2html-button--primary';
$mod_cls = $base;
if ($sticky) { $mod_cls .= ' '.(function_exists('img2html_bem') ? img2html_bem('hero','', 'sticky') : $base.'--sticky'); }
if ($transparent) { $mod_cls .= ' '.(function_exists('img2html_bem') ? img2html_bem('hero','', 'transparent') : $base.'--transparent'); }
if ($dark) { $mod_cls .= ' '.(function_exists('img2html_bem') ? img2html_bem('hero','', 'dark') : $base.'--dark'); }
if ($align === 'center') { $mod_cls .= ' '.(function_exists('img2html_bem') ? img2html_bem('hero','', 'center') : $base.'--center'); }
if ($align === 'right') { $mod_cls .= ' '.(function_exists('img2html_bem') ? img2html_bem('hero','', 'right') : $base.'--right'); }
$extra = (isset($attributes['className']) && is_string($attributes['className'])) ? ' '.sanitize_html_class($attributes['className']) : '';
?>
<section class="<?php echo esc_attr($mod_cls.$extra); ?>">
  <?php if (!empty($image)): ?>
    <div class="<?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('hero','layout') : $base.'__layout'); ?>">
      <div class="<?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('hero','media') : $base.'__media'); ?>">
        <img src="<?php echo esc_url($image); ?>" alt="<?php echo esc_attr($imageAlt); ?>" />
      </div>
      <div class="<?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('hero','content') : $base.'__content'); ?>">
        <h1 class="<?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('hero','title') : $base.'__title'); ?>"><?php echo esc_html($title); ?></h1>
        <p class="<?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('hero','subtitle') : $base.'__subtitle'); ?>"><?php echo esc_html($subtitle); ?></p>
        <div class="wp-block-buttons <?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('hero','actions') : $base.'__actions'); ?>">
          <?php $hero_btn = function_exists('img2html_bem') ? img2html_bem('hero','button') : $base.'__button'; $hero_btn_primary = function_exists('img2html_bem') ? img2html_bem('hero','button','primary') : $base.'__button--primary'; ?>
          <div class="wp-block-button <?php echo esc_attr($btn_base.' '.$btn_primary.' '.$hero_btn.' '.$hero_btn_primary); ?>">
            <a class="wp-block-button__link" href="<?php echo esc_url($btnUrl); ?>"><?php echo esc_html($btnText); ?></a>
          </div>
        </div>
      </div>
    </div>
  <?php else: ?>
    <h1 class="<?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('hero','title') : $base.'__title'); ?>"><?php echo esc_html($title); ?></h1>
    <p class="<?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('hero','subtitle') : $base.'__subtitle'); ?>"><?php echo esc_html($subtitle); ?></p>
    <div class="wp-block-buttons <?php echo esc_attr(function_exists('img2html_bem') ? img2html_bem('hero','actions') : $base.'__actions'); ?>">
      <div class="wp-block-button <?php echo esc_attr($btn_base.' '.$btn_primary); ?>">
        <a class="wp-block-button__link" href="<?php echo esc_url($btnUrl); ?>"><?php echo esc_html($btnText); ?></a>
      </div>
    </div>
  <?php endif; ?>
</section>
