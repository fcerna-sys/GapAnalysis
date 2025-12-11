"""
Módulo para crear bloques personalizados de Gutenberg
Incluye Slider, Hero, Section, Cards, etc.
"""
import os
import json
import re
from typing import Dict, List, Optional

def get_bem_prefix(theme_slug: Optional[str] = None) -> str:
    """
    Obtiene el prefijo BEM desde theme_slug.
    Convierte a formato válido (solo letras, números, guiones) y usa como prefijo.
    Si no hay theme_slug, usa 'img2html' como fallback.
    """
    if not theme_slug:
        return 'img2html'
    # Limpiar slug: solo letras, números, guiones; convertir a minúsculas
    clean = re.sub(r'[^a-z0-9-]', '', theme_slug.lower())
    # Si queda vacío o muy corto, usar fallback
    if not clean or len(clean) < 2:
        return 'img2html'
    return clean

def setup_css_framework(theme_dir: str, framework: str):
    """
    Configura el framework CSS seleccionado (Tailwind, Bootstrap o ninguno).
    """
    if framework == 'tailwind':
        _setup_tailwind(theme_dir)
    elif framework == 'bootstrap':
        _setup_bootstrap(theme_dir)
    else:
        # CSS propio - no hacer nada especial
        pass

def _setup_tailwind(theme_dir: str):
    """Configura Tailwind CSS con compilación automática."""
    try:
        # Crear tailwind.config.js
        tailwind_config = """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './**/*.php',
    './blocks/**/*.js',
    './templates/**/*.html',
    './parts/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        // Colores del tema se agregarán automáticamente
      },
    },
  },
  plugins: [],
  corePlugins: {
    preflight: false, // Evitar conflictos con WordPress
  },
}
"""
        config_path = os.path.join(theme_dir, 'tailwind.config.js')
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(tailwind_config)
        
        # Crear package.json para compilar Tailwind
        package_json = {
            "name": "img2html-theme",
            "version": "1.0.0",
            "scripts": {
                "build:css": "tailwindcss -i ./src/input.css -o ./assets/css/tailwind.css --minify",
                "watch:css": "tailwindcss -i ./src/input.css -o ./assets/css/tailwind.css --watch"
            },
            "devDependencies": {
                "tailwindcss": "^3.4.0"
            }
        }
        package_path = os.path.join(theme_dir, 'package.json')
        with open(package_path, 'w', encoding='utf-8') as f:
            json.dump(package_json, f, indent=2)
        
        # Crear directorio src y archivo input.css
        src_dir = os.path.join(theme_dir, 'src')
        os.makedirs(src_dir, exist_ok=True)
        input_css = """@tailwind base;
@tailwind components;
@tailwind utilities;

/* Estilos personalizados del tema */
"""
        input_css_path = os.path.join(src_dir, 'input.css')
        with open(input_css_path, 'w', encoding='utf-8') as f:
            f.write(input_css)
        
        # Crear assets/css si no existe
        assets_css_dir = os.path.join(theme_dir, 'assets', 'css')
        os.makedirs(assets_css_dir, exist_ok=True)
        
        # Crear tailwind.css compilado básico (se recompilará después)
        tailwind_css = """/* Tailwind CSS compilado */
/* Este archivo se regenera con: npm run build:css */
"""
        tailwind_css_path = os.path.join(assets_css_dir, 'tailwind.css')
        with open(tailwind_css_path, 'w', encoding='utf-8') as f:
            f.write(tailwind_css)
        
        print("Tailwind CSS configurado. Ejecuta 'npm install && npm run build:css' para compilar.")
        
    except Exception as e:
        print(f"Error al configurar Tailwind: {e}")

def _setup_bootstrap(theme_dir: str):
    """Configura Bootstrap 5 con archivos locales."""
    try:
        # Crear directorio assets
        assets_dir = os.path.join(theme_dir, 'assets')
        os.makedirs(assets_dir, exist_ok=True)
        css_dir = os.path.join(assets_dir, 'css')
        js_dir = os.path.join(assets_dir, 'js')
        os.makedirs(css_dir, exist_ok=True)
        os.makedirs(js_dir, exist_ok=True)
        
        # Crear bootstrap.custom.css
        bootstrap_custom = """/* Bootstrap 5 Custom Styles */
/* Solo incluye lo necesario para evitar conflictos con Gutenberg */

/* Importar Bootstrap desde node_modules o CDN local */
@import url('bootstrap.min.css');

/* Scope local para evitar conflictos */
.img2html-theme {
  /* Estilos del tema aquí */
}

/* Evitar conflictos con editor */
.block-editor-page .img2html-theme {
  /* Estilos específicos del editor */
}
"""
        bootstrap_custom_path = os.path.join(css_dir, 'bootstrap.custom.css')
        with open(bootstrap_custom_path, 'w', encoding='utf-8') as f:
            f.write(bootstrap_custom)
        
        # Crear README para Bootstrap
        bootstrap_readme = """# Bootstrap 5 Setup

Para usar Bootstrap 5 en este tema:

1. Descarga Bootstrap desde https://getbootstrap.com/
2. Copia bootstrap.min.css a assets/css/
3. Copia bootstrap.bundle.min.js a assets/js/
4. O usa npm: npm install bootstrap@5

El tema usará bootstrap.custom.css para estilos personalizados.
"""
        readme_path = os.path.join(assets_dir, 'BOOTSTRAP_README.md')
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(bootstrap_readme)
        
        print("Bootstrap 5 configurado. Descarga los archivos desde getbootstrap.com")
        
    except Exception as e:
        print(f"Error al configurar Bootstrap: {e}")

def create_custom_blocks(theme_dir: str, css_framework: str, plan: Dict, theme_slug: Optional[str] = None):
    """
    Crea todos los bloques personalizados de Gutenberg.
    Usa prefijo BEM derivado de theme_slug.
    """
    blocks_dir = os.path.join(theme_dir, 'blocks')
    os.makedirs(blocks_dir, exist_ok=True)
    
    # Obtener prefijo BEM
    bem_prefix = get_bem_prefix(theme_slug)
    
    # Bloques principales (pasar prefijo BEM)
    create_slider_block(blocks_dir, css_framework, bem_prefix)
    create_hero_block(blocks_dir, css_framework, bem_prefix)
    create_section_block(blocks_dir, css_framework, bem_prefix)
    create_cards_block(blocks_dir, css_framework, bem_prefix)
    create_gallery_block(blocks_dir, css_framework, bem_prefix)
    create_text_image_block(blocks_dir, css_framework, bem_prefix)
    create_sidebar_block(blocks_dir, css_framework, bem_prefix)
    create_search_block(blocks_dir, css_framework, bem_prefix)
    create_pagination_block(blocks_dir, css_framework, bem_prefix)
    create_header_block(blocks_dir, css_framework, bem_prefix)
    create_footer_block(blocks_dir, css_framework, bem_prefix)
    create_form_block(blocks_dir, css_framework, bem_prefix)
    create_menu_block(blocks_dir, css_framework, bem_prefix)
    
    # Registrar bloques en functions.php
    register_blocks_in_functions(theme_dir, blocks_dir)

def create_slider_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """
    Crea el bloque Slider completo con todas las funcionalidades.
    Usa prefijo BEM para clases CSS.
    """
    slider_dir = os.path.join(blocks_dir, 'slider')
    os.makedirs(slider_dir, exist_ok=True)
    
    # block.json
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": "img2html/slider",
        "version": "1.0.0",
        "title": "Slider",
        "category": "img2html",
        "icon": "slides",
        "description": "Slider administrable con múltiples diapositivas",
        "keywords": ["slider", "carousel", "slideshow"],
        "textdomain": "img2html",
        "editorScript": "file:./index.js",
        "editorStyle": "file:./editor.css",
        "style": "file:./style.css",
        "render": "file:./render.php",
        "supports": {
            "align": ["wide", "full"],
            "html": False
        },
        "attributes": {
            "showSlider": {
                "type": "boolean",
                "default": True
            },
            "fullWidth": {
                "type": "boolean",
                "default": False
            },
            "showArrows": {
                "type": "boolean",
                "default": True
            },
            "showDots": {
                "type": "boolean",
                "default": True
            },
            "autoplay": {
                "type": "boolean",
                "default": True
            },
            "autoplaySpeed": {
                "type": "number",
                "default": 5000
            },
            "transitionSpeed": {
                "type": "number",
                "default": 500
            },
            "height": {
                "type": "string",
                "default": "70vh"
            },
            "slides": {
                "type": "array",
                "default": []
            }
        }
    }
    
    block_json_path = os.path.join(slider_dir, 'block.json')
    with open(block_json_path, 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2, ensure_ascii=False)
    
    # render.php (frontend)
    render_php = _generate_slider_render_php(css_framework, bem_prefix)
    render_path = os.path.join(slider_dir, 'render.php')
    with open(render_path, 'w', encoding='utf-8') as f:
        f.write(render_php)
    
    # index.js (editor)
    editor_js = _generate_slider_editor_js()
    editor_js_path = os.path.join(slider_dir, 'index.js')
    with open(editor_js_path, 'w', encoding='utf-8') as f:
        f.write(editor_js)
    
    # style.css (frontend)
    style_css = _generate_slider_style_css(css_framework)
    style_path = os.path.join(slider_dir, 'style.css')
    with open(style_path, 'w', encoding='utf-8') as f:
        f.write(style_css)
    
    # editor.css (editor)
    editor_css = _generate_slider_editor_css()
    editor_css_path = os.path.join(slider_dir, 'editor.css')
    with open(editor_css_path, 'w', encoding='utf-8') as f:
        f.write(editor_css)

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
(function() {
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
    
    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.classList.toggle('active', i === index);
        });
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === index);
        });
        currentSlide = index;
    }
    
    function nextSlide() {
        const next = (currentSlide + 1) % slides.length;
        showSlide(next);
    }
    
    function prevSlide() {
        const prev = (currentSlide - 1 + slides.length) % slides.length;
        showSlide(prev);
    }
    
    if (prevBtn) prevBtn.addEventListener('click', prevSlide);
    if (nextBtn) nextBtn.addEventListener('click', nextSlide);
    
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => showSlide(index));
    });
    
    if (autoplay && slides.length > 1) {
        autoplayInterval = setInterval(nextSlide, speed);
        slider.addEventListener('mouseenter', () => clearInterval(autoplayInterval));
        slider.addEventListener('mouseleave', () => {
            autoplayInterval = setInterval(nextSlide, speed);
        });
    }
})();
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

def _generate_slider_editor_js() -> str:
    """Genera el JavaScript del editor para el bloque Slider."""
    return """import { registerBlockType } from '@wordpress/blocks';
import { 
    InspectorControls, 
    MediaUpload, 
    MediaUploadCheck,
    useBlockProps,
    RichText
} from '@wordpress/block-editor';
import { 
    PanelBody, 
    Button, 
    ToggleControl, 
    RangeControl,
    SelectControl,
    TextControl
} from '@wordpress/components';
import { __ } from '@wordpress/i18n';
import './editor.css';

registerBlockType('img2html/slider', {
    edit: ({ attributes, setAttributes }) => {
        const {
            showSlider,
            fullWidth,
            showArrows,
            showDots,
            autoplay,
            autoplaySpeed,
            transitionSpeed,
            height,
            slides = []
        } = attributes;

        const blockProps = useBlockProps({
            className: 'img2html-slider-editor'
        });

        const addSlide = () => {
            const newSlide = {
                imageUrl: '',
                imageWebp: '',
                imageThumb: '',
                imageId: null,
                title: '',
                subtitle: '',
                buttonText: '',
                buttonUrl: '',
                showButton: true,
                textPosition: 'center',
                showOverlay: true
            };
            setAttributes({
                slides: [...slides, newSlide]
            });
        };

        const removeSlide = (index) => {
            const newSlides = slides.filter((_, i) => i !== index);
            setAttributes({ slides: newSlides });
        };

        const updateSlide = (index, field, value) => {
            const newSlides = [...slides];
            newSlides[index] = { ...newSlides[index], [field]: value };
            setAttributes({ slides: newSlides });
        };

        const moveSlide = (index, direction) => {
            const newSlides = [...slides];
            const targetIndex = direction === 'up' ? index - 1 : index + 1;
            if (targetIndex >= 0 && targetIndex < newSlides.length) {
                [newSlides[index], newSlides[targetIndex]] = [newSlides[targetIndex], newSlides[index]];
                setAttributes({ slides: newSlides });
            }
        };

        return (
            <div {...blockProps}>
                <InspectorControls>
                    <PanelBody title={__('Configuración del Slider', 'img2html')} initialOpen={true}>
                        <ToggleControl
                            label={__('Mostrar Slider', 'img2html')}
                            checked={showSlider}
                            onChange={(value) => setAttributes({ showSlider: value })}
                        />
                        <ToggleControl
                            label={__('Slider a pantalla completa', 'img2html')}
                            checked={fullWidth}
                            onChange={(value) => setAttributes({ fullWidth: value })}
                        />
                        <ToggleControl
                            label={__('Mostrar flechas', 'img2html')}
                            checked={showArrows}
                            onChange={(value) => setAttributes({ showArrows: value })}
                        />
                        <ToggleControl
                            label={__('Mostrar puntos', 'img2html')}
                            checked={showDots}
                            onChange={(value) => setAttributes({ showDots: value })}
                        />
                        <ToggleControl
                            label={__('Autoplay', 'img2html')}
                            checked={autoplay}
                            onChange={(value) => setAttributes({ autoplay: value })}
                        />
                        <RangeControl
                            label={__('Velocidad del autoplay (ms)', 'img2html')}
                            value={autoplaySpeed}
                            onChange={(value) => setAttributes({ autoplaySpeed: value })}
                            min={1000}
                            max={10000}
                            step={500}
                        />
                        <RangeControl
                            label={__('Duración de transición (ms)', 'img2html')}
                            value={transitionSpeed}
                            onChange={(value) => setAttributes({ transitionSpeed: value })}
                            min={100}
                            max={2000}
                            step={100}
                        />
                        <SelectControl
                            label={__('Altura del slider', 'img2html')}
                            value={height}
                            options={[
                                { label: 'Auto', value: 'auto' },
                                { label: '60vh', value: '60vh' },
                                { label: '70vh', value: '70vh' },
                                { label: '100vh', value: '100vh' }
                            ]}
                            onChange={(value) => setAttributes({ height: value })}
                        />
                    </PanelBody>
                </InspectorControls>

                <div className="slider-editor-content">
                    <div className="slider-editor-header">
                        <h3>{__('Slider', 'img2html')}</h3>
                        <Button isPrimary onClick={addSlide}>
                            {__('Agregar nueva diapositiva', 'img2html')}
                        </Button>
                    </div>

                    {slides.length === 0 ? (
                        <div className="slider-empty-state">
                            <p>{__('No hay diapositivas. Agrega una para comenzar.', 'img2html')}</p>
                        </div>
                    ) : (
                        <div className="slider-slides-list">
                            {slides.map((slide, index) => (
                                <div key={index} className="slider-slide-editor">
                                    <div className="slide-header">
                                        <h4>{__('Diapositiva', 'img2html')} {index + 1}</h4>
                                        <div className="slide-actions">
                                            <Button 
                                                isSmall 
                                                onClick={() => moveSlide(index, 'up')}
                                                disabled={index === 0}
                                            >
                                                ↑
                                            </Button>
                                            <Button 
                                                isSmall 
                                                onClick={() => moveSlide(index, 'down')}
                                                disabled={index === slides.length - 1}
                                            >
                                                ↓
                                            </Button>
                                            <Button 
                                                isDestructive 
                                                isSmall 
                                                onClick={() => removeSlide(index)}
                                            >
                                                {__('Eliminar', 'img2html')}
                                            </Button>
                                        </div>
                                    </div>

                                    <MediaUploadCheck>
                                        <MediaUpload
                                            onSelect={(media) => {
                                                updateSlide(index, 'imageUrl', media.url);
                                                updateSlide(index, 'imageId', media.id);
                                            }}
                                            allowedTypes={['image']}
                                            value={slide.imageId}
                                            render={({ open }) => (
                                                <Button onClick={open} isSecondary>
                                                    {slide.imageUrl 
                                                        ? __('Cambiar Imagen', 'img2html')
                                                        : __('Seleccionar Imagen', 'img2html')
                                                    }
                                                </Button>
                                            )}
                                        />
                                    </MediaUploadCheck>

                                    {slide.imageUrl && (
                                        <img src={slide.imageUrl} alt="" className="slide-preview" />
                                    )}

                                    <TextControl
                                        label={__('Título', 'img2html')}
                                        value={slide.title}
                                        onChange={(value) => updateSlide(index, 'title', value)}
                                    />

                                    <TextControl
                                        label={__('Subtítulo', 'img2html')}
                                        value={slide.subtitle}
                                        onChange={(value) => updateSlide(index, 'subtitle', value)}
                                    />

                                    <ToggleControl
                                        label={__('Mostrar botón', 'img2html')}
                                        checked={slide.showButton}
                                        onChange={(value) => updateSlide(index, 'showButton', value)}
                                    />

                                    {slide.showButton && (
                                        <>
                                            <TextControl
                                                label={__('Texto del botón', 'img2html')}
                                                value={slide.buttonText}
                                                onChange={(value) => updateSlide(index, 'buttonText', value)}
                                            />
                                            <TextControl
                                                label={__('URL del botón', 'img2html')}
                                                value={slide.buttonUrl}
                                                onChange={(value) => updateSlide(index, 'buttonUrl', value)}
                                            />
                                        </>
                                    )}

                                    <SelectControl
                                        label={__('Posición del texto', 'img2html')}
                                        value={slide.textPosition}
                                        options={[
                                            { label: __('Izquierda', 'img2html'), value: 'left' },
                                            { label: __('Centro', 'img2html'), value: 'center' },
                                            { label: __('Derecha', 'img2html'), value: 'right' }
                                        ]}
                                        onChange={(value) => updateSlide(index, 'textPosition', value)}
                                    />

                                    <ToggleControl
                                        label={__('Overlay oscuro', 'img2html')}
                                        checked={slide.showOverlay}
                                        onChange={(value) => updateSlide(index, 'showOverlay', value)}
                                    />
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        );
    },

    save: () => {
        // El bloque usa render.php para el frontend
        return null;
    }
});
"""

def _generate_slider_style_css(css_framework: str) -> str:
    """Genera los estilos CSS del slider según el framework."""
    if css_framework == 'tailwind':
        return """/* Estilos del Slider - Tailwind CSS */
/* La mayoría de estilos se manejan con clases de Tailwind */
"""
    elif css_framework == 'bootstrap':
        return """/* Estilos del Slider - Bootstrap 5 */
/* Los estilos principales vienen de Bootstrap */
.img2html-slider .carousel-overlay {
    z-index: 1;
}
"""
    else:
        return """/* Estilos del Slider - CSS Propio */
.img2html-slider {
    position: relative;
    overflow: hidden;
}

.img2html-slider .slider-wrapper {
    position: relative;
    width: 100%;
    height: 100%;
}

.img2html-slider .slide {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    transition: opacity 0.5s ease-in-out;
}

.img2html-slider .slide.active {
    opacity: 1;
    z-index: 1;
}

.img2html-slider .slider-arrow {
    cursor: pointer;
    z-index: 10;
}

.img2html-slider .slider-dots {
    z-index: 10;
}

.img2html-slider .dot {
    cursor: pointer;
    border: none;
    background: rgba(255, 255, 255, 0.5);
}

.img2html-slider .dot.active {
    background: rgba(255, 255, 255, 1);
}
"""

def _generate_slider_editor_css() -> str:
    """Genera los estilos CSS del editor."""
    return """/* Estilos del Editor del Slider */
.img2html-slider-editor {
    border: 2px dashed #ccc;
    padding: 20px;
    margin: 20px 0;
}

.slider-editor-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.slider-empty-state {
    text-align: center;
    padding: 40px;
    color: #666;
}

.slider-slides-list {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.slider-slide-editor {
    border: 1px solid #ddd;
    padding: 15px;
    border-radius: 4px;
    background: #f9f9f9;
}

.slide-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}

.slide-actions {
    display: flex;
    gap: 5px;
}

.slide-preview {
    max-width: 100%;
    height: auto;
    margin: 10px 0;
    border-radius: 4px;
}
"""

def create_hero_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Crea el bloque Hero."""
    hero_dir = os.path.join(blocks_dir, 'hero')
    os.makedirs(hero_dir, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": "img2html/hero",
        "version": "1.0.0",
        "title": "Hero",
        "category": "img2html",
        "icon": "cover-image",
        "description": "Bloque Hero administrable",
        "textdomain": "img2html",
        "render": "file:./render.php",
        "attributes": {
            "title": {"type": "string", "default": "Título hero"},
            "subtitle": {"type": "string", "default": "Subtítulo"},
            "buttonText": {"type": "string", "default": "Call to action"},
            "buttonUrl": {"type": "string", "default": "#"},
            "showButton": {"type": "boolean", "default": True},
            "showOverlay": {"type": "boolean", "default": True},
            "height": {"type": "string", "default": "70vh"},
            "align": {"type": "string", "default": "center"},
            "imageUrl": {"type": "string", "default": ""},
            "imageWebp": {"type": "string", "default": ""},
            "imageThumb": {"type": "string", "default": ""}
        }
    }
    block_json_path = os.path.join(hero_dir, 'block.json')
    with open(block_json_path, 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2)
    with open(os.path.join(hero_dir, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(_render_hero(css_framework, bem_prefix))
    with open(os.path.join(hero_dir, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* hero styles */")

def create_section_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Crea el bloque Section con prefijo BEM."""
    section_dir = os.path.join(blocks_dir, 'section')
    os.makedirs(section_dir, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": "img2html/section",
        "version": "1.0.0",
        "title": "Sección",
        "category": "img2html",
        "icon": "columns",
        "description": "Bloque de sección multipropósito",
        "textdomain": "img2html",
        "render": "file:./render.php",
        "attributes": {
            "variant": {"type": "string", "default": "default"},
            "title": {"type": "string", "default": "Sección"},
            "content": {"type": "string", "default": "Texto de ejemplo"},
            "columns": {"type": "number", "default": 2},
            "imageUrl": {"type": "string", "default": ""},
            "imageWebp": {"type": "string", "default": ""},
            "imageThumb": {"type": "string", "default": ""}
        }
    }
    block_json_path = os.path.join(section_dir, 'block.json')
    with open(block_json_path, 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2)
    with open(os.path.join(section_dir, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(_render_section(css_framework, bem_prefix))
    with open(os.path.join(section_dir, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* section styles */")

def create_cards_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Crea el bloque Cards."""
    cards_dir = os.path.join(blocks_dir, 'cards')
    os.makedirs(cards_dir, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": "img2html/cards",
        "version": "1.0.0",
        "title": "Cards",
        "category": "img2html",
        "icon": "grid-view",
        "description": "Bloque de tarjetas",
        "textdomain": "img2html",
        "render": "file:./render.php",
        "attributes": {
            "cards": {"type": "array", "default": []},
            "columns": {"type": "number", "default": 3},
            "gap": {"type": "number", "default": 16}
        }
    }
    block_json_path = os.path.join(cards_dir, 'block.json')
    with open(block_json_path, 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2)
    with open(os.path.join(cards_dir, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(_render_cards(css_framework, bem_prefix))
    with open(os.path.join(cards_dir, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* cards styles */")

def create_gallery_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Crea el bloque Gallery."""
    gallery_dir = os.path.join(blocks_dir, 'gallery')
    os.makedirs(gallery_dir, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": "img2html/gallery",
        "version": "1.0.0",
        "title": "Galería",
        "category": "img2html",
        "icon": "format-gallery",
        "description": "Bloque de galería",
        "textdomain": "img2html",
        "render": "file:./render.php",
        "attributes": {
            "images": {"type": "array", "default": []},
            "columns": {"type": "number", "default": 3},
            "gap": {"type": "number", "default": 12},
            "lightbox": {"type": "boolean", "default": False}
        }
    }
    block_json_path = os.path.join(gallery_dir, 'block.json')
    with open(block_json_path, 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2)
    with open(os.path.join(gallery_dir, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(_render_gallery(css_framework, bem_prefix))
    with open(os.path.join(gallery_dir, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* gallery styles */")


# --- Bloques adicionales multipropósito ---

def create_text_image_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    dir_path = os.path.join(blocks_dir, 'text-image')
    os.makedirs(dir_path, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": "img2html/text-image",
        "version": "1.0.0",
        "title": "Texto + Imagen",
        "category": "img2html",
        "icon": "align-pull-left",
        "description": "Bloque de texto con imagen multipropósito",
        "textdomain": "img2html",
        "editorScript": "file:./index.js",
        "style": "file:./style.css",
        "attributes": {
            "layout": {"type": "string", "default": "image-left"},
            "title": {"type": "string", "default": "Título de sección"},
            "body": {"type": "string", "default": "Contenido de ejemplo"},
            "imageUrl": {"type": "string", "default": ""},
            "imageWebp": {"type": "string", "default": ""},
            "imageThumb": {"type": "string", "default": ""},
            "imageId": {"type": "number"},
            "bgStyle": {"type": "string", "default": "light"},
            "padding": {"type": "string", "default": "md"}
        }
    }
    with open(os.path.join(dir_path, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2, ensure_ascii=False)
    with open(os.path.join(dir_path, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(_render_simple_section(css_framework, "text-image", bem_prefix))
    with open(os.path.join(dir_path, 'index.js'), 'w', encoding='utf-8') as f:
        f.write(_editor_simple_section())
    with open(os.path.join(dir_path, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* text-image styles */")


def create_sidebar_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    dir_path = os.path.join(blocks_dir, 'sidebar')
    os.makedirs(dir_path, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": "img2html/sidebar",
        "version": "1.0.0",
        "title": "Sidebar Dinámico",
        "category": "img2html",
        "icon": "menu",
        "description": "Sidebar administrable con enlaces y widgets",
        "textdomain": "img2html",
        "editorScript": "file:./index.js",
        "style": "file:./style.css",
        "attributes": {
            "title": {"type": "string", "default": "Sidebar"},
            "links": {"type": "array", "default": []},
            "showRecent": {"type": "boolean", "default": True},
            "showCategories": {"type": "boolean", "default": True},
            "showTags": {"type": "boolean", "default": True},
            "styleVariant": {"type": "string", "default": "light"},
            "padding": {"type": "string", "default": "md"},
            "border": {"type": "boolean", "default": False},
            "linkStyle": {"type": "string", "default": "normal"}
        }
    }
    with open(os.path.join(dir_path, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2, ensure_ascii=False)
    with open(os.path.join(dir_path, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(_render_sidebar(css_framework, bem_prefix))
    with open(os.path.join(dir_path, 'index.js'), 'w', encoding='utf-8') as f:
        f.write(_editor_sidebar())
    with open(os.path.join(dir_path, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* sidebar styles */")


def create_search_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    dir_path = os.path.join(blocks_dir, 'search-extended')
    os.makedirs(dir_path, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": "img2html/search-extended",
        "version": "1.0.0",
        "title": "Buscador",
        "category": "img2html",
        "icon": "search",
        "description": "Buscador extendido",
        "textdomain": "img2html",
        "editorScript": "file:./index.js",
        "style": "file:./style.css",
        "attributes": {
            "size": {"type": "string", "default": "md"},
            "rounded": {"type": "boolean", "default": True},
            "buttonInside": {"type": "boolean", "default": True},
            "placeholder": {"type": "string", "default": "Buscar..."},
            "showIcon": {"type": "boolean", "default": True}
        }
    }
    with open(os.path.join(dir_path, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2, ensure_ascii=False)
    with open(os.path.join(dir_path, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(_render_search(css_framework, bem_prefix))
    with open(os.path.join(dir_path, 'index.js'), 'w', encoding='utf-8') as f:
        f.write(_editor_search())
    with open(os.path.join(dir_path, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* search styles */")


def create_pagination_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    dir_path = os.path.join(blocks_dir, 'pagination')
    os.makedirs(dir_path, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": "img2html/pagination",
        "version": "1.0.0",
        "title": "Paginación",
        "category": "img2html",
        "icon": "controls-repeat",
        "description": "Bloque de paginación",
        "textdomain": "img2html",
        "editorScript": "file:./index.js",
        "style": "file:./style.css",
        "attributes": {
            "mode": {"type": "string", "default": "numbers"},
            "align": {"type": "string", "default": "center"},
            "size": {"type": "string", "default": "md"},
            "gap": {"type": "number", "default": 8},
            "showPageCount": {"type": "boolean", "default": False}
        }
    }
    with open(os.path.join(dir_path, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2, ensure_ascii=False)
    with open(os.path.join(dir_path, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(_render_pagination(css_framework, bem_prefix))
    with open(os.path.join(dir_path, 'index.js'), 'w', encoding='utf-8') as f:
        f.write(_editor_pagination())
    with open(os.path.join(dir_path, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* pagination styles */")


def create_header_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    dir_path = os.path.join(blocks_dir, 'header')
    os.makedirs(dir_path, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": "img2html/header",
        "version": "1.0.0",
        "title": "Header",
        "category": "img2html",
        "icon": "admin-site",
        "description": "Header editable con logo, menú y CTA",
        "textdomain": "img2html",
        "editorScript": "file:./index.js",
        "style": "file:./style.css",
        "attributes": {
            "sticky": {"type": "boolean", "default": False},
            "transparent": {"type": "boolean", "default": False},
            "scrollChange": {"type": "boolean", "default": False},
            "height": {"type": "string", "default": "md"},
            "ctaText": {"type": "string", "default": "Contáctanos"},
            "ctaUrl": {"type": "string", "default": "#"},
            "ctaShow": {"type": "boolean", "default": True}
        }
    }
    with open(os.path.join(dir_path, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2, ensure_ascii=False)
    with open(os.path.join(dir_path, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(_render_header(css_framework, bem_prefix))
    with open(os.path.join(dir_path, 'index.js'), 'w', encoding='utf-8') as f:
        f.write(_editor_header())
    with open(os.path.join(dir_path, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* header styles */")


def create_footer_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    dir_path = os.path.join(blocks_dir, 'footer')
    os.makedirs(dir_path, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": "img2html/footer",
        "version": "1.0.0",
        "title": "Footer",
        "category": "img2html",
        "icon": "editor-insertmore",
        "description": "Footer editable multicolumna",
        "textdomain": "img2html",
        "editorScript": "file:./index.js",
        "style": "file:./style.css",
        "attributes": {
            "columns": {"type": "number", "default": 3},
            "bg": {"type": "string", "default": "dark"},
            "legal": {"type": "string", "default": "© 2025. Todos los derechos reservados."},
            "links": {"type": "array", "default": []},
            "showSocial": {"type": "boolean", "default": True}
        }
    }
    with open(os.path.join(dir_path, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2, ensure_ascii=False)
    with open(os.path.join(dir_path, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(_render_footer(css_framework, bem_prefix))
    with open(os.path.join(dir_path, 'index.js'), 'w', encoding='utf-8') as f:
        f.write(_editor_footer())
    with open(os.path.join(dir_path, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* footer styles */")


def create_form_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    dir_path = os.path.join(blocks_dir, 'form')
    os.makedirs(dir_path, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": "img2html/form",
        "version": "1.0.0",
        "title": "Formulario de Contacto",
        "category": "img2html",
        "icon": "email",
        "description": "Formulario nativo (nombre, email, teléfono, mensaje)",
        "textdomain": "img2html",
        "editorScript": "file:./index.js",
        "style": "file:./style.css",
        "render": "file:./render.php",
        "attributes": {
            "showPhone": {"type": "boolean", "default": True},
            "submitText": {"type": "string", "default": "Enviar"},
            "successMessage": {"type": "string", "default": "Mensaje enviado"},
            "errorMessage": {"type": "string", "default": "Ocurrió un error"},
            "endpoint": {"type": "string", "default": "/wp-json/img2html/v1/contact"}
        }
    }
    with open(os.path.join(dir_path, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2, ensure_ascii=False)
    with open(os.path.join(dir_path, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(_render_form(css_framework, bem_prefix))
    with open(os.path.join(dir_path, 'index.js'), 'w', encoding='utf-8') as f:
        f.write(_editor_form())
    with open(os.path.join(dir_path, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* form styles */")


def create_menu_block(blocks_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    dir_path = os.path.join(blocks_dir, 'menu')
    os.makedirs(dir_path, exist_ok=True)
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": "img2html/menu",
        "version": "1.0.0",
        "title": "Menú Avanzado",
        "category": "img2html",
        "icon": "menu",
        "description": "Menú desktop/mobile con CTA y redes",
        "textdomain": "img2html",
        "editorScript": "file:./index.js",
        "style": "file:./style.css",
        "render": "file:./render.php",
        "attributes": {
            "sticky": {"type": "boolean", "default": False},
            "transparent": {"type": "boolean", "default": False},
            "ctaText": {"type": "string", "default": "Contáctanos"},
            "ctaUrl": {"type": "string", "default": "#"},
            "ctaShow": {"type": "boolean", "default": True},
            "showSocial": {"type": "boolean", "default": False}
        }
    }
    with open(os.path.join(dir_path, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2, ensure_ascii=False)
    with open(os.path.join(dir_path, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(_render_menu(css_framework, bem_prefix))
    with open(os.path.join(dir_path, 'index.js'), 'w', encoding='utf-8') as f:
        f.write(_editor_menu())
    with open(os.path.join(dir_path, 'style.css'), 'w', encoding='utf-8') as f:
        f.write("/* menu styles */")


# --- Render helpers (simplificados) ---

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
(function(){
  const form = document.currentScript.previousElementSibling;
  if(!form) return;
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(form);
    const endpoint = form.dataset.endpoint || '/wp-json/img2html/v1/contact';
    try {
      await fetch(endpoint, { method: 'POST', body: fd });
      form.querySelector('.form-feedback').classList.remove('hidden');
      form.querySelector('.form-error').classList.add('hidden');
      form.reset();
    } catch(err) {
      form.querySelector('.form-error').classList.remove('hidden');
    }
  });
})();
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
(function(){
  const form = document.currentScript.previousElementSibling;
  if(!form) return;
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(form);
    const endpoint = form.dataset.endpoint || '/wp-json/img2html/v1/contact';
    try {
      await fetch(endpoint, { method: 'POST', body: fd });
      form.querySelector('.form-feedback').classList.remove('d-none');
      form.querySelector('.form-error').classList.add('d-none');
      form.reset();
    } catch(err) {
      form.querySelector('.form-error').classList.remove('d-none');
    }
  });
})();
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
(function(){
  const nav = document.currentScript.previousElementSibling;
  if(!nav) return;
  const toggle = nav.querySelector('.menu-toggle');
  const panel = nav.querySelector('.mobile-panel');
  const closeBtn = nav.querySelector('.menu-close');
  const desktopNav = nav.querySelector('.wp-block-navigation');
  if(toggle && panel){
    toggle.addEventListener('click', () => panel.classList.remove('hidden'));
  }
  if(closeBtn && panel){
    closeBtn.addEventListener('click', () => panel.classList.add('hidden'));
  }

  // Dropdown desktop (hover) para items con submenú
  if (desktopNav) {
    desktopNav.querySelectorAll('li.has-child').forEach((item) => {
      item.classList.add('relative');
      const submenu = item.querySelector('ul');
      if (!submenu) return;
      submenu.classList.add('absolute','hidden','bg-white','shadow','rounded','mt-2','min-w-[200px]','z-50','p-2');
      item.addEventListener('mouseenter', () => submenu.classList.remove('hidden'));
      item.addEventListener('mouseleave', () => submenu.classList.add('hidden'));
    });
  }
})();
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
(function(){
  // Dropdown hover para desktop en Bootstrap
  const nav = document.currentScript.previousElementSibling;
  if(!nav) return;
  const dropdowns = nav.querySelectorAll('.menu-item-has-children, .has-child');
  dropdowns.forEach((item) => {
    const submenu = item.querySelector('ul');
    if(!submenu) return;
    item.classList.add('position-relative');
    submenu.classList.add('dropdown-menu','show');
    submenu.style.display = 'none';
    item.addEventListener('mouseenter', () => { submenu.style.display = 'block'; });
    item.addEventListener('mouseleave', () => { submenu.style.display = 'none'; });
  });
})();
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
if ($ratios) {
  $parts = [];
  foreach ($ratios as $r) {
    if ($r) { $parts[] = "minmax(0, {$r}%)"; }
  }
  if (!empty($parts)) {
    $grid_style = 'style="grid-template-columns:' . implode(' ', $parts) . ';"';
  }
}
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
      if (!empty($ratios)) {
        $idx = array_search($img, $images, true);
        if ($idx !== false && isset($ratios[$idx])) {
          $calc = intval(round(($ratios[$idx]/100.0)*12));
          if ($calc > 0) { $w = max(1, min(12, $calc)); }
        }
      }
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
        if ($ratios) {
          foreach ($ratios as $r) {
            $width = max(1, min(12, intval(round(($r/100.0)*12))));
            $col_classes[] = 'col-md-' . $width;
          }
        }
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
if (isset($attributes['layoutRows']) && is_array($attributes['layoutRows']) && !empty($attributes['layoutRows'])) {
  // si el plan trajo layout, usar el primer rows para columnas
  $first = $attributes['layoutRows'][0];
  if (isset($first['columns']) && is_array($first['columns'])) {
    $cols = max(1, min(4, count($first['columns'])));
  }
}
$ratios = ($attributes['layoutRows'][0]['ratios_percent'] ?? []) ?: [];
$grid_style = '';
if ($ratios) {
  $parts = [];
  foreach ($ratios as $r) {
    if ($r) { $parts[] = "minmax(0, {$r}%)"; }
  }
  if (!empty($parts)) {
    $grid_style = 'style="grid-template-columns:' . implode(' ', $parts) . ';"';
  }
}
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
if (isset($attributes['layoutRows']) && is_array($attributes['layoutRows']) && !empty($attributes['layoutRows'])) {
  $first = $attributes['layoutRows'][0];
  if (isset($first['columns']) && is_array($first['columns'])) {
    $cols = max(1, min(4, count($first['columns'])));
  }
}
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
        if (!empty($ratios)) {
          $idx = array_search($card, $cards, true);
          if ($idx !== false && isset($ratios[$idx])) {
            $calc = intval(round(($ratios[$idx]/100.0)*12));
            if ($calc > 0) { $w = max(1, min(12, $calc)); }
          }
        }
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


# --- Editor JS helpers cortos ---

def _editor_simple_section() -> str:
    return """import { registerBlockType } from '@wordpress/blocks';
import { InspectorControls, MediaUpload, MediaUploadCheck, useBlockProps, RichText } from '@wordpress/block-editor';
import { PanelBody, SelectControl, Button, TextareaControl, TextControl } from '@wordpress/components';

registerBlockType('img2html/text-image', {
  edit: ({ attributes, setAttributes }) => {
    const { layout, title, body, imageUrl, bgStyle, padding } = attributes;
    const blockProps = useBlockProps({ className: 'img2html-text-image-editor' });
    return (
      <div {...blockProps}>
        <InspectorControls>
          <PanelBody title=\"Ajustes\" initialOpen={true}>
            <SelectControl
              label=\"Layout\"
              value={layout}
              options={[
                { label: 'Imagen izquierda', value: 'image-left' },
                { label: 'Imagen derecha', value: 'image-right' }
              ]}
              onChange={(value) => setAttributes({ layout: value })}
            />
            <SelectControl
              label=\"Fondo\"
              value={bgStyle}
              options={[
                { label: 'Claro', value: 'light' },
                { label: 'Oscuro', value: 'dark' }
              ]}
              onChange={(value) => setAttributes({ bgStyle: value })}
            />
            <SelectControl
              label=\"Padding\"
              value={padding}
              options={[
                { label: 'Pequeño', value: 'sm' },
                { label: 'Medio', value: 'md' },
                { label: 'Grande', value: 'lg' }
              ]}
              onChange={(value) => setAttributes({ padding: value })}
            />
          </PanelBody>
        </InspectorControls>
        <div className=\"editor-grid\">
          <div className=\"editor-image\">
            <MediaUploadCheck>
              <MediaUpload
                onSelect={(media) => setAttributes({ imageUrl: media.url, imageId: media.id })}
                allowedTypes={['image']}
                render={({ open }) => (
                  <Button onClick={open} variant=\"secondary\">
                    {imageUrl ? 'Cambiar imagen' : 'Seleccionar imagen'}
                  </Button>
                )}
              />
            </MediaUploadCheck>
            {imageUrl && <img src={imageUrl} alt=\"\" style={{ maxWidth: '100%', marginTop: '8px' }} />}
          </div>
          <div className=\"editor-text\">
            <TextControl
              label=\"Título\"
              value={title}
              onChange={(value) => setAttributes({ title: value })}
            />
            <TextareaControl
              label=\"Contenido\"
              value={body}
              onChange={(value) => setAttributes({ body: value })}
            />
          </div>
        </div>
      </div>
    );
  },
  save: () => null
});
"""


def _editor_sidebar() -> str:
    return """import { registerBlockType } from '@wordpress/blocks';
import { InspectorControls, useBlockProps, TextControl } from '@wordpress/block-editor';
import { PanelBody, ToggleControl, Button, SelectControl } from '@wordpress/components';
import { __ } from '@wordpress/i18n';

registerBlockType('img2html/sidebar', {
  edit: ({ attributes, setAttributes }) => {
    const { title, links = [], showRecent, showCategories, showTags, styleVariant, padding, border, linkStyle } = attributes;
    const blockProps = useBlockProps({ className: 'img2html-sidebar-editor' });

    const addLink = () => setAttributes({ links: [...links, { label: 'Nuevo enlace', url: '#' }] });
    const updateLink = (index, field, value) => {
      const newLinks = [...links];
      newLinks[index] = { ...newLinks[index], [field]: value };
      setAttributes({ links: newLinks });
    };
    const removeLink = (index) => setAttributes({ links: links.filter((_, i) => i !== index) });

    return (
      <div {...blockProps}>
        <InspectorControls>
          <PanelBody title={__('Ajustes del Sidebar', 'img2html')} initialOpen={true}>
            <SelectControl
              label={__('Estilo de fondo', 'img2html')}
              value={styleVariant}
              options={[
                { label: 'Claro', value: 'light' },
                { label: 'Oscuro', value: 'dark' }
              ]}
              onChange={(value) => setAttributes({ styleVariant: value })}
            />
            <SelectControl
              label={__('Padding', 'img2html')}
              value={padding}
              options={[
                { label: 'Pequeño', value: 'sm' },
                { label: 'Medio', value: 'md' },
                { label: 'Grande', value: 'lg' }
              ]}
              onChange={(value) => setAttributes({ padding: value })}
            />
            <ToggleControl
              label={__('Borde', 'img2html')}
              checked={border}
              onChange={(value) => setAttributes({ border: value })}
            />
            <SelectControl
              label={__('Estilo de enlaces', 'img2html')}
              value={linkStyle}
              options={[
                { label: 'Normal', value: 'normal' },
                { label: 'Subrayado', value: 'underline' }
              ]}
              onChange={(value) => setAttributes({ linkStyle: value })}
            />
            <ToggleControl
              label={__('Mostrar últimos posts', 'img2html')}
              checked={showRecent}
              onChange={(value) => setAttributes({ showRecent: value })}
            />
            <ToggleControl
              label={__('Mostrar categorías', 'img2html')}
              checked={showCategories}
              onChange={(value) => setAttributes({ showCategories: value })}
            />
            <ToggleControl
              label={__('Mostrar etiquetas', 'img2html')}
              checked={showTags}
              onChange={(value) => setAttributes({ showTags: value })}
            />
          </PanelBody>
        </InspectorControls>

        <TextControl
          label={__('Título', 'img2html')}
          value={title}
          onChange={(value) => setAttributes({ title: value })}
        />

        <div className=\"links-editor\">
          <h4>{__('Enlaces', 'img2html')}</h4>
          {links.map((link, index) => (
            <div key={index} className=\"link-item\">
              <TextControl
                label={__('Texto', 'img2html')}
                value={link.label}
                onChange={(value) => updateLink(index, 'label', value)}
              />
              <TextControl
                label={__('URL', 'img2html')}
                value={link.url}
                onChange={(value) => updateLink(index, 'url', value)}
              />
              <Button variant=\"tertiary\" isDestructive onClick={() => removeLink(index)}>{__('Eliminar', 'img2html')}</Button>
            </div>
          ))}
          <Button variant=\"primary\" onClick={addLink}>{__('Agregar enlace', 'img2html')}</Button>
        </div>
      </div>
    );
  },
  save: () => null
});
"""


def _editor_search() -> str:
    return """import { registerBlockType } from '@wordpress/blocks';
import { InspectorControls, useBlockProps } from '@wordpress/block-editor';
import { PanelBody, SelectControl, ToggleControl, TextControl } from '@wordpress/components';
import { __ } from '@wordpress/i18n';

registerBlockType('img2html/search-extended', {
  edit: ({ attributes, setAttributes }) => {
    const { size, rounded, buttonInside, placeholder, showIcon } = attributes;
    const blockProps = useBlockProps({ className: 'img2html-search-editor' });

    return (
      <div {...blockProps}>
        <InspectorControls>
          <PanelBody title={__('Ajustes del buscador', 'img2html')} initialOpen={true}>
            <SelectControl
              label={__('Tamaño', 'img2html')}
              value={size}
              options={[
                { label: 'Pequeño', value: 'sm' },
                { label: 'Medio', value: 'md' },
                { label: 'Grande', value: 'lg' }
              ]}
              onChange={(value) => setAttributes({ size: value })}
            />
            <ToggleControl
              label={__('Bordes redondeados', 'img2html')}
              checked={rounded}
              onChange={(value) => setAttributes({ rounded: value })}
            />
            <ToggleControl
              label={__('Botón dentro del input', 'img2html')}
              checked={buttonInside}
              onChange={(value) => setAttributes({ buttonInside: value })}
            />
            <ToggleControl
              label={__('Mostrar ícono', 'img2html')}
              checked={showIcon}
              onChange={(value) => setAttributes({ showIcon: value })}
            />
            <TextControl
              label={__('Placeholder', 'img2html')}
              value={placeholder}
              onChange={(value) => setAttributes({ placeholder: value })}
            />
          </PanelBody>
        </InspectorControls>
        <div className=\"preview\">
          <input type=\"text\" placeholder={placeholder} disabled />
        </div>
      </div>
    );
  },
  save: () => null
});
"""


def _editor_pagination() -> str:
    return """import { registerBlockType } from '@wordpress/blocks';
import { InspectorControls, useBlockProps } from '@wordpress/block-editor';
import { PanelBody, SelectControl, ToggleControl, RangeControl } from '@wordpress/components';
import { __ } from '@wordpress/i18n';

registerBlockType('img2html/pagination', {
  edit: ({ attributes, setAttributes }) => {
    const { mode, align, size, gap, showPageCount } = attributes;
    const blockProps = useBlockProps({ className: 'img2html-pagination-editor' });

    return (
      <div {...blockProps}>
        <InspectorControls>
          <PanelBody title={__('Paginación', 'img2html')} initialOpen={true}>
            <SelectControl
              label={__('Tipo', 'img2html')}
              value={mode}
              options={[
                { label: 'Numerada', value: 'numbers' },
                { label: 'Anterior/Siguiente', value: 'prev-next' },
                { label: 'Minimal', value: 'minimal' }
              ]}
              onChange={(value) => setAttributes({ mode: value })}
            />
            <SelectControl
              label={__('Alineación', 'img2html')}
              value={align}
              options={[
                { label: 'Izquierda', value: 'left' },
                { label: 'Centro', value: 'center' },
                { label: 'Derecha', value: 'right' }
              ]}
              onChange={(value) => setAttributes({ align: value })}
            />
            <SelectControl
              label={__('Tamaño', 'img2html')}
              value={size}
              options={[
                { label: 'Small', value: 'sm' },
                { label: 'Normal', value: 'md' },
                { label: 'Large', value: 'lg' }
              ]}
              onChange={(value) => setAttributes({ size: value })}
            />
            <RangeControl
              label={__('Espaciado', 'img2html')}
              value={gap}
              onChange={(value) => setAttributes({ gap: value })}
              min={0}
              max={24}
            />
            <ToggleControl
              label={__('Mostrar cantidad de páginas', 'img2html')}
              checked={showPageCount}
              onChange={(value) => setAttributes({ showPageCount: value })}
            />
          </PanelBody>
        </InspectorControls>
        <div className=\"preview\">{__('Vista previa de paginación', 'img2html')}</div>
      </div>
    );
  },
  save: () => null
});
"""


def _editor_header() -> str:
    return """import { registerBlockType } from '@wordpress/blocks';
import { InspectorControls, useBlockProps, TextControl, ToggleControl } from '@wordpress/block-editor';
import { PanelBody } from '@wordpress/components';
import { __ } from '@wordpress/i18n';

registerBlockType('img2html/header', {
  edit: ({ attributes, setAttributes }) => {
    const { sticky, transparent, scrollChange, height, ctaText, ctaUrl, ctaShow } = attributes;
    const blockProps = useBlockProps({ className: 'img2html-header-editor' });

    return (
      <div {...blockProps}>
        <InspectorControls>
          <PanelBody title={__('Header', 'img2html')} initialOpen={true}>
            <ToggleControl
              label={__('Sticky', 'img2html')}
              checked={sticky}
              onChange={(value) => setAttributes({ sticky: value })}
            />
            <ToggleControl
              label={__('Transparente', 'img2html')}
              checked={transparent}
              onChange={(value) => setAttributes({ transparent: value })}
            />
            <ToggleControl
              label={__('Cambiar color al hacer scroll', 'img2html')}
              checked={scrollChange}
              onChange={(value) => setAttributes({ scrollChange: value })}
            />
            <TextControl
              label={__('CTA Texto', 'img2html')}
              value={ctaText}
              onChange={(value) => setAttributes({ ctaText: value })}
            />
            <TextControl
              label={__('CTA URL', 'img2html')}
              value={ctaUrl}
              onChange={(value) => setAttributes({ ctaUrl: value })}
            />
            <ToggleControl
              label={__('Mostrar CTA', 'img2html')}
              checked={ctaShow}
              onChange={(value) => setAttributes({ ctaShow: value })}
            />
          </PanelBody>
        </InspectorControls>
        <div className=\"preview\">Header editable</div>
      </div>
    );
  },
  save: () => null
});
"""


def _editor_footer() -> str:
    return """import { registerBlockType } from '@wordpress/blocks';
import { InspectorControls, useBlockProps, TextControl, ToggleControl } from '@wordpress/block-editor';
import { PanelBody, RangeControl, SelectControl } from '@wordpress/components';
import { __ } from '@wordpress/i18n';

registerBlockType('img2html/footer', {
  edit: ({ attributes, setAttributes }) => {
    const { columns, bg, legal, showSocial } = attributes;
    const blockProps = useBlockProps({ className: 'img2html-footer-editor' });

    return (
      <div {...blockProps}>
        <InspectorControls>
          <PanelBody title={__('Footer', 'img2html')} initialOpen={true}>
            <RangeControl
              label={__('Columnas', 'img2html')}
              value={columns}
              onChange={(value) => setAttributes({ columns: value })}
              min={1}
              max={4}
            />
            <SelectControl
              label={__('Fondo', 'img2html')}
              value={bg}
              options={[
                { label: 'Oscuro', value: 'dark' },
                { label: 'Claro', value: 'light' }
              ]}
              onChange={(value) => setAttributes({ bg: value })}
            />
            <TextControl
              label={__('Texto legal', 'img2html')}
              value={legal}
              onChange={(value) => setAttributes({ legal: value })}
            />
            <ToggleControl
              label={__('Mostrar redes', 'img2html')}
              checked={showSocial}
              onChange={(value) => setAttributes({ showSocial: value })}
            />
          </PanelBody>
        </InspectorControls>
        <div className=\"preview\">Footer editable</div>
      </div>
    );
  },
  save: () => null
});
"""

def register_blocks_in_functions(theme_dir: str, blocks_dir: str):
    """Registra todos los bloques en functions.php."""
    functions_path = os.path.join(theme_dir, 'functions.php')
    
    # Leer functions.php existente
    functions_content = ""
    if os.path.isfile(functions_path):
        with open(functions_path, 'r', encoding='utf-8') as f:
            functions_content = f.read()
    
    # Agregar registro de bloques si no existe
    if 'register_block_type' not in functions_content or 'img2html' not in functions_content:
        blocks_registration = """
// Registrar bloques personalizados
function img2html_register_blocks() {
    $blocks = [
        'slider',
        'hero',
        'section',
        'cards',
        'gallery',
        'text-image',
        'sidebar',
        'search-extended',
        'pagination',
        'header',
        'footer',
        'form',
        'menu'
    ];
    
    foreach ($blocks as $block) {
        $block_path = get_template_directory() . '/blocks/' . $block;
        if (file_exists($block_path . '/block.json')) {
            register_block_type($block_path);
        }
    }
}
add_action('init', 'img2html_register_blocks');
"""
        # Agregar al final del archivo
        if not functions_content.strip().endswith('?>'):
            functions_content += blocks_registration
        else:
            functions_content = functions_content.rstrip('?>') + blocks_registration + "\n?>"
        
        with open(functions_path, 'w', encoding='utf-8') as f:
            f.write(functions_content)


