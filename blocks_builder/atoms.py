"""
Módulo para crear componentes atómicos (átomos).
Componentes básicos reutilizables: button, heading, input, icon, badge, link.
"""
import os
import json
from typing import Optional
from .helpers import get_bem_prefix, generate_bem_css


def create_atom_button(atoms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Crea el átomo Button - componente básico reutilizable."""
    button_dir = os.path.join(atoms_dir, 'button')
    os.makedirs(button_dir, exist_ok=True)
    
    try:
        from gutenberg_integration import generate_enhanced_block_json, generate_enhanced_attributes
    except ImportError:
        generate_enhanced_block_json = None
        generate_enhanced_attributes = None
    
    base_attributes = {
        "text": {"type": "string", "default": "Click aquí"},
        "url": {"type": "string", "default": "#"},
        "variant": {"type": "string", "default": "primary"},
        "size": {"type": "string", "default": "md"},
        "fullWidth": {"type": "boolean", "default": False}
    }
    
    if generate_enhanced_attributes:
        attributes = generate_enhanced_attributes(base_attributes)
    else:
        attributes = base_attributes
    
    if generate_enhanced_block_json:
        block_json = generate_enhanced_block_json(
            block_name="atom-button",
            title="Botón (Átomo)",
            description="Botón básico reutilizable",
            category="img2html-atoms",
            icon="button",
            attributes=attributes,
            bem_prefix=bem_prefix
        )
    else:
        block_json = {
            "$schema": "https://schemas.wp.org/trunk/block.json",
            "apiVersion": 3,
            "name": f"{bem_prefix}/atom-button",
            "version": "1.0.0",
            "title": "Botón (Átomo)",
            "category": "img2html-atoms",
            "icon": "button",
            "description": "Botón básico reutilizable",
            "textdomain": bem_prefix,
            "render": "file:./render.php",
            "attributes": attributes
        }
    
    with open(os.path.join(button_dir, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2)
    
    render_php = f"""<?php
$text = $attributes['text'] ?? 'Click aquí';
$url = $attributes['url'] ?? '#';
$variant = $attributes['variant'] ?? 'primary';
$size = $attributes['size'] ?? 'md';
$full_width = $attributes['fullWidth'] ?? false;

$variant_class = $variant === 'secondary' ? '{bem_prefix}-atom-button--secondary' : 
                 ($variant === 'outline' ? '{bem_prefix}-atom-button--outline' : '');
$size_class = $size === 'sm' ? '{bem_prefix}-atom-button--small' : 
              ($size === 'lg' ? '{bem_prefix}-atom-button--large' : '');
$width_class = $full_width ? '{bem_prefix}-atom-button--full' : '';
?>
<a href="<?php echo esc_url($url); ?>" 
   class="{bem_prefix}-atom-button <?php echo esc_attr(trim("$variant_class $size_class $width_class")); ?>">
    <?php echo esc_html($text); ?>
</a>
"""
    
    with open(os.path.join(button_dir, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(render_php)
    
    css = generate_bem_css('atom-button', bem_prefix, css_framework, 
                          [('text', '    display: inline-block;')],
                          {'button': ['primary', 'secondary', 'outline', 'small', 'large', 'full']},
                          '    display: inline-block;\n    padding: 0.75rem 1.5rem;\n    border-radius: 0.5rem;\n    text-decoration: none;\n    cursor: pointer;')
    
    with open(os.path.join(button_dir, 'style.css'), 'w', encoding='utf-8') as f:
        f.write(css)


def create_atom_heading(atoms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Crea el átomo Heading - título reutilizable."""
    heading_dir = os.path.join(atoms_dir, 'heading')
    os.makedirs(heading_dir, exist_ok=True)
    
    try:
        from gutenberg_integration import generate_enhanced_block_json, generate_enhanced_attributes
    except ImportError:
        generate_enhanced_block_json = None
        generate_enhanced_attributes = None
    
    base_attributes = {
        "text": {"type": "string", "default": "Título"},
        "level": {"type": "number", "default": 2},
        "align": {"type": "string", "default": "left"}
    }
    
    if generate_enhanced_attributes:
        attributes = generate_enhanced_attributes(base_attributes)
    else:
        attributes = base_attributes
    
    if generate_enhanced_block_json:
        block_json = generate_enhanced_block_json(
            block_name="atom-heading",
            title="Título (Átomo)",
            description="Título básico reutilizable",
            category="img2html-atoms",
            icon="heading",
            attributes=attributes,
            bem_prefix=bem_prefix
        )
    else:
        block_json = {
            "$schema": "https://schemas.wp.org/trunk/block.json",
            "apiVersion": 3,
            "name": f"{bem_prefix}/atom-heading",
            "version": "1.0.0",
            "title": "Título (Átomo)",
            "category": "img2html-atoms",
            "icon": "heading",
            "description": "Título básico reutilizable",
            "textdomain": bem_prefix,
            "render": "file:./render.php",
            "attributes": attributes
        }
    
    with open(os.path.join(heading_dir, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2)
    
    render_php = f"""<?php
$text = $attributes['text'] ?? 'Título';
$level = max(1, min(6, intval($attributes['level'] ?? 2)));
$align = $attributes['align'] ?? 'left';
$tag = "h" . $level;
$align_class = $align === 'center' ? '{bem_prefix}-atom-heading--center' : 
               ($align === 'right' ? '{bem_prefix}-atom-heading--right' : '');
?>
<?php echo "<" . $tag . " class=\\"{bem_prefix}-atom-heading " . esc_attr($align_class) . "\\">"; ?>
    <?php echo esc_html($text); ?>
<?php echo "</" . $tag . ">"; ?>
"""
    
    with open(os.path.join(heading_dir, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(render_php)
    
    css = generate_bem_css('atom-heading', bem_prefix, css_framework,
                          [('text', '    margin: 0;')],
                          {'heading': ['center', 'right']},
                          '    margin: 0;\n    font-weight: 700;')
    
    with open(os.path.join(heading_dir, 'style.css'), 'w', encoding='utf-8') as f:
        f.write(css)


def create_atom_input(atoms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Crea el átomo Input - campo de entrada básico."""
    input_dir = os.path.join(atoms_dir, 'input')
    os.makedirs(input_dir, exist_ok=True)
    
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": f"{bem_prefix}/atom-input",
        "version": "1.0.0",
        "title": "Input (Átomo)",
        "category": "img2html-atoms",
        "icon": "edit",
        "description": "Campo de entrada básico",
        "textdomain": bem_prefix,
        "render": "file:./render.php",
        "attributes": {
            "type": {"type": "string", "default": "text"},
            "placeholder": {"type": "string", "default": ""},
            "name": {"type": "string", "default": ""},
            "required": {"type": "boolean", "default": False}
        }
    }
    
    with open(os.path.join(input_dir, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2)
    
    render_php = f"""<?php
$type = $attributes['type'] ?? 'text';
$placeholder = $attributes['placeholder'] ?? '';
$name = $attributes['name'] ?? '';
$required = $attributes['required'] ?? false;
?>
<input type="<?php echo esc_attr($type); ?>" 
       class="{bem_prefix}-atom-input"
       name="<?php echo esc_attr($name); ?>"
       placeholder="<?php echo esc_attr($placeholder); ?>"
       <?php if ($required): ?>required<?php endif; ?> />
"""
    
    with open(os.path.join(input_dir, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(render_php)
    
    css = generate_bem_css('atom-input', bem_prefix, css_framework,
                          [],
                          {},
                          '    width: 100%;\n    padding: 0.75rem;\n    border: 1px solid #ddd;\n    border-radius: 0.25rem;')
    
    with open(os.path.join(input_dir, 'style.css'), 'w', encoding='utf-8') as f:
        f.write(css)


def create_atom_icon(atoms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Crea el átomo Icon - icono reutilizable."""
    icon_dir = os.path.join(atoms_dir, 'icon')
    os.makedirs(icon_dir, exist_ok=True)
    
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": f"{bem_prefix}/atom-icon",
        "version": "1.0.0",
        "title": "Icono (Átomo)",
        "category": "img2html-atoms",
        "icon": "star-filled",
        "description": "Icono básico reutilizable",
        "textdomain": bem_prefix,
        "render": "file:./render.php",
        "attributes": {
            "name": {"type": "string", "default": "star"},
            "size": {"type": "string", "default": "md"}
        }
    }
    
    with open(os.path.join(icon_dir, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2)
    
    render_php = f"""<?php
$name = $attributes['name'] ?? 'star';
$size = $attributes['size'] ?? 'md';
$size_class = $size === 'sm' ? '{bem_prefix}-atom-icon--small' : 
              ($size === 'lg' ? '{bem_prefix}-atom-icon--large' : '');
?>
<span class="{bem_prefix}-atom-icon <?php echo esc_attr($size_class); ?>" data-icon="<?php echo esc_attr($name); ?>">
    <!-- Icono: <?php echo esc_html($name); ?> -->
</span>
"""
    
    with open(os.path.join(icon_dir, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(render_php)
    
    css = generate_bem_css('atom-icon', bem_prefix, css_framework,
                          [],
                          {'icon': ['small', 'large']},
                          '    display: inline-block;\n    width: 1rem;\n    height: 1rem;')
    
    with open(os.path.join(icon_dir, 'style.css'), 'w', encoding='utf-8') as f:
        f.write(css)


def create_atom_badge(atoms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Crea el átomo Badge - etiqueta reutilizable."""
    badge_dir = os.path.join(atoms_dir, 'badge')
    os.makedirs(badge_dir, exist_ok=True)
    
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": f"{bem_prefix}/atom-badge",
        "version": "1.0.0",
        "title": "Badge (Átomo)",
        "category": "img2html-atoms",
        "icon": "tag",
        "description": "Etiqueta básica reutilizable",
        "textdomain": bem_prefix,
        "render": "file:./render.php",
        "attributes": {
            "text": {"type": "string", "default": "Nuevo"},
            "variant": {"type": "string", "default": "primary"}
        }
    }
    
    with open(os.path.join(badge_dir, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2)
    
    render_php = f"""<?php
$text = $attributes['text'] ?? 'Nuevo';
$variant = $attributes['variant'] ?? 'primary';
$variant_class = $variant === 'success' ? '{bem_prefix}-atom-badge--success' : 
                 ($variant === 'warning' ? '{bem_prefix}-atom-badge--warning' : '');
?>
<span class="{bem_prefix}-atom-badge <?php echo esc_attr($variant_class); ?>">
    <?php echo esc_html($text); ?>
</span>
"""
    
    with open(os.path.join(badge_dir, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(render_php)
    
    css = generate_bem_css('atom-badge', bem_prefix, css_framework,
                          [('text', '    display: inline-block;')],
                          {'badge': ['success', 'warning']},
                          '    display: inline-block;\n    padding: 0.25rem 0.75rem;\n    border-radius: 9999px;\n    font-size: 0.875rem;')
    
    with open(os.path.join(badge_dir, 'style.css'), 'w', encoding='utf-8') as f:
        f.write(css)


def create_atom_link(atoms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Crea el átomo Link - enlace reutilizable."""
    link_dir = os.path.join(atoms_dir, 'link')
    os.makedirs(link_dir, exist_ok=True)
    
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": f"{bem_prefix}/atom-link",
        "version": "1.0.0",
        "title": "Enlace (Átomo)",
        "category": "img2html-atoms",
        "icon": "admin-links",
        "description": "Enlace básico reutilizable",
        "textdomain": bem_prefix,
        "render": "file:./render.php",
        "attributes": {
            "text": {"type": "string", "default": "Enlace"},
            "url": {"type": "string", "default": "#"},
            "target": {"type": "string", "default": "_self"}
        }
    }
    
    with open(os.path.join(link_dir, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2)
    
    render_php = f"""<?php
$text = $attributes['text'] ?? 'Enlace';
$url = $attributes['url'] ?? '#';
$target = $attributes['target'] ?? '_self';
?>
<a href="<?php echo esc_url($url); ?>" 
   target="<?php echo esc_attr($target); ?>"
   class="{bem_prefix}-atom-link">
    <?php echo esc_html($text); ?>
</a>
"""
    
    with open(os.path.join(link_dir, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(render_php)
    
    css = generate_bem_css('atom-link', bem_prefix, css_framework,
                          [],
                          {},
                          '    color: var(--wp--preset--color--primary);\n    text-decoration: none;')
    
    with open(os.path.join(link_dir, 'style.css'), 'w', encoding='utf-8') as f:
        f.write(css)


__all__ = [
    'create_atom_button',
    'create_atom_heading',
    'create_atom_input',
    'create_atom_icon',
    'create_atom_badge',
    'create_atom_link',
]
