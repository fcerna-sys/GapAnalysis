"""
Módulo para crear componentes moleculares.
Combinaciones de átomos: card, form-field, nav-item, testimonial, pricing-item.
"""
import os
import json
from typing import Optional
from .helpers import get_bem_prefix, generate_bem_css
from .editor_ux import enhance_block_json_ux


def create_molecule_card(molecules_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Crea la molécula Card - combina heading, texto, button."""
    card_dir = os.path.join(molecules_dir, 'card')
    os.makedirs(card_dir, exist_ok=True)
    
    try:
        from gutenberg_integration import generate_enhanced_block_json, generate_enhanced_attributes
    except ImportError:
        generate_enhanced_block_json = None
        generate_enhanced_attributes = None
    
    base_attributes = {
        "title": {"type": "string", "default": "Título"},
        "text": {"type": "string", "default": "Descripción"},
        "imageUrl": {"type": "string", "default": ""},
        "imageId": {"type": "number", "default": 0},
        "buttonText": {"type": "string", "default": ""},
        "buttonUrl": {"type": "string", "default": "#"}
    }
    
    if generate_enhanced_attributes:
        attributes = generate_enhanced_attributes(base_attributes)
    else:
        attributes = base_attributes
    
    if generate_enhanced_block_json:
        block_json = generate_enhanced_block_json(
            block_name="molecule-card",
            title="Tarjeta (Molécula)",
            description="Tarjeta que combina átomos",
            category="img2html-molecules",
            icon="index-card",
            attributes=attributes,
            bem_prefix=bem_prefix
        )
    else:
        block_json = {
            "$schema": "https://schemas.wp.org/trunk/block.json",
            "apiVersion": 3,
            "name": f"{bem_prefix}/molecule-card",
            "version": "1.0.0",
            "title": "Tarjeta (Molécula)",
            "category": "img2html-molecules",
            "icon": "index-card",
            "description": "Tarjeta que combina átomos",
            "textdomain": bem_prefix,
            "render": "file:./render.php",
            "attributes": attributes
        }
    
    # Mejorar UX del editor
    block_json = enhance_block_json_ux(block_json, 'molecule', 'card', bem_prefix)
    
    with open(os.path.join(card_dir, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2)
    
    render_php = f"""<?php
$title = $attributes['title'] ?? 'Título';
$text = $attributes['text'] ?? 'Descripción';
$image = $attributes['imageUrl'] ?? '';
$btn_text = $attributes['buttonText'] ?? '';
$btn_url = $attributes['buttonUrl'] ?? '#';
?>
<div class="{bem_prefix}-molecule-card">
    <?php if ($image): ?>
        <div class="{bem_prefix}-molecule-card__image">
            <img src="<?php echo esc_url($image); ?>" alt="<?php echo esc_attr($title); ?>" loading="lazy" />
        </div>
    <?php endif; ?>
    <div class="{bem_prefix}-molecule-card__content">
        <h3 class="{bem_prefix}-molecule-card__title"><?php echo esc_html($title); ?></h3>
        <p class="{bem_prefix}-molecule-card__text"><?php echo esc_html($text); ?></p>
        <?php if ($btn_text): ?>
            <a href="<?php echo esc_url($btn_url); ?>" class="{bem_prefix}-atom-button">
                <?php echo esc_html($btn_text); ?>
            </a>
        <?php endif; ?>
    </div>
</div>
"""
    
    with open(os.path.join(card_dir, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(render_php)
    
    css = generate_bem_css('molecule-card', bem_prefix, css_framework,
                          [('image', '    width: 100%;'), ('content', '    padding: 1.5rem;'), ('title', '    margin-bottom: 0.75rem;'), ('text', '    margin-bottom: 1rem;')],
                          {},
                          '    background: #fff;\n    border-radius: 0.5rem;\n    overflow: hidden;\n    box-shadow: 0 1px 3px rgba(0,0,0,0.1);')
    
    with open(os.path.join(card_dir, 'style.css'), 'w', encoding='utf-8') as f:
        f.write(css)


def create_molecule_form_field(molecules_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Crea la molécula FormField - combina label + input."""
    formfield_dir = os.path.join(molecules_dir, 'form-field')
    os.makedirs(formfield_dir, exist_ok=True)
    
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": f"{bem_prefix}/molecule-form-field",
        "version": "1.0.0",
        "title": "Campo de Formulario (Molécula)",
        "category": "img2html-molecules",
        "icon": "forms",
        "description": "Campo de formulario con label",
        "textdomain": bem_prefix,
        "render": "file:./render.php",
        "attributes": {
            "label": {"type": "string", "default": "Etiqueta"},
            "type": {"type": "string", "default": "text"},
            "name": {"type": "string", "default": ""},
            "placeholder": {"type": "string", "default": ""},
            "required": {"type": "boolean", "default": False}
        }
    }
    
    with open(os.path.join(formfield_dir, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2)
    
    render_php = f"""<?php
$label = $attributes['label'] ?? 'Etiqueta';
$type = $attributes['type'] ?? 'text';
$name = $attributes['name'] ?? '';
$placeholder = $attributes['placeholder'] ?? '';
$required = $attributes['required'] ?? false;
?>
<div class="{bem_prefix}-molecule-form-field">
    <label class="{bem_prefix}-molecule-form-field__label">
        <?php echo esc_html($label); ?>
        <?php if ($required): ?><span class="{bem_prefix}-molecule-form-field__required">*</span><?php endif; ?>
    </label>
    <input type="<?php echo esc_attr($type); ?>" 
           class="{bem_prefix}-atom-input"
           name="<?php echo esc_attr($name); ?>"
           placeholder="<?php echo esc_attr($placeholder); ?>"
           <?php if ($required): ?>required<?php endif; ?> />
</div>
"""
    
    with open(os.path.join(formfield_dir, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(render_php)
    
    css = generate_bem_css('molecule-form-field', bem_prefix, css_framework,
                          [('label', '    display: block;\n    margin-bottom: 0.5rem;'), ('required', '    color: #ef4444;')],
                          {},
                          '    margin-bottom: 1rem;')
    
    with open(os.path.join(formfield_dir, 'style.css'), 'w', encoding='utf-8') as f:
        f.write(css)


def create_molecule_nav_item(molecules_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Crea la molécula NavItem - combina link + icon opcional."""
    navitem_dir = os.path.join(molecules_dir, 'nav-item')
    os.makedirs(navitem_dir, exist_ok=True)
    
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": f"{bem_prefix}/molecule-nav-item",
        "version": "1.0.0",
        "title": "Item de Navegación (Molécula)",
        "category": "img2html-molecules",
        "icon": "admin-links",
        "description": "Item de menú con enlace",
        "textdomain": bem_prefix,
        "render": "file:./render.php",
        "attributes": {
            "text": {"type": "string", "default": "Enlace"},
            "url": {"type": "string", "default": "#"},
            "icon": {"type": "string", "default": ""}
        }
    }
    
    with open(os.path.join(navitem_dir, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2)
    
    render_php = f"""<?php
$text = $attributes['text'] ?? 'Enlace';
$url = $attributes['url'] ?? '#';
$icon = $attributes['icon'] ?? '';
?>
<li class="{bem_prefix}-molecule-nav-item">
    <a href="<?php echo esc_url($url); ?>" class="{bem_prefix}-atom-link">
        <?php if ($icon): ?>
            <span class="{bem_prefix}-atom-icon" data-icon="<?php echo esc_attr($icon); ?>"></span>
        <?php endif; ?>
        <?php echo esc_html($text); ?>
    </a>
</li>
"""
    
    with open(os.path.join(navitem_dir, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(render_php)
    
    css = generate_bem_css('molecule-nav-item', bem_prefix, css_framework,
                          [],
                          {},
                          '    list-style: none;')
    
    with open(os.path.join(navitem_dir, 'style.css'), 'w', encoding='utf-8') as f:
        f.write(css)


def create_molecule_testimonial(molecules_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Crea la molécula Testimonial - combina texto + autor."""
    testimonial_dir = os.path.join(molecules_dir, 'testimonial')
    os.makedirs(testimonial_dir, exist_ok=True)
    
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": f"{bem_prefix}/molecule-testimonial",
        "version": "1.0.0",
        "title": "Testimonio (Molécula)",
        "category": "img2html-molecules",
        "icon": "format-quote",
        "description": "Testimonio con cita y autor",
        "textdomain": bem_prefix,
        "render": "file:./render.php",
        "attributes": {
            "quote": {"type": "string", "default": "Excelente servicio"},
            "author": {"type": "string", "default": "Cliente"},
            "role": {"type": "string", "default": ""},
            "imageUrl": {"type": "string", "default": ""}
        }
    }
    
    with open(os.path.join(testimonial_dir, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2)
    
    render_php = f"""<?php
$quote = $attributes['quote'] ?? 'Excelente servicio';
$author = $attributes['author'] ?? 'Cliente';
$role = $attributes['role'] ?? '';
$image = $attributes['imageUrl'] ?? '';
?>
<div class="{bem_prefix}-molecule-testimonial">
    <blockquote class="{bem_prefix}-molecule-testimonial__quote">
        <?php echo esc_html($quote); ?>
    </blockquote>
    <div class="{bem_prefix}-molecule-testimonial__author">
        <?php if ($image): ?>
            <img src="<?php echo esc_url($image); ?>" alt="<?php echo esc_attr($author); ?>" class="{bem_prefix}-molecule-testimonial__avatar" loading="lazy" />
        <?php endif; ?>
        <div>
            <cite class="{bem_prefix}-molecule-testimonial__name"><?php echo esc_html($author); ?></cite>
            <?php if ($role): ?>
                <span class="{bem_prefix}-molecule-testimonial__role"><?php echo esc_html($role); ?></span>
            <?php endif; ?>
        </div>
    </div>
</div>
"""
    
    with open(os.path.join(testimonial_dir, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(render_php)
    
    css = generate_bem_css('molecule-testimonial', bem_prefix, css_framework,
                          [('quote', '    margin-bottom: 1rem;'), ('author', '    display: flex;\n    align-items: center;\n    gap: 1rem;'), ('avatar', '    width: 48px;\n    height: 48px;\n    border-radius: 50%;')],
                          {},
                          '    padding: 1.5rem;\n    background: #f9fafb;\n    border-radius: 0.5rem;')
    
    with open(os.path.join(testimonial_dir, 'style.css'), 'w', encoding='utf-8') as f:
        f.write(css)


def create_molecule_pricing_item(molecules_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Crea la molécula PricingItem - combina precio + features + button."""
    pricing_dir = os.path.join(molecules_dir, 'pricing-item')
    os.makedirs(pricing_dir, exist_ok=True)
    
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": f"{bem_prefix}/molecule-pricing-item",
        "version": "1.0.0",
        "title": "Item de Precio (Molécula)",
        "category": "img2html-molecules",
        "icon": "money-alt",
        "description": "Item de precio con características",
        "textdomain": bem_prefix,
        "render": "file:./render.php",
        "attributes": {
            "title": {"type": "string", "default": "Plan"},
            "price": {"type": "string", "default": "$0"},
            "period": {"type": "string", "default": "/mes"},
            "features": {"type": "array", "default": []},
            "buttonText": {"type": "string", "default": "Seleccionar"},
            "buttonUrl": {"type": "string", "default": "#"},
            "featured": {"type": "boolean", "default": False}
        }
    }
    
    with open(os.path.join(pricing_dir, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2)
    
    render_php = f"""<?php
$title = $attributes['title'] ?? 'Plan';
$price = $attributes['price'] ?? '$0';
$period = $attributes['period'] ?? '/mes';
$features = $attributes['features'] ?? [];
$btn_text = $attributes['buttonText'] ?? 'Seleccionar';
$btn_url = $attributes['buttonUrl'] ?? '#';
$featured = $attributes['featured'] ?? false;
$featured_class = $featured ? '{bem_prefix}-molecule-pricing-item--featured' : '';
?>
<div class="{bem_prefix}-molecule-pricing-item <?php echo esc_attr($featured_class); ?>">
    <h3 class="{bem_prefix}-molecule-pricing-item__title"><?php echo esc_html($title); ?></h3>
    <div class="{bem_prefix}-molecule-pricing-item__price">
        <span class="{bem_prefix}-molecule-pricing-item__amount"><?php echo esc_html($price); ?></span>
        <span class="{bem_prefix}-molecule-pricing-item__period"><?php echo esc_html($period); ?></span>
    </div>
    <?php if (!empty($features)): ?>
        <ul class="{bem_prefix}-molecule-pricing-item__features">
            <?php foreach ($features as $feature): ?>
                <li><?php echo esc_html($feature); ?></li>
            <?php endforeach; ?>
        </ul>
    <?php endif; ?>
    <a href="<?php echo esc_url($btn_url); ?>" class="{bem_prefix}-atom-button">
        <?php echo esc_html($btn_text); ?>
    </a>
</div>
"""
    
    with open(os.path.join(pricing_dir, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(render_php)
    
    css = generate_bem_css('molecule-pricing-item', bem_prefix, css_framework,
                          [('title', '    margin-bottom: 1rem;'), ('price', '    margin-bottom: 1.5rem;'), ('features', '    list-style: none;\n    padding: 0;\n    margin-bottom: 1.5rem;')],
                          {'pricing-item': ['featured']},
                          '    padding: 2rem;\n    background: #fff;\n    border-radius: 0.5rem;\n    text-align: center;')
    
    with open(os.path.join(pricing_dir, 'style.css'), 'w', encoding='utf-8') as f:
        f.write(css)


__all__ = [
    'create_molecule_card',
    'create_molecule_form_field',
    'create_molecule_nav_item',
    'create_molecule_testimonial',
    'create_molecule_pricing_item',
]
