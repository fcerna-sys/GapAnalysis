"""
Módulo para funciones de renderizado PHP de bloques.
Contiene TODAS las funciones _render_* y _generate_*_render_php.
Código completo migrado desde blocks_builder_backup.py
"""


def _generate_slider_render_php(css_framework: str, bem_prefix: str = 'img2html') -> str:
    """Genera el PHP de renderizado del slider según el framework. Usa prefijo BEM."""
    base_class = f"{bem_prefix}-slider"
    wrapper_class = f"{bem_prefix}-slider__wrapper"
    slide_class = f"{bem_prefix}-slider__slide"
    arrow_class = f"{bem_prefix}-slider__arrow"
    dot_class = f"{bem_prefix}-slider__dot"
    
    if css_framework == 'tailwind':
        return f"""<?php
/**
 * Template para renderizar el Slider
 */
$show_slider = $attributes['showSlider'] ?? true;
$full_width = $attributes['fullWidth'] ?? false;
$show_arrows = $attributes['showArrows'] ?? true;
$show_dots = $attributes['showDots'] ?? true;
$autoplay = $attributes['autoplay'] ?? true;
$autoplay_speed = $attributes['autoplaySpeed'] ?? 5000;
$transition_speed = $attributes['transitionSpeed'] ?? 500;
$height = $attributes['height'] ?? '70vh';
$slides = $attributes['slides'] ?? [];

if (!$show_slider || empty($slides)) {{
    return;
}}

$container_class = $full_width ? 'w-full' : 'container mx-auto';
$height_class = $height === 'auto' ? 'h-auto' : ($height === '100vh' ? 'h-screen' : 'h-[70vh]');
?>
<div class="{base_class} <?php echo esc_attr($container_class); ?> <?php echo esc_attr($height_class); ?> relative overflow-hidden" 
     data-autoplay="<?php echo $autoplay ? 'true' : 'false'; ?>"
     data-speed="<?php echo esc_attr($autoplay_speed); ?>"
     data-transition="<?php echo esc_attr($transition_speed); ?>">
    <div class="{wrapper_class} relative w-full h-full">
        <?php foreach ($slides as $index => $slide): ?>
            <?php
            $image_url = $slide['imageUrl'] ?? '';
            $image_webp = $slide['imageWebp'] ?? '';
            $image_thumb = $slide['imageThumb'] ?? '';
            $title = $slide['title'] ?? '';
            $subtitle = $slide['subtitle'] ?? '';
            $button_text = $slide['buttonText'] ?? '';
            $button_url = $slide['buttonUrl'] ?? '';
            $show_button = $slide['showButton'] ?? true;
            $text_position = $slide['textPosition'] ?? 'center';
            $show_overlay = $slide['showOverlay'] ?? true;
            $active = $index === 0 ? 'active' : '';
            
            $text_align = $text_position === 'left' ? 'text-left items-start' : 
                         ($text_position === 'right' ? 'text-right items-end' : 'text-center items-center');
            ?>
            <div class="{slide_class} absolute inset-0 w-full h-full <?php echo esc_attr($active); ?>" data-slide="<?php echo $index; ?>">
                <?php if ($image_url): ?>
                    <picture>
                        <?php if ($image_webp): ?><source srcset="<?php echo esc_url($image_webp); ?>" type="image/webp"><?php endif; ?>
                        <?php if ($image_thumb): ?><source srcset="<?php echo esc_url($image_thumb); ?>" media="(max-width: 640px)"><?php endif; ?>
                        <img src="<?php echo esc_url($image_url); ?>" 
                             alt="<?php echo esc_attr($title); ?>"
                             class="w-full h-full object-cover"
                             loading="lazy">
                    </picture>
                <?php endif; ?>
                
                <?php if ($show_overlay): ?>
                    <div class="absolute inset-0 bg-black bg-opacity-40"></div>
                <?php endif; ?>
                
                <div class="absolute inset-0 flex <?php echo esc_attr($text_align); ?> justify-center p-8 md:p-16">
                    <div class="max-w-2xl">
                        <?php if ($title): ?>
                            <h2 class="text-4xl md:text-6xl font-bold text-white mb-4"><?php echo esc_html($title); ?></h2>
                        <?php endif; ?>
                        
                        <?php if ($subtitle): ?>
                            <p class="text-xl md:text-2xl text-white mb-6"><?php echo esc_html($subtitle); ?></p>
                        <?php endif; ?>
                        
                        <?php if ($show_button && $button_text && $button_url): ?>
                            <a href="<?php echo esc_url($button_url); ?>" 
                               class="inline-block px-8 py-3 bg-white text-gray-900 font-semibold rounded-lg hover:bg-gray-100 transition">
                                <?php echo esc_html($button_text); ?>
                            </a>
                        <?php endif; ?>
                    </div>
                </div>
            </div>
        <?php endforeach; ?>
    </div>
    
    <?php if ($show_arrows && count($slides) > 1): ?>
        <button class="{arrow_class} {arrow_class}--prev absolute left-4 top-1/2 -translate-y-1/2 bg-white bg-opacity-80 hover:bg-opacity-100 rounded-full p-3 z-10 transition">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
            </svg>
        </button>
        <button class="{arrow_class} {arrow_class}--next absolute right-4 top-1/2 -translate-y-1/2 bg-white bg-opacity-80 hover:bg-opacity-100 rounded-full p-3 z-10 transition">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
        </button>
    <?php endif; ?>
    
    <?php if ($show_dots && count($slides) > 1): ?>
        <div class="{base_class}__dots absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2 z-10">
            <?php foreach ($slides as $index => $slide): ?>
                <button class="{dot_class} w-3 h-3 rounded-full bg-white bg-opacity-50 hover:bg-opacity-100 transition <?php echo $index === 0 ? '{dot_class}--active' : ''; ?>" 
                        data-slide="<?php echo $index; ?>"></button>
            <?php endforeach; ?>
        </div>
    <?php endif; ?>
</div>

<script>
(function() {{
    const slider = document.querySelector('.img2html-slider');
    if (!slider) return;
    
    const slides = slider.querySelectorAll('.slide');
    const dots = slider.querySelectorAll('.dot');
    const prevBtn = slider.querySelector('.slider-prev');
    const nextBtn = slider.querySelector('.slider-next');
    const autoplay = slider.dataset.autoplay === 'true';
    const speed = parseInt(slider.dataset.speed) || 5000;
    const transition = parseInt(slider.dataset.transition) || 500;
    
    let currentSlide = 0;
    let autoplayInterval;
    
    function showSlide(index) {{
        slides.forEach((slide, i) => {{
            slide.classList.toggle('active', i === index);
        }});
        dots.forEach((dot, i) => {{
            dot.classList.toggle('active', i === index);
        }});
        currentSlide = index;
    }}
    
    function nextSlide() {{
        const next = (currentSlide + 1) % slides.length;
        showSlide(next);
    }}
    
    function prevSlide() {{
        const prev = (currentSlide - 1 + slides.length) % slides.length;
        showSlide(prev);
    }}
    
    if (prevBtn) prevBtn.addEventListener('click', prevSlide);
    if (nextBtn) nextBtn.addEventListener('click', nextSlide);
    
    dots.forEach((dot, index) => {{
        dot.addEventListener('click', () => showSlide(index));
    }});
    
    if (autoplay && slides.length > 1) {{
        autoplayInterval = setInterval(nextSlide, speed);
        slider.addEventListener('mouseenter', () => clearInterval(autoplayInterval));
        slider.addEventListener('mouseleave', () => {{
            autoplayInterval = setInterval(nextSlide, speed);
        }});
    }}
}})();
</script>
"""
    elif css_framework == 'bootstrap':
        return """<?php
/**
 * Template para renderizar el Slider con Bootstrap
 */
$show_slider = $attributes['showSlider'] ?? true;
$full_width = $attributes['fullWidth'] ?? false;
$show_arrows = $attributes['showArrows'] ?? true;
$show_dots = $attributes['showDots'] ?? true;
$autoplay = $attributes['autoplay'] ?? true;
$autoplay_speed = $attributes['autoplaySpeed'] ?? 5000;
$height = $attributes['height'] ?? '70vh';
$slides = $attributes['slides'] ?? [];

if (!$show_slider || empty($slides)) {
    return;
}

$container_class = $full_width ? 'container-fluid p-0' : 'container';
$height_style = $height === 'auto' ? '' : 'style="height: ' . esc_attr($height) . ';"';
$carousel_id = 'slider-' . uniqid();
?>
<div class="img2html-slider <?php echo esc_attr($container_class); ?>" <?php echo $height_style; ?>>
    <div id="<?php echo esc_attr($carousel_id); ?>" class="carousel slide" data-bs-ride="<?php echo $autoplay ? 'carousel' : 'false'; ?>" data-bs-interval="<?php echo esc_attr($autoplay_speed); ?>">
        <?php if ($show_dots && count($slides) > 1): ?>
            <div class="carousel-indicators">
                <?php foreach ($slides as $index => $slide): ?>
                    <button type="button" data-bs-target="#<?php echo esc_attr($carousel_id); ?>" 
                            data-bs-slide-to="<?php echo $index; ?>" 
                            <?php echo $index === 0 ? 'class="active" aria-current="true"' : ''; ?> 
                            aria-label="Slide <?php echo $index + 1; ?>"></button>
                <?php endforeach; ?>
            </div>
        <?php endif; ?>
        
        <div class="carousel-inner">
            <?php foreach ($slides as $index => $slide): ?>
                <?php
                $image_url = $slide['imageUrl'] ?? '';
                $title = $slide['title'] ?? '';
                $subtitle = $slide['subtitle'] ?? '';
                $button_text = $slide['buttonText'] ?? '';
                $button_url = $slide['buttonUrl'] ?? '';
                $show_button = $slide['showButton'] ?? true;
                $text_position = $slide['textPosition'] ?? 'center';
                $show_overlay = $slide['showOverlay'] ?? true;
                $active = $index === 0 ? 'active' : '';
                
                $text_align = $text_position === 'left' ? 'text-start' : 
                             ($text_position === 'right' ? 'text-end' : 'text-center');
                ?>
                <div class="carousel-item <?php echo esc_attr($active); ?>">
                    <?php if ($image_url): ?>
                        <img src="<?php echo esc_url($image_url); ?>" 
                             class="d-block w-100" 
                             alt="<?php echo esc_attr($title); ?>"
                             style="object-fit: cover; height: <?php echo esc_attr($height); ?>;">
                    <?php endif; ?>
                    
                    <?php if ($show_overlay): ?>
                        <div class="carousel-overlay position-absolute top-0 start-0 w-100 h-100 bg-dark bg-opacity-40"></div>
                    <?php endif; ?>
                    
                    <div class="carousel-caption d-flex flex-column <?php echo esc_attr($text_align); ?> justify-content-center h-100">
                        <div class="container">
                            <?php if ($title): ?>
                                <h2 class="display-4 fw-bold mb-4"><?php echo esc_html($title); ?></h2>
                            <?php endif; ?>
                            
                            <?php if ($subtitle): ?>
                                <p class="lead mb-4"><?php echo esc_html($subtitle); ?></p>
                            <?php endif; ?>
                            
                            <?php if ($show_button && $button_text && $button_url): ?>
                                <a href="<?php echo esc_url($button_url); ?>" 
                                   class="btn btn-light btn-lg">
                                    <?php echo esc_html($button_text); ?>
                                </a>
                            <?php endif; ?>
                        </div>
                    </div>
                </div>
            <?php endforeach; ?>
        </div>
        
        <?php if ($show_arrows && count($slides) > 1): ?>
            <button class="carousel-control-prev" type="button" data-bs-target="#<?php echo esc_attr($carousel_id); ?>" data-bs-slide="prev">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Previous</span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#<?php echo esc_attr($carousel_id); ?>" data-bs-slide="next">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Next</span>
            </button>
        <?php endif; ?>
    </div>
</div>
"""
    else:
        # CSS propio
        return """<?php
/**
 * Template para renderizar el Slider con CSS propio
 */
$show_slider = $attributes['showSlider'] ?? true;
$full_width = $attributes['fullWidth'] ?? false;
$show_arrows = $attributes['showArrows'] ?? true;
$show_dots = $attributes['showDots'] ?? true;
$autoplay = $attributes['autoplay'] ?? true;
$autoplay_speed = $attributes['autoplaySpeed'] ?? 5000;
$height = $attributes['height'] ?? '70vh';
$slides = $attributes['slides'] ?? [];

if (!$show_slider || empty($slides)) {
    return;
}
?>
<div class="img2html-slider" style="height: <?php echo esc_attr($height); ?>;">
    <!-- Slider implementado con CSS propio -->
    <div class="slider-wrapper">
        <?php foreach ($slides as $index => $slide): ?>
            <div class="slide <?php echo $index === 0 ? 'active' : ''; ?>">
                <!-- Contenido del slide -->
            </div>
        <?php endforeach; ?>
    </div>
</div>
"""

def _render_simple_section(css_framework: str, block_name: str, bem_prefix: str = 'img2html') -> str:
    base_class = f"{bem_prefix}-{block_name}"
    if css_framework == 'tailwind':
        return f"""<?php
$layout = $attributes['layout'] ?? 'image-left';
$title = $attributes['title'] ?? '';
$body = $attributes['body'] ?? '';
$image = $attributes['imageUrl'] ?? '';
$image_webp = $attributes['imageWebp'] ?? '';
$image_thumb = $attributes['imageThumb'] ?? '';
$bg = $attributes['bgStyle'] ?? 'light';
$padding = $attributes['padding'] ?? 'md';
$pad = $padding === 'lg' ? 'py-16' : ($padding === 'sm' ? 'py-6' : 'py-10');
$bgClass = $bg === 'dark' ? 'bg-gray-900 text-white' : 'bg-white text-gray-900';
$isImgLeft = $layout !== 'image-right';
?>
<section class="{base_class} <?php echo $bgClass; ?> <?php echo $pad; ?>">
    <div class="container mx-auto grid md:grid-cols-2 gap-10 items-center">
    <?php if ($isImgLeft && $image): ?>
      <div>
        <picture>
          <?php if ($image_webp): ?><source srcset="<?php echo esc_url($image_webp); ?>" type="image/webp"><?php endif; ?>
          <?php if ($image_thumb): ?><source srcset="<?php echo esc_url($image_thumb); ?>" media="(max-width: 640px)"><?php endif; ?>
          <img src="<?php echo esc_url($image); ?>" class="w-full h-auto rounded-lg object-cover" loading="lazy" />
        </picture>
      </div>
    <?php endif; ?>
    <div>
      <?php if ($title): ?><h2 class="text-3xl font-bold mb-4"><?php echo esc_html($title); ?></h2><?php endif; ?>
      <?php if ($body): ?><p class="text-lg leading-relaxed"><?php echo esc_html($body); ?></p><?php endif; ?>
    </div>
    <?php if (!$isImgLeft && $image): ?>
      <div>
        <picture>
          <?php if ($image_webp): ?><source srcset="<?php echo esc_url($image_webp); ?>" type="image/webp"><?php endif; ?>
          <?php if ($image_thumb): ?><source srcset="<?php echo esc_url($image_thumb); ?>" media="(max-width: 640px)"><?php endif; ?>
          <img src="<?php echo esc_url($image); ?>" class="w-full h-auto rounded-lg object-cover" loading="lazy" />
        </picture>
      </div>
    <?php endif; ?>
  </div>
</section>
"""
    else:
        return f"""<?php
$layout = $attributes['layout'] ?? 'image-left';
$title = $attributes['title'] ?? '';
$body = $attributes['body'] ?? '';
$image = $attributes['imageUrl'] ?? '';
$image_webp = $attributes['imageWebp'] ?? '';
$image_thumb = $attributes['imageThumb'] ?? '';
$bg = $attributes['bgStyle'] ?? 'light';
$padding = $attributes['padding'] ?? 'md';
$pad = $padding === 'lg' ? 'py-5' : ($padding === 'sm' ? 'py-2' : 'py-4');
$bgClass = $bg === 'dark' ? 'bg-dark text-white' : 'bg-light text-dark';
$isImgLeft = $layout !== 'image-right';
?>
<section class="{base_class} <?php echo $bgClass; ?> <?php echo $pad; ?>">
      <div class="container">
        <div class="row align-items-center g-4">
      <?php if ($isImgLeft && $image): ?>
        <div class="col-md-6">
          <picture>
            <?php if ($image_webp): ?><source srcset="<?php echo esc_url($image_webp); ?>" type="image/webp"><?php endif; ?>
            <?php if ($image_thumb): ?><source srcset="<?php echo esc_url($image_thumb); ?>" media="(max-width: 640px)"><?php endif; ?>
            <img src="<?php echo esc_url($image); ?>" class="img-fluid rounded" loading="lazy">
          </picture>
        </div>
      <?php endif; ?>
      <div class="col-md-6">
        <?php if ($title): ?><h2 class="fw-bold mb-3"><?php echo esc_html($title); ?></h2><?php endif; ?>
        <?php if ($body): ?><p class="lead"><?php echo esc_html($body); ?></p><?php endif; ?>
      </div>
      <?php if (!$isImgLeft && $image): ?>
        <div class="col-md-6">
          <picture>
            <?php if ($image_webp): ?><source srcset="<?php echo esc_url($image_webp); ?>" type="image/webp"><?php endif; ?>
            <?php if ($image_thumb): ?><source srcset="<?php echo esc_url($image_thumb); ?>" media="(max-width: 640px)"><?php endif; ?>
            <img src="<?php echo esc_url($image); ?>" class="img-fluid rounded" loading="lazy">
          </picture>
        </div>
      <?php endif; ?>
    </div>
  </div>
</section>
"""

def _render_sidebar(css_framework: str, bem_prefix: str = 'img2html') -> str:
    base_class = f"{bem_prefix}-sidebar"
    if css_framework == 'tailwind':
        return f"""<?php
$title = $attributes['title'] ?? 'Sidebar';
$links = $attributes['links'] ?? [];
$showRecent = $attributes['showRecent'] ?? true;
$showCategories = $attributes['showCategories'] ?? true;
$showTags = $attributes['showTags'] ?? true;
$style = $attributes['styleVariant'] ?? 'light';
$padding = $attributes['padding'] ?? 'md';
$border = $attributes['border'] ?? false;
$linkStyle = $attributes['linkStyle'] ?? 'normal';

$bg = $style === 'dark' ? 'bg-gray-900 text-white' : 'bg-white text-gray-900';
$pad = $padding === 'lg' ? 'p-6' : ($padding === 'sm' ? 'p-3' : 'p-4');
$borderClass = $border ? 'border border-gray-200' : '';
$linkClass = $linkStyle === 'underline' ? 'underline' : 'no-underline';
?>
<aside class="{base_class} <?php echo "$bg $pad $borderClass"; ?>">
  <?php if ($title): ?><h3 class="text-xl font-semibold mb-4"><?php echo esc_html($title); ?></h3><?php endif; ?>
  <?php if (!empty($links)): ?>
    <ul class="space-y-2 mb-4">
      <?php foreach ($links as $link): ?>
        <?php $label = $link['label'] ?? ''; $url = $link['url'] ?? '#'; ?>
        <li><a class="text-primary <?php echo $linkClass; ?>" href="<?php echo esc_url($url); ?>"><?php echo esc_html($label); ?></a></li>
      <?php endforeach; ?>
    </ul>
  <?php endif; ?>
  <?php if ($showRecent): ?>
    <div class="mb-4"><h4 class="font-semibold mb-2">Últimos posts</h4><?php echo wp_get_recent_posts( ['numberposts'=>5, 'post_status'=>'publish'], ARRAY_A ) ? wp_get_archives(['type'=>'postbypost','limit'=>5,'echo'=>0]) : ''; ?></div>
  <?php endif; ?>
  <?php if ($showCategories): ?>
    <div class="mb-4"><h4 class="font-semibold mb-2">Categorías</h4><ul class="list-disc list-inside text-sm"><?php wp_list_categories(['title_li'=>'']); ?></ul></div>
  <?php endif; ?>
  <?php if ($showTags): ?>
    <div class="mb-2"><h4 class="font-semibold mb-2">Etiquetas</h4><div class="flex flex-wrap gap-2 text-sm"><?php wp_tag_cloud(['smallest'=>10,'largest'=>12,'unit'=>'px']); ?></div></div>
  <?php endif; ?>
</aside>
"""
    else:
        return f"""<?php
$title = $attributes['title'] ?? 'Sidebar';
$links = $attributes['links'] ?? [];
$showRecent = $attributes['showRecent'] ?? true;
$showCategories = $attributes['showCategories'] ?? true;
$showTags = $attributes['showTags'] ?? true;
$style = $attributes['styleVariant'] ?? 'light';
$padding = $attributes['padding'] ?? 'md';
$border = $attributes['border'] ?? false;
$linkStyle = $attributes['linkStyle'] ?? 'normal';

$bg = $style === 'dark' ? 'bg-dark text-white' : 'bg-light text-dark';
$pad = $padding === 'lg' ? 'p-4' : ($padding === 'sm' ? 'p-2' : 'p-3');
$borderClass = $border ? 'border border-1 border-secondary' : '';
$linkClass = $linkStyle === 'underline' ? 'text-decoration-underline' : 'text-decoration-none';
?>
<aside class="{base_class} <?php echo "$bg $pad $borderClass"; ?>">
  <?php if ($title): ?><h3 class="h5 fw-semibold mb-3"><?php echo esc_html($title); ?></h3><?php endif; ?>
  <?php if (!empty($links)): ?>
    <ul class="list-unstyled mb-3">
      <?php foreach ($links as $link): ?>
        <?php $label = $link['label'] ?? ''; $url = $link['url'] ?? '#'; ?>
        <li class="mb-2"><a class="link-primary <?php echo $linkClass; ?>" href="<?php echo esc_url($url); ?>"><?php echo esc_html($label); ?></a></li>
      <?php endforeach; ?>
    </ul>
  <?php endif; ?>
  <?php if ($showRecent): ?>
    <div class="mb-3"><h4 class="h6 fw-semibold mb-2">Últimos posts</h4><?php echo wp_get_archives(['type'=>'postbypost','limit'=>5,'echo'=>0]); ?></div>
  <?php endif; ?>
  <?php if ($showCategories): ?>
    <div class="mb-3"><h4 class="h6 fw-semibold mb-2">Categorías</h4><ul class="list-unstyled small"><?php wp_list_categories(['title_li'=>'']); ?></ul></div>
  <?php endif; ?>
  <?php if ($showTags): ?>
    <div class="mb-2"><h4 class="h6 fw-semibold mb-2">Etiquetas</h4><div class="d-flex flex-wrap gap-2 small"><?php wp_tag_cloud(['smallest'=>10,'largest'=>12,'unit'=>'px']); ?></div></div>
  <?php endif; ?>
</aside>
"""

def _render_search(css_framework: str, bem_prefix: str = 'img2html') -> str:
    base_class = f"{bem_prefix}-search"
    if css_framework == 'tailwind':
        return f"""<?php
$size = $attributes['size'] ?? 'md';
$rounded = $attributes['rounded'] ?? true;
$buttonInside = $attributes['buttonInside'] ?? true;
$placeholder = $attributes['placeholder'] ?? 'Buscar...';
$showIcon = $attributes['showIcon'] ?? true;

$sizeClass = $size === 'lg' ? 'text-lg py-3 px-4' : ($size === 'sm' ? 'text-sm py-2 px-3' : 'text-base py-2.5 px-3');
$roundedClass = $rounded ? 'rounded-full' : 'rounded-md';
?>
<div class="{base_class} w-full relative">
  <?php if ($buttonInside): ?>
    <div class="relative">
      <form role="search" method="get" class="w-full">
        <input class="w-full bg-white text-gray-900 <?php echo "$sizeClass $roundedClass"; ?> pr-24 border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary" 
               type="search" placeholder="<?php echo esc_attr($placeholder); ?>" value="<?php echo get_search_query(); ?>" name="s">
        <button class="absolute right-2 top-1/2 -translate-y-1/2 bg-primary text-white px-4 py-2 rounded-md" type="submit">
          <?php echo $showIcon ? '🔍' : __('Buscar', 'img2html'); ?>
        </button>
      </form>
    </div>
  <?php else: ?>
    <form role="search" method="get" class="flex w-full gap-2">
      <input class="flex-1 bg-white text-gray-900 <?php echo "$sizeClass $roundedClass"; ?> border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary" 
             type="search" placeholder="<?php echo esc_attr($placeholder); ?>" value="<?php echo get_search_query(); ?>" name="s">
      <button class="bg-primary text-white px-4 py-2 rounded-md" type="submit"><?php echo $showIcon ? '🔍' : __('Buscar', 'img2html'); ?></button>
    </form>
  <?php endif; ?>
</div>
"""
    else:
        return f"""<?php
$size = $attributes['size'] ?? 'md';
$rounded = $attributes['rounded'] ?? true;
$buttonInside = $attributes['buttonInside'] ?? true;
$placeholder = $attributes['placeholder'] ?? 'Buscar...';
$showIcon = $attributes['showIcon'] ?? true;

$sizeClass = $size === 'lg' ? 'form-control-lg' : ($size === 'sm' ? 'form-control-sm' : '');
$roundedClass = $rounded ? 'rounded-pill' : '';
?>
<div class="{base_class} w-100">
  <?php if ($buttonInside): ?>
    <form role="search" method="get" class="input-group">
      <input type="search" class="form-control <?php echo $sizeClass; ?> <?php echo $roundedClass; ?>" placeholder="<?php echo esc_attr($placeholder); ?>" value="<?php echo get_search_query(); ?>" name="s">
      <button class="btn btn-primary" type="submit"><?php echo $showIcon ? '🔍' : __('Buscar', 'img2html'); ?></button>
    </form>
  <?php else: ?>
    <form role="search" method="get" class="d-flex gap-2">
      <input type="search" class="form-control <?php echo $sizeClass; ?> <?php echo $roundedClass; ?>" placeholder="<?php echo esc_attr($placeholder); ?>" value="<?php echo get_search_query(); ?>" name="s">
      <button class="btn btn-primary" type="submit"><?php echo $showIcon ? '🔍' : __('Buscar', 'img2html'); ?></button>
    </form>
  <?php endif; ?>
</div>
"""

def _render_pagination(css_framework: str, bem_prefix: str = 'img2html') -> str:
    base_class = f"{bem_prefix}-pagination"
    return f"""<?php
$mode = $attributes['mode'] ?? 'numbers';
$align = $attributes['align'] ?? 'center';
$size = $attributes['size'] ?? 'md';
$gap = $attributes['gap'] ?? 8;
$showPageCount = $attributes['showPageCount'] ?? false;

if (!have_posts()) {{ return; }}

$alignClass = $align === 'left' ? 'justify-content-start' : ($align === 'right' ? 'justify-content-end' : 'justify-content-center');
$sizeClass = $size === 'lg' ? 'pagination-lg' : ($size === 'sm' ? 'pagination-sm' : '');

$links = paginate_links([
    'type'      => 'array',
    'prev_text' => '«',
    'next_text' => '»',
]);

if (!$links) {{ return; }}
?>
<nav class="{base_class} d-flex <?php echo esc_attr($alignClass); ?>">
  <?php if ($mode === 'minimal'): ?>
    <div class="d-flex align-items-center gap-2">
      <?php echo get_previous_posts_link('←'); ?>
      <?php echo get_next_posts_link('→'); ?>
    </div>
  <?php elseif ($mode === 'prev-next'): ?>
    <div class="d-flex align-items-center gap-2">
      <?php echo get_previous_posts_link('Anterior'); ?>
      <?php echo get_next_posts_link('Siguiente'); ?>
    </div>
  <?php else: ?>
    <ul class="pagination <?php echo esc_attr($sizeClass); ?>" style="gap: <?php echo intval($gap); ?>px;">
      <?php foreach ($links as $link): ?>
        <li class="page-item <?php echo strpos($link, 'current') !== false ? 'active' : ''; ?>">
          <?php echo str_replace('page-numbers', 'page-link', $link); ?>
        </li>
      <?php endforeach; ?>
    </ul>
  <?php endif; ?>
  <?php if ($showPageCount): ?>
    <span class="ms-2 small text-muted"><?php global $wp_query; echo sprintf('%d %s', $wp_query->max_num_pages, __('páginas', 'img2html')); ?></span>
  <?php endif; ?>
</nav>
"""

def _render_header(css_framework: str, bem_prefix: str = 'img2html') -> str:
    base = f"{bem_prefix}-header"
    if css_framework == 'tailwind':
        return f"""<?php
$sticky = $attributes['sticky'] ?? false;
$transparent = $attributes['transparent'] ?? false;
$ctaShow = $attributes['ctaShow'] ?? true;
$ctaText = $attributes['ctaText'] ?? 'Contáctanos';
$ctaUrl = $attributes['ctaUrl'] ?? '#';

$stickyClass = $sticky ? 'sticky top-0' : '';
$bgClass = $transparent ? 'bg-transparent' : 'bg-white shadow';
?>
<header class="{base} <?php echo "$stickyClass $bgClass"; ?> py-4">
  <div class="container mx-auto flex items-center justify-between gap-4">
    <!-- Logo editable como bloque core/site-logo -->
    <!-- wp:site-logo {"width":48} /-->
    <!-- wp:navigation {"layout":{"type":"flex","justifyContent":"center","orientation":"horizontal"}} /-->
    <?php if ($ctaShow): ?>
      <a href="<?php echo esc_url($ctaUrl); ?>" class="px-4 py-2 bg-primary text-white rounded-lg font-semibold"><?php echo esc_html($ctaText); ?></a>
    <?php endif; ?>
  </div>
</header>
"""
    else:
        return f"""<?php
$sticky = $attributes['sticky'] ?? false;
$transparent = $attributes['transparent'] ?? false;
$ctaShow = $attributes['ctaShow'] ?? true;
$ctaText = $attributes['ctaText'] ?? 'Contáctanos';
$ctaUrl = $attributes['ctaUrl'] ?? '#';
$showSocial = $attributes['showSocial'] ?? false;

$stickyClass = $sticky ? 'sticky-top' : '';
$bgClass = $transparent ? 'bg-transparent' : 'bg-white shadow-sm';
?>
<header class="{base} <?php echo "$stickyClass $bgClass"; ?> py-3">
  <div class="container d-flex align-items-center justify-content-between gap-3">
    <!-- wp:site-logo {"width":48} /-->
    <!-- wp:navigation {"layout":{"type":"flex","justifyContent":"center","orientation":"horizontal"}} /-->
    <div class="d-flex align-items-center gap-2">
      <?php if ($showSocial): ?>
        <!-- wp:social-links /-->
      <?php endif; ?>
      <?php if ($ctaShow): ?>
        <a href="<?php echo esc_url($ctaUrl); ?>" class="btn btn-primary"><?php echo esc_html($ctaText); ?></a>
      <?php endif; ?>
    </div>
  </div>
</header>
"""

def _render_footer(css_framework: str, bem_prefix: str = 'img2html') -> str:
    base = f"{bem_prefix}-footer"
    if css_framework == 'tailwind':
        return f"""<?php
$columns = max(1, min(4, intval($attributes['columns'] ?? 3)));
$bg = $attributes['bg'] ?? 'dark';
$legal = $attributes['legal'] ?? '© 2025. Todos los derechos reservados.';
$links = $attributes['links'] ?? [];
$showSocial = $attributes['showSocial'] ?? true;

$bgClass = $bg === 'dark' ? 'bg-gray-900 text-white' : 'bg-gray-100 text-gray-900';
?>
<footer class="{base} <?php echo $bgClass; ?> py-10">
  <div class="container mx-auto grid gap-8" style="grid-template-columns: repeat(<?php echo $columns; ?>, minmax(0, 1fr));">
    <!-- Columna 1: Logo + legal -->
    <div>
      <!-- wp:site-logo {"width":48} /-->
      <p class="mt-4 text-sm"><?php echo esc_html($legal); ?></p>
    </div>
    <!-- Columna de enlaces -->
    <?php if (!empty($links)): ?>
      <div>
        <h4 class="font-semibold mb-3">Enlaces</h4>
        <ul class="space-y-2 text-sm">
          <?php foreach ($links as $link): ?>
            <?php $label = $link['label'] ?? ''; $url = $link['url'] ?? '#'; ?>
            <li><a class="hover:underline" href="<?php echo esc_url($url); ?>"><?php echo esc_html($label); ?></a></li>
          <?php endforeach; ?>
        </ul>
      </div>
    <?php endif; ?>
    <?php if ($showSocial): ?>
      <div>
        <h4 class="font-semibold mb-3">Social</h4>
        <!-- wp:social-links /-->
      </div>
    <?php endif; ?>
  </div>
</footer>
"""
    else:
        return f"""<?php
$columns = max(1, min(4, intval($attributes['columns'] ?? 3)));
$bg = $attributes['bg'] ?? 'dark';
$legal = $attributes['legal'] ?? '© 2025. Todos los derechos reservados.';
$links = $attributes['links'] ?? [];
$showSocial = $attributes['showSocial'] ?? true;

$bgClass = $bg === 'dark' ? 'bg-dark text-white' : 'bg-light text-dark';
?>
<footer class="{base} <?php echo $bgClass; ?> py-5">
  <div class="container">
    <div class="row g-4 row-cols-<?php echo $columns; ?>">
      <div class="col">
        <!-- wp:site-logo {"width":48} /-->
        <p class="mt-3 small mb-0"><?php echo esc_html($legal); ?></p>
      </div>
      <?php if (!empty($links)): ?>
        <div class="col">
          <h4 class="h6 fw-semibold mb-3">Enlaces</h4>
          <ul class="list-unstyled small">
            <?php foreach ($links as $link): ?>
              <?php $label = $link['label'] ?? ''; $url = $link['url'] ?? '#'; ?>
              <li class="mb-2"><a href="<?php echo esc_url($url); ?>" class="link-light text-decoration-none"><?php echo esc_html($label); ?></a></li>
            <?php endforeach; ?>
          </ul>
        </div>
      <?php endif; ?>
      <?php if ($showSocial): ?>
        <div class="col">
          <h4 class="h6 fw-semibold mb-3">Social</h4>
          <!-- wp:social-links /-->
        </div>
      <?php endif; ?>
    </div>
  </div>
</footer>
"""

def _render_form(css_framework: str, bem_prefix: str = 'img2html') -> str:
    base_class = f"{bem_prefix}-form"
    if css_framework == 'tailwind':
        return f"""<?php
$showPhone = $attributes['showPhone'] ?? true;
$submitText = $attributes['submitText'] ?? 'Enviar';
$successMessage = $attributes['successMessage'] ?? 'Mensaje enviado';
$errorMessage = $attributes['errorMessage'] ?? 'Ocurrió un error';
$endpoint = $attributes['endpoint'] ?? '/wp-json/img2html/v1/contact';
?>
<form class="{base_class} space-y-4" data-endpoint="<?php echo esc_attr($endpoint); ?>">
  <div class="grid md:grid-cols-2 gap-4">
    <input class="w-full border border-gray-200 rounded-lg px-4 py-3" type="text" name="name" placeholder="Nombre" required>
    <input class="w-full border border-gray-200 rounded-lg px-4 py-3" type="email" name="email" placeholder="Email" required>
    <?php if ($showPhone): ?>
    <input class="w-full border border-gray-200 rounded-lg px-4 py-3" type="tel" name="phone" placeholder="Teléfono">
    <?php endif; ?>
  </div>
  <textarea class="w-full border border-gray-200 rounded-lg px-4 py-3" name="message" rows="4" placeholder="Mensaje" required></textarea>
  <button class="px-6 py-3 bg-primary text-white rounded-lg font-semibold" type="submit"><?php echo esc_html($submitText); ?></button>
  <div class="form-feedback text-sm text-green-600 hidden"><?php echo esc_html($successMessage); ?></div>
  <div class="form-error text-sm text-red-600 hidden"><?php echo esc_html($errorMessage); ?></div>
</form>
<script>
(function(){{
  const form = document.currentScript.previousElementSibling;
  if(!form) return;
  form.addEventListener('submit', async (e) => {{
    e.preventDefault();
    const fd = new FormData(form);
    const endpoint = form.dataset.endpoint || '/wp-json/img2html/v1/contact';
    try {{
      await fetch(endpoint, {{ method: 'POST', body: fd }});
      form.querySelector('.form-feedback').classList.remove('hidden');
      form.querySelector('.form-error').classList.add('hidden');
      form.reset();
    }} catch(err) {{
      form.querySelector('.form-error').classList.remove('hidden');
    }}
  }});
}})();
</script>
"""
    else:
        return f"""<?php
$showPhone = $attributes['showPhone'] ?? true;
$submitText = $attributes['submitText'] ?? 'Enviar';
$successMessage = $attributes['successMessage'] ?? 'Mensaje enviado';
$errorMessage = $attributes['errorMessage'] ?? 'Ocurrió un error';
$endpoint = $attributes['endpoint'] ?? '/wp-json/img2html/v1/contact';
?>
<form class="{base_class} row g-3" data-endpoint="<?php echo esc_attr($endpoint); ?>">
  <div class="col-md-6">
    <input class="form-control" type="text" name="name" placeholder="Nombre" required>
  </div>
  <div class="col-md-6">
    <input class="form-control" type="email" name="email" placeholder="Email" required>
  </div>
  <?php if ($showPhone): ?>
  <div class="col-12">
    <input class="form-control" type="tel" name="phone" placeholder="Teléfono">
  </div>
  <?php endif; ?>
  <div class="col-12">
    <textarea class="form-control" name="message" rows="4" placeholder="Mensaje" required></textarea>
  </div>
  <div class="col-12">
    <button class="btn btn-primary" type="submit"><?php echo esc_html($submitText); ?></button>
  </div>
  <div class="form-feedback small text-success d-none"><?php echo esc_html($successMessage); ?></div>
  <div class="form-error small text-danger d-none"><?php echo esc_html($errorMessage); ?></div>
</form>
<script>
(function(){{
  const form = document.currentScript.previousElementSibling;
  if(!form) return;
  form.addEventListener('submit', async (e) => {{
    e.preventDefault();
    const fd = new FormData(form);
    const endpoint = form.dataset.endpoint || '/wp-json/img2html/v1/contact';
    try {{
      await fetch(endpoint, {{ method: 'POST', body: fd }});
      form.querySelector('.form-feedback').classList.remove('d-none');
      form.querySelector('.form-error').classList.add('d-none');
      form.reset();
    }} catch(err) {{
      form.querySelector('.form-error').classList.remove('d-none');
    }}
  }});
}})();
</script>
"""

def _render_menu(css_framework: str, bem_prefix: str = 'img2html') -> str:
    base_class = f"{bem_prefix}-menu"
    if css_framework == 'tailwind':
        return f"""<?php
$sticky = $attributes['sticky'] ?? false;
$transparent = $attributes['transparent'] ?? false;
$ctaShow = $attributes['ctaShow'] ?? true;
$ctaText = $attributes['ctaText'] ?? 'Contáctanos';
$ctaUrl = $attributes['ctaUrl'] ?? '#';
$showSocial = $attributes['showSocial'] ?? false;

$stickyClass = $sticky ? 'sticky top-0' : '';
$bgClass = $transparent ? 'bg-transparent' : 'bg-white shadow';
?>
<nav class="{base_class} <?php echo "$stickyClass $bgClass"; ?> py-4">
  <div class="container mx-auto flex items-center justify-between gap-4">
    <!-- wp:site-logo {"width":40} /-->
    <button class="menu-toggle md:hidden w-10 h-10 border border-gray-200 rounded-lg flex items-center justify-center" aria-label="Menu">
      <span class="block w-5 h-0.5 bg-gray-800 mb-1"></span>
      <span class="block w-5 h-0.5 bg-gray-800 mb-1"></span>
      <span class="block w-5 h-0.5 bg-gray-800"></span>
    </button>
    <div class="flex-1 flex items-center justify-end gap-4">
      <div class="navigation-wrapper hidden md:flex md:items-center md:gap-6">
        <!-- wp:navigation {"layout":{"type":"flex","orientation":"horizontal","justifyContent":"center"}} /-->
      </div>
      <?php if ($showSocial): ?>
        <div class="hidden md:flex">
          <!-- wp:social-links /-->
        </div>
      <?php endif; ?>
      <?php if ($ctaShow): ?>
        <a href="<?php echo esc_url($ctaUrl); ?>" class="hidden md:inline-flex px-4 py-2 bg-primary text-white rounded-lg font-semibold"><?php echo esc_html($ctaText); ?></a>
      <?php endif; ?>
    </div>
  </div>
  <div class="mobile-panel fixed inset-0 bg-white z-40 hidden">
    <div class="p-4 flex justify-between items-center border-b border-gray-200">
      <!-- wp:site-logo {"width":36} /-->
      <button class="menu-close w-10 h-10 border border-gray-200 rounded-lg flex items-center justify-center" aria-label="Cerrar">
        ✕
      </button>
    </div>
    <div class="p-4 space-y-4">
      <!-- wp:navigation {"layout":{"type":"flex","orientation":"vertical"}} /-->
      <?php if ($ctaShow): ?>
        <a href="<?php echo esc_url($ctaUrl); ?>" class="block w-full text-center px-4 py-3 bg-primary text-white rounded-lg font-semibold"><?php echo esc_html($ctaText); ?></a>
      <?php endif; ?>
      <?php if ($showSocial): ?>
        <div>
          <!-- wp:social-links /-->
        </div>
      <?php endif; ?>
    </div>
  </div>
</nav>
<script>
(function(){{
  const nav = document.currentScript.previousElementSibling;
  if(!nav) return;
  const toggle = nav.querySelector('.menu-toggle');
  const panel = nav.querySelector('.mobile-panel');
  const closeBtn = nav.querySelector('.menu-close');
  const desktopNav = nav.querySelector('.wp-block-navigation');
  if(toggle && panel){{
    toggle.addEventListener('click', () => panel.classList.remove('hidden'));
  }}
  if(closeBtn && panel){{
    closeBtn.addEventListener('click', () => panel.classList.add('hidden'));
  }}

  /* Dropdown desktop (hover) para items con submenú */
  if (desktopNav) {{
    desktopNav.querySelectorAll('li.has-child').forEach((item) => {{
      item.classList.add('relative');
      const submenu = item.querySelector('ul');
      if (!submenu) return;
      submenu.classList.add('absolute','hidden','bg-white','shadow','rounded','mt-2','min-w-[200px]','z-50','p-2');
      item.addEventListener('mouseenter', () => submenu.classList.remove('hidden'));
      item.addEventListener('mouseleave', () => submenu.classList.add('hidden'));
    }});
  }}
}})();
</script>
"""
    else:
        return f"""<?php
$sticky = $attributes['sticky'] ?? false;
$transparent = $attributes['transparent'] ?? false;
$ctaShow = $attributes['ctaShow'] ?? true;
$ctaText = $attributes['ctaText'] ?? 'Contáctanos';
$ctaUrl = $attributes['ctaUrl'] ?? '#';
$showSocial = $attributes['showSocial'] ?? false;

$stickyClass = $sticky ? 'sticky-top' : '';
$bgClass = $transparent ? 'bg-transparent' : 'bg-white shadow-sm';
?>
<nav class="{base_class} navbar navbar-expand-lg <?php echo "$stickyClass $bgClass"; ?>">
  <div class="container">
    <!-- wp:site-logo {"width":40} /-->
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#img2htmlNav" aria-controls="img2htmlNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="img2htmlNav">
      <!-- wp:navigation {"layout":{"type":"flex","orientation":"horizontal","justifyContent":"center"}} /-->
      <div class="ms-auto d-flex align-items-center gap-2">
        <?php if ($showSocial): ?>
          <!-- wp:social-links /-->
        <?php endif; ?>
        <?php if ($ctaShow): ?>
          <a href="<?php echo esc_url($ctaUrl); ?>" class="btn btn-primary"><?php echo esc_html($ctaText); ?></a>
        <?php endif; ?>
      </div>
    </div>
  </div>
</nav>
<script>
(function(){{
  /* Dropdown hover para desktop en Bootstrap */
  const nav = document.currentScript.previousElementSibling;
  if(!nav) return;
  const dropdowns = nav.querySelectorAll('.menu-item-has-children, .has-child');
  dropdowns.forEach((item) => {{
    const submenu = item.querySelector('ul');
    if(!submenu) return;
    item.classList.add('position-relative');
    submenu.classList.add('dropdown-menu','show');
    submenu.style.display = 'none';
    item.addEventListener('mouseenter', () => {{ submenu.style.display = 'block'; }});
    item.addEventListener('mouseleave', () => {{ submenu.style.display = 'none'; }});
  }});
}})();
</script>
"""

def _render_gallery(css_framework: str, bem_prefix: str = 'img2html') -> str:
    base = f"{bem_prefix}-gallery"
    if css_framework == 'tailwind':
        return f"""<?php
$images = $attributes['images'] ?? [];
$cols = max(1, min(6, intval($attributes['columns'] ?? 3)));
$gap = intval($attributes['gap'] ?? 12);
$lightbox = !empty($attributes['lightbox']);
$ratios = ($attributes['layoutRows'][0]['ratios_percent'] ?? []) ?: [];
$grid_style = '';
if ($ratios) {{
  $parts = [];
  foreach ($ratios as $r) {{
    if ($r) {{ $parts[] = "minmax(0, {{$r}}%)"; }}
  }}
  if (!empty($parts)) {{
    $grid_style = 'style="grid-template-columns:' . implode(' ', $parts) . ';"';
  }}
}}
if (!$images) return;
?>
<div class="{base}">
  <div class="grid" style="grid-template-columns: repeat(<?php echo $cols; ?>, minmax(0, 1fr)); gap: <?php echo $gap; ?>px;" <?php echo $grid_style; ?>>
    <?php foreach ($images as $img): 
      $src = $img['url'] ?? ''; 
      $webp = $img['webp'] ?? ''; 
      $thumb = $img['thumb'] ?? '';
    ?>
      <a href="<?php echo esc_url($src); ?>" <?php if(!$lightbox): ?>target="_blank"<?php endif; ?> class="block">
        <picture>
          <?php if ($webp): ?><source srcset="<?php echo esc_url($webp); ?>" type="image/webp"><?php endif; ?>
          <?php if ($thumb): ?><source srcset="<?php echo esc_url($thumb); ?>" media="(max-width: 640px)"><?php endif; ?>
          <img src="<?php echo esc_url($src); ?>" class="w-full h-auto rounded object-cover" loading="lazy" />
        </picture>
      </a>
    <?php endforeach; ?>
  </div>
</div>
"""
    else:
        return f"""<?php
$images = $attributes['images'] ?? [];
$cols = max(1, min(6, intval($attributes['columns'] ?? 3)));
$gap = intval($attributes['gap'] ?? 12);
$lightbox = !empty($attributes['lightbox']);
$ratios = ($attributes['layoutRows'][0]['ratios_percent'] ?? []) ?: [];
if (!$images) return;
?>
<div class="{base}">
  <div class="row g-<?php echo max(0, min(5, intval($gap/4))); ?>">
    <?php foreach ($images as $img): 
      $src = $img['url'] ?? ''; 
      $webp = $img['webp'] ?? ''; 
      $thumb = $img['thumb'] ?? '';
      $w = 12 / max(1,$cols);
      if (!empty($ratios)) {{
        $idx = array_search($img, $images, true);
        if ($idx !== false && isset($ratios[$idx])) {{
          $calc = intval(round(($ratios[$idx]/100.0)*12));
          if ($calc > 0) {{ $w = max(1, min(12, $calc)); }}
        }}
      }}
    ?>
      <div class="col-<?php echo intval($w); ?>">
        <a href="<?php echo esc_url($src); ?>" <?php if(!$lightbox): ?>target="_blank"<?php endif; ?> class="d-block mb-3">
          <picture>
            <?php if ($webp): ?><source srcset="<?php echo esc_url($webp); ?>" type="image/webp"><?php endif; ?>
            <?php if ($thumb): ?><source srcset="<?php echo esc_url($thumb); ?>" media="(max-width: 640px)"><?php endif; ?>
            <img src="<?php echo esc_url($src); ?>" class="img-fluid rounded" loading="lazy">
          </picture>
        </a>
      </div>
    <?php endforeach; ?>
  </div>
</div>
"""

def _render_section(css_framework: str, bem_prefix: str = 'img2html') -> str:
    base_class = f"{bem_prefix}-section"
    if css_framework == 'tailwind':
        return f"""<?php
$variant = $attributes['variant'] ?? 'default';
$title = $attributes['title'] ?? '';
$content = $attributes['content'] ?? '';
$cols = max(1, min(3, intval($attributes['columns'] ?? 2)));
$rows = $attributes['layoutRows'] ?? [];
if ($rows && is_array($rows) && isset($rows[0]['columns'])) {{
  $cols = max(1, min(3, count($rows[0]['columns'])));
}}
$ratios = ($rows && isset($rows[0]['ratios_percent']) && is_array($rows[0]['ratios_percent'])) ? $rows[0]['ratios_percent'] : [];
$image = $attributes['imageUrl'] ?? '';
$image_webp = $attributes['imageWebp'] ?? '';
$image_thumb = $attributes['imageThumb'] ?? '';
$grid = $cols === 1 ? 'grid-cols-1' : ($cols === 3 ? 'md:grid-cols-3' : 'md:grid-cols-2');
$grid_style = '';
if ($ratios) {{
  $parts = [];
  foreach ($ratios as $r) {{
    if ($r) {{ $parts[] = "minmax(0, {{$r}}%)"; }}
  }}
  if (!empty($parts)) {{
    $grid_style = 'style="grid-template-columns:' . implode(' ', $parts) . ';"';
  }}
}}
?>
<section class="{base_class} py-12">
  <div class="container mx-auto grid <?php echo $grid; ?> gap-8 items-center" <?php echo $grid_style; ?>>
    <?php if ($image): ?>
      <div>
        <picture>
          <?php if ($image_webp): ?><source srcset="<?php echo esc_url($image_webp); ?>" type="image/webp"><?php endif; ?>
          <?php if ($image_thumb): ?><source srcset="<?php echo esc_url($image_thumb); ?>" media="(max-width: 640px)"><?php endif; ?>
          <img src="<?php echo esc_url($image); ?>" class="w-full h-auto rounded-lg object-cover" loading="lazy" />
        </picture>
      </div>
    <?php endif; ?>
    <div class="prose max-w-none">
      <?php if ($title): ?><h2 class="text-3xl font-bold mb-4"><?php echo esc_html($title); ?></h2><?php endif; ?>
      <?php if ($content): ?><div><?php echo wp_kses_post($content); ?></div><?php endif; ?>
    </div>
  </div>
</section>
"""
    else:
        return f"""<?php
$variant = $attributes['variant'] ?? 'default';
$title = $attributes['title'] ?? '';
$content = $attributes['content'] ?? '';
$cols = max(1, min(3, intval($attributes['columns'] ?? 2)));
$rows = $attributes['layoutRows'] ?? [];
if ($rows && is_array($rows) && isset($rows[0]['columns'])) {{
  $cols = max(1, min(3, count($rows[0]['columns'])));
}}
$ratios = ($rows && isset($rows[0]['ratios_percent']) && is_array($rows[0]['ratios_percent'])) ? $rows[0]['ratios_percent'] : [];
$image = $attributes['imageUrl'] ?? '';
$image_webp = $attributes['imageWebp'] ?? '';
$image_thumb = $attributes['imageThumb'] ?? '';
$col_class = $cols === 1 ? 'col-12' : ($cols === 3 ? 'col-md-4' : 'col-md-6');
?>
<section class="{base_class} py-5">
  <div class="container">
    <div class="row g-4 align-items-center">
      <?php if ($image): ?>
        <div class="<?php echo esc_attr($col_class); ?>">
          <picture>
            <?php if ($image_webp): ?><source srcset="<?php echo esc_url($image_webp); ?>" type="image/webp"><?php endif; ?>
            <?php if ($image_thumb): ?><source srcset="<?php echo esc_url($image_thumb); ?>" media="(max-width: 640px)"><?php endif; ?>
            <img src="<?php echo esc_url($image); ?>" class="img-fluid rounded" loading="lazy">
          </picture>
        </div>
      <?php endif; ?>
      <?php 
        $col_classes = [];
        if ($ratios) {{
          foreach ($ratios as $r) {{
            $width = max(1, min(12, intval(round(($r/100.0)*12))));
            $col_classes[] = 'col-md-' . $width;
          }}
        }}
        $col_class_left = !empty($col_classes) ? $col_classes[0] : $col_class;
      ?>
      <div class="<?php echo esc_attr($col_class_left); ?>">
        <?php if ($title): ?><h2 class="fw-bold mb-3"><?php echo esc_html($title); ?></h2><?php endif; ?>
        <?php if ($content): ?><div><?php echo wp_kses_post($content); ?></div><?php endif; ?>
      </div>
    </div>
  </div>
</section>
"""

def _render_cards(css_framework: str, bem_prefix: str = 'img2html') -> str:
    base = f"{bem_prefix}-cards"
    if css_framework == 'tailwind':
        return f"""<?php
$cards = $attributes['cards'] ?? [];
$cols = max(1, min(4, intval($attributes['columns'] ?? 3)));
if (isset($attributes['layoutRows']) && is_array($attributes['layoutRows']) && !empty($attributes['layoutRows'])) {{
  /* si el plan trajo layout, usar el primer rows para columnas */
  $first = $attributes['layoutRows'][0];
  if (isset($first['columns']) && is_array($first['columns'])) {{
    $cols = max(1, min(4, count($first['columns'])));
  }}
}}
$ratios = ($attributes['layoutRows'][0]['ratios_percent'] ?? []) ?: [];
$grid_style = '';
if ($ratios) {{
  $parts = [];
  foreach ($ratios as $r) {{
    if ($r) {{ $parts[] = "minmax(0, {{$r}}%)"; }}
  }}
  if (!empty($parts)) {{
    $grid_style = 'style="grid-template-columns:' . implode(' ', $parts) . ';"';
  }}
}}
$gap = intval($attributes['gap'] ?? 16);
if (!$cards) return;
?>
<section class="{base} py-10">
  <div class="container mx-auto grid gap-<?php echo max(2, intval($gap/4)); ?> md:grid-cols-<?php echo $cols; ?>" <?php echo $grid_style; ?>>
    <?php foreach ($cards as $card): 
      $title = $card['title'] ?? '';
      $text = $card['text'] ?? '';
      $img = $card['imageUrl'] ?? '';
      $webp = $card['imageWebp'] ?? '';
      $thumb = $card['imageThumb'] ?? '';
      $btn = $card['buttonText'] ?? '';
      $url = $card['buttonUrl'] ?? '#';
    ?>
      <div class="bg-white rounded-xl shadow-sm p-6 flex flex-col gap-3">
        <?php if ($img): ?>
          <picture>
            <?php if ($webp): ?><source srcset="<?php echo esc_url($webp); ?>" type="image/webp"><?php endif; ?>
            <?php if ($thumb): ?><source srcset="<?php echo esc_url($thumb); ?>" media="(max-width: 640px)"><?php endif; ?>
            <img src="<?php echo esc_url($img); ?>" class="w-full h-48 object-cover rounded-lg" loading="lazy">
          </picture>
        <?php endif; ?>
        <?php if ($title): ?><h3 class="text-xl font-semibold"><?php echo esc_html($title); ?></h3><?php endif; ?>
        <?php if ($text): ?><p class="text-gray-600"><?php echo esc_html($text); ?></p><?php endif; ?>
        <?php if ($btn): ?><a href="<?php echo esc_url($url); ?>" class="mt-auto inline-flex px-4 py-2 bg-primary text-white rounded-lg font-semibold"><?php echo esc_html($btn); ?></a><?php endif; ?>
      </div>
    <?php endforeach; ?>
  </div>
</section>
"""
    else:
        return f"""<?php
$cards = $attributes['cards'] ?? [];
$cols = max(1, min(4, intval($attributes['columns'] ?? 3)));
if (isset($attributes['layoutRows']) && is_array($attributes['layoutRows']) && !empty($attributes['layoutRows'])) {{
  $first = $attributes['layoutRows'][0];
  if (isset($first['columns']) && is_array($first['columns'])) {{
    $cols = max(1, min(4, count($first['columns'])));
  }}
}}
$ratios = ($attributes['layoutRows'][0]['ratios_percent'] ?? []) ?: [];
$gap = intval($attributes['gap'] ?? 16);
if (!$cards) return;
?>
<section class="{base} py-4">
  <div class="container">
    <div class="row g-<?php echo max(0, min(5, intval($gap/4))); ?>">
      <?php foreach ($cards as $card): 
        $title = $card['title'] ?? '';
        $text = $card['text'] ?? '';
        $img = $card['imageUrl'] ?? '';
        $webp = $card['imageWebp'] ?? '';
        $thumb = $card['imageThumb'] ?? '';
        $btn = $card['buttonText'] ?? '';
        $url = $card['buttonUrl'] ?? '#';
        $w = 12 / max(1,$cols);
        if (!empty($ratios)) {{
          $idx = array_search($card, $cards, true);
          if ($idx !== false && isset($ratios[$idx])) {{
            $calc = intval(round(($ratios[$idx]/100.0)*12));
            if ($calc > 0) {{ $w = max(1, min(12, $calc)); }}
          }}
        }}
      ?>
        <div class="col-<?php echo intval($w); ?>">
          <div class="card h-100 shadow-sm">
            <?php if ($img): ?>
              <picture>
                <?php if ($webp): ?><source srcset="<?php echo esc_url($webp); ?>" type="image/webp"><?php endif; ?>
                <?php if ($thumb): ?><source srcset="<?php echo esc_url($thumb); ?>" media="(max-width: 640px)"><?php endif; ?>
                <img src="<?php echo esc_url($img); ?>" class="card-img-top" loading="lazy">
              </picture>
            <?php endif; ?>
            <div class="card-body d-flex flex-column gap-2">
              <?php if ($title): ?><h5 class="card-title mb-2"><?php echo esc_html($title); ?></h5><?php endif; ?>
              <?php if ($text): ?><p class="card-text text-muted"><?php echo esc_html($text); ?></p><?php endif; ?>
              <?php if ($btn): ?><a href="<?php echo esc_url($url); ?>" class="btn btn-primary mt-auto"><?php echo esc_html($btn); ?></a><?php endif; ?>
            </div>
          </div>
        </div>
      <?php endforeach; ?>
    </div>
  </div>
</section>
"""

def _render_hero(css_framework: str, bem_prefix: str = 'img2html') -> str:
    base_class = f"{bem_prefix}-hero"
    if css_framework == 'tailwind':
        return f"""<?php
$title = $attributes['title'] ?? '';
$subtitle = $attributes['subtitle'] ?? '';
$button_text = $attributes['buttonText'] ?? '';
$button_url = $attributes['buttonUrl'] ?? '#';
$show_button = $attributes['showButton'] ?? true;
$show_overlay = $attributes['showOverlay'] ?? true;
$height = $attributes['height'] ?? '70vh';
$align = $attributes['align'] ?? 'center';
$image = $attributes['imageUrl'] ?? '';
$image_webp = $attributes['imageWebp'] ?? '';
$image_thumb = $attributes['imageThumb'] ?? '';

$justify = $align === 'left' ? 'items-start text-left' : ($align === 'right' ? 'items-end text-right' : 'items-center text-center');
?>
<section class="{base_class} relative overflow-hidden flex <?php echo $justify; ?>" style="min-height: <?php echo esc_attr($height); ?>;">
  <?php if ($image): ?>
    <picture>
      <?php if ($image_webp): ?><source srcset="<?php echo esc_url($image_webp); ?>" type="image/webp"><?php endif; ?>
      <?php if ($image_thumb): ?><source srcset="<?php echo esc_url($image_thumb); ?>" media="(max-width: 640px)"><?php endif; ?>
      <img src="<?php echo esc_url($image); ?>" class="absolute inset-0 w-full h-full object-cover" loading="lazy">
    </picture>
  <?php endif; ?>
  <?php if ($show_overlay): ?><div class="absolute inset-0 bg-black/40"></div><?php endif; ?>
  <div class="relative container mx-auto py-16 flex flex-col gap-4">
    <?php if ($title): ?><h1 class="text-4xl md:text-6xl font-bold text-white"><?php echo esc_html($title); ?></h1><?php endif; ?>
    <?php if ($subtitle): ?><p class="text-xl md:text-2xl text-white max-w-3xl"><?php echo esc_html($subtitle); ?></p><?php endif; ?>
    <?php if ($show_button && $button_text): ?>
      <a href="<?php echo esc_url($button_url); ?>" class="inline-flex px-6 py-3 bg-primary text-white rounded-lg font-semibold w-max"><?php echo esc_html($button_text); ?></a>
    <?php endif; ?>
  </div>
</section>
"""
    else:
        return f"""<?php
$title = $attributes['title'] ?? '';
$subtitle = $attributes['subtitle'] ?? '';
$button_text = $attributes['buttonText'] ?? '';
$button_url = $attributes['buttonUrl'] ?? '#';
$show_button = $attributes['showButton'] ?? true;
$show_overlay = $attributes['showOverlay'] ?? true;
$height = $attributes['height'] ?? '70vh';
$align = $attributes['align'] ?? 'center';
$image = $attributes['imageUrl'] ?? '';
$image_webp = $attributes['imageWebp'] ?? '';
$image_thumb = $attributes['imageThumb'] ?? '';

$justify = $align === 'left' ? 'text-start' : ($align === 'right' ? 'text-end ms-auto' : 'text-center mx-auto');
?>
<section class="{base_class} position-relative overflow-hidden d-flex align-items-center" style="min-height: <?php echo esc_attr($height); ?>;">
  <?php if ($image): ?>
    <picture>
      <?php if ($image_webp): ?><source srcset="<?php echo esc_url($image_webp); ?>" type="image/webp"><?php endif; ?>
      <?php if ($image_thumb): ?><source srcset="<?php echo esc_url($image_thumb); ?>" media="(max-width: 640px)"><?php endif; ?>
      <img src="<?php echo esc_url($image); ?>" class="position-absolute top-0 start-0 w-100 h-100 object-fit-cover" loading="lazy">
    </picture>
  <?php endif; ?>
  <?php if ($show_overlay): ?><div class="position-absolute top-0 start-0 w-100 h-100 bg-dark opacity-50"></div><?php endif; ?>
  <div class="position-relative container py-5" style="z-index: 2;">
    <div class="d-flex flex-column gap-3 <?php echo esc_attr($justify); ?>">
      <?php if ($title): ?><h1 class="display-4 fw-bold text-white"><?php echo esc_html($title); ?></h1><?php endif; ?>
      <?php if ($subtitle): ?><p class="fs-4 text-white"><?php echo esc_html($subtitle); ?></p><?php endif; ?>
      <?php if ($show_button && $button_text): ?>
        <a href="<?php echo esc_url($button_url); ?>" class="btn btn-primary"><?php echo esc_html($button_text); ?></a>
      <?php endif; ?>
    </div>
  </div>
</section>
"""

__all__ = [
    '_generate_slider_render_php',
    '_render_simple_section',
    '_render_sidebar',
    '_render_search',
    '_render_pagination',
    '_render_header',
    '_render_footer',
    '_render_form',
    '_render_menu',
    '_render_gallery',
    '_render_section',
    '_render_cards',
    '_render_hero',
]
