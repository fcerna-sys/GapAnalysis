"""
Módulo para crear componentes atómicos (átomos).
Componentes básicos reutilizables: button, heading, input, icon, badge, link, image.
"""
import os
import json
from typing import Optional
from .helpers import get_bem_prefix, generate_bem_css
from .editor_ux import enhance_block_json_ux
from .prefix_manager import get_prefix_manager


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
        # Usar PrefixManager para asegurar consistencia
        pm = get_prefix_manager(bem_prefix, bem_prefix)
        block_json = {
            "$schema": "https://schemas.wp.org/trunk/block.json",
            "apiVersion": 3,
            "name": pm.get_block_name('atom', 'button'),
            "version": "1.0.0",
            "title": "Botón (Átomo)",
            "category": pm.get_block_category('atoms'),
            "icon": "button",
            "description": "Botón básico reutilizable",
            "textdomain": pm.get_block_textdomain(),
            "render": "file:./render.php",
            "attributes": attributes
        }
    
    # Mejorar UX del editor
    block_json = enhance_block_json_ux(block_json, 'atom', 'button', bem_prefix)
    
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
        # Usar PrefixManager para asegurar consistencia
        pm = get_prefix_manager(bem_prefix, bem_prefix)
        block_json = {
            "$schema": "https://schemas.wp.org/trunk/block.json",
            "apiVersion": 3,
            "name": pm.get_block_name('atom', 'heading'),
            "version": "1.0.0",
            "title": "Título (Átomo)",
            "category": pm.get_block_category('atoms'),
            "icon": "heading",
            "description": "Título básico reutilizable",
            "textdomain": pm.get_block_textdomain(),
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
    # Usar PrefixManager para asegurar consistencia
    pm = get_prefix_manager(bem_prefix, bem_prefix)
    input_dir = os.path.join(atoms_dir, 'input')
    os.makedirs(input_dir, exist_ok=True)
    
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
            "name": pm.get_block_name('atom', 'input'),
        "version": "1.0.0",
        "title": "Input (Átomo)",
            "category": pm.get_block_category('atoms'),
        "icon": "edit",
        "description": "Campo de entrada básico",
            "textdomain": pm.get_block_textdomain(),
        "render": "file:./render.php",
        "attributes": {
            "type": {"type": "string", "default": "text"},
            "placeholder": {"type": "string", "default": ""},
            "name": {"type": "string", "default": ""},
            "required": {"type": "boolean", "default": False}
        }
    }
    
    # Mejorar UX del editor
    block_json = enhance_block_json_ux(block_json, 'atom', 'input', bem_prefix)
    
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
    # Usar PrefixManager para asegurar consistencia
    pm = get_prefix_manager(bem_prefix, bem_prefix)
    icon_dir = os.path.join(atoms_dir, 'icon')
    os.makedirs(icon_dir, exist_ok=True)
    
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": f"{bem_prefix}/atom-icon",
        "version": "1.0.0",
        "title": "Icono (Átomo)",
            "category": pm.get_block_category('atoms'),
        "icon": "star-filled",
        "description": "Icono básico reutilizable",
            "textdomain": pm.get_block_textdomain(),
        "render": "file:./render.php",
        "attributes": {
            "name": {"type": "string", "default": "star"},
            "size": {"type": "string", "default": "md"}
        }
    }
    
    # Mejorar UX del editor
    block_json = enhance_block_json_ux(block_json, 'atom', 'icon', bem_prefix)
    
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
    # Usar PrefixManager para asegurar consistencia
    pm = get_prefix_manager(bem_prefix, bem_prefix)
    badge_dir = os.path.join(atoms_dir, 'badge')
    os.makedirs(badge_dir, exist_ok=True)
    
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": f"{bem_prefix}/atom-badge",
        "version": "1.0.0",
        "title": "Badge (Átomo)",
            "category": pm.get_block_category('atoms'),
        "icon": "tag",
        "description": "Etiqueta básica reutilizable",
            "textdomain": pm.get_block_textdomain(),
        "render": "file:./render.php",
        "attributes": {
            "text": {"type": "string", "default": "Nuevo"},
            "variant": {"type": "string", "default": "primary"}
        }
    }
    
    # Mejorar UX del editor
    block_json = enhance_block_json_ux(block_json, 'atom', 'badge', bem_prefix)
    
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
    # Usar PrefixManager para asegurar consistencia
    pm = get_prefix_manager(bem_prefix, bem_prefix)
    link_dir = os.path.join(atoms_dir, 'link')
    os.makedirs(link_dir, exist_ok=True)
    
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": f"{bem_prefix}/atom-link",
        "version": "1.0.0",
        "title": "Enlace (Átomo)",
            "category": pm.get_block_category('atoms'),
        "icon": "admin-links",
        "description": "Enlace básico reutilizable",
            "textdomain": pm.get_block_textdomain(),
        "render": "file:./render.php",
        "attributes": {
            "text": {"type": "string", "default": "Enlace"},
            "url": {"type": "string", "default": "#"},
            "target": {"type": "string", "default": "_self"}
        }
    }
    
    # Mejorar UX del editor
    block_json = enhance_block_json_ux(block_json, 'atom', 'link', bem_prefix)
    
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


def create_atom_image(atoms_dir: str, css_framework: str, bem_prefix: str = 'img2html'):
    """Crea el átomo Image - imagen reutilizable."""
    # Usar PrefixManager para asegurar consistencia
    pm = get_prefix_manager(bem_prefix, bem_prefix)
    image_dir = os.path.join(atoms_dir, 'image')
    os.makedirs(image_dir, exist_ok=True)
    
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": f"{bem_prefix}/atom-image",
        "version": "1.0.0",
        "title": "Imagen (Átomo)",
            "category": pm.get_block_category('atoms'),
        "icon": "format-image",
        "description": "Imagen básica reutilizable",
            "textdomain": pm.get_block_textdomain(),
        "editorScript": "file:./index.js",
        "style": "file:./style.css",
        "render": "file:./render.php",
        "attributes": {
            "imageUrl": {"type": "string", "default": ""},
            "imageId": {"type": "number", "default": 0},
            "alt": {"type": "string", "default": ""},
            "width": {"type": "string", "default": ""},
            "height": {"type": "string", "default": ""},
            "objectFit": {"type": "string", "default": "cover"},
            "rounded": {"type": "boolean", "default": False}
        },
        "supports": {
            "align": True,
            "html": False,
            "spacing": {
                "margin": True,
                "padding": True
            },
            "dimensions": {
                "aspectRatio": True,
                "minHeight": True
            }
        }
    }
    
    # Mejorar UX del editor
    block_json = enhance_block_json_ux(block_json, 'atom', 'image', bem_prefix)
    
    with open(os.path.join(image_dir, 'block.json'), 'w', encoding='utf-8') as f:
        json.dump(block_json, f, indent=2)
    
    render_php = f"""<?php
$image_url = $attributes['imageUrl'] ?? '';
$image_id = $attributes['imageId'] ?? 0;
$alt = $attributes['alt'] ?? '';
$width = $attributes['width'] ?? '';
$height = $attributes['height'] ?? '';
$object_fit = $attributes['objectFit'] ?? 'cover';
$rounded = $attributes['rounded'] ?? false;

if (!$image_url && $image_id) {{
    $image_url = wp_get_attachment_image_url($image_id, 'full');
    if (!$alt) {{
        $alt = get_post_meta($image_id, '_wp_attachment_image_alt', true);
    }}
}}

if (!$image_url) {{
    return;
}}

$rounded_class = $rounded ? '{bem_prefix}-atom-image--rounded' : '';
$style_attr = '';
if ($width) $style_attr .= 'width: ' . esc_attr($width) . '; ';
if ($height) $style_attr .= 'height: ' . esc_attr($height) . '; ';
if ($object_fit) $style_attr .= 'object-fit: ' . esc_attr($object_fit) . '; ';
?>
<img src="<?php echo esc_url($image_url); ?>" 
     alt="<?php echo esc_attr($alt); ?>"
     class="{bem_prefix}-atom-image <?php echo esc_attr($rounded_class); ?>"
     <?php if ($style_attr): ?>style="<?php echo esc_attr($style_attr); ?>"<?php endif; ?>
     loading="lazy" />
"""
    
    with open(os.path.join(image_dir, 'render.php'), 'w', encoding='utf-8') as f:
        f.write(render_php)
    
    editor_js = f"""import {{ registerBlockType }} from '@wordpress/blocks';
import {{ InspectorControls, useBlockProps, MediaUpload, MediaUploadCheck }} from '@wordpress/block-editor';
import {{ PanelBody, TextControl, ToggleControl, SelectControl, Button }} from '@wordpress/components';
import {{ __ }} from '@wordpress/i18n';

registerBlockType('{bem_prefix}/atom-image', {{
    edit: ({{ attributes, setAttributes }}) => {{
        const {{ imageUrl, imageId, alt, width, height, objectFit, rounded }} = attributes;
        const blockProps = useBlockProps();
        
        const onSelectImage = (media) => {{
            setAttributes({{ 
                imageUrl: media.url, 
                imageId: media.id,
                alt: media.alt || alt
            }});
        }};
        
        return (
            <div {{...blockProps}}>
                <InspectorControls>
                    <PanelBody title={{__('Configuración de Imagen', 'img2html')}}>
                        <MediaUploadCheck>
                            <MediaUpload
                                onSelect={{onSelectImage}}
                                allowedTypes={{"image"}}
                                value={{imageId}}
                                render={{({ open }) => (
                                    <Button onClick={{open}} isSecondary>
                                        {{imageUrl ? __('Cambiar imagen', 'img2html') : __('Seleccionar imagen', 'img2html')}}
                                    </Button>
                                )}}
                            />
                        </MediaUploadCheck>
                        <TextControl
                            label={{__('Texto alternativo', 'img2html')}}
                            value={{alt}}
                            onChange={{(value) => setAttributes({{ alt: value }})}}
                        />
                        <TextControl
                            label={{__('Ancho', 'img2html')}}
                            value={{width}}
                            onChange={{(value) => setAttributes({{ width: value }})}}
                        />
                        <TextControl
                            label={{__('Alto', 'img2html')}}
                            value={{height}}
                            onChange={{(value) => setAttributes({{ height: value }})}}
                        />
                        <SelectControl
                            label={{__('Ajuste de objeto', 'img2html')}}
                            value={{objectFit}}
                            options={{[
                                {{ label: __('Cubrir', 'img2html'), value: 'cover' }},
                                {{ label: __('Contener', 'img2html'), value: 'contain' }},
                                {{ label: __('Rellenar', 'img2html'), value: 'fill' }},
                                {{ label: __('Ninguno', 'img2html'), value: 'none' }}
                            ]}}
                            onChange={{(value) => setAttributes({{ objectFit: value }})}}
                        />
                        <ToggleControl
                            label={{__('Redondeado', 'img2html')}}
                            checked={{rounded}}
                            onChange={{(value) => setAttributes({{ rounded: value }})}}
                        />
                    </PanelBody>
                </InspectorControls>
                <div className="{bem_prefix}-atom-image-editor">
                    {{imageUrl ? (
                        <img src={{imageUrl}} alt={{alt}} style={{{{ maxWidth: '100%', height: 'auto' }}}} />
                    ) : (
                        <p>{{__('Selecciona una imagen', 'img2html')}}</p>
                    )}}
                </div>
            </div>
        );
    }},
    save: () => null
}});
"""
    
    with open(os.path.join(image_dir, 'index.js'), 'w', encoding='utf-8') as f:
        f.write(editor_js)
    
    css = generate_bem_css('atom-image', bem_prefix, css_framework,
                          [],
                          {'image': ['rounded']},
                          '    max-width: 100%;\n    height: auto;\n    display: block;')
    
    with open(os.path.join(image_dir, 'style.css'), 'w', encoding='utf-8') as f:
        f.write(css)


__all__ = [
    'create_atom_button',
    'create_atom_heading',
    'create_atom_input',
    'create_atom_icon',
    'create_atom_badge',
    'create_atom_link',
    'create_atom_image',
]
