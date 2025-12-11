"""
Integración completa con Gutenberg Block API.
Genera bloques con controles nativos del editor (color, tipografía, spacing, layout).
"""
import json
from typing import Dict, List, Optional


def generate_enhanced_block_json(
    block_name: str,
    title: str,
    description: str,
    category: str,
    icon: str,
    attributes: Dict,
    bem_prefix: str = 'img2html',
    supports: Optional[Dict] = None,
    keywords: Optional[List[str]] = None
) -> Dict:
    """
    Genera un block.json completo con soporte para controles nativos de Gutenberg.
    """
    default_supports = {
        "align": ["wide", "full"],
        "html": False,
        "spacing": {
            "margin": True,
            "padding": True,
            "blockGap": True
        },
        "color": {
            "background": True,
            "text": True,
            "gradients": True,
            "link": True
        },
        "typography": {
            "fontSize": True,
            "lineHeight": True,
            "fontFamily": True,
            "fontWeight": True,
            "fontStyle": True,
            "textTransform": True,
            "textDecoration": True,
            "letterSpacing": True
        },
        "layout": {
            "allowSwitching": False,
            "allowInheriting": False,
            "default": {
                "type": "constrained"
            }
        },
        "dimensions": {
            "minHeight": True
        },
        "position": {
            "sticky": True
        }
    }
    
    if supports:
        default_supports.update(supports)
    
    block_json = {
        "$schema": "https://schemas.wp.org/trunk/block.json",
        "apiVersion": 3,
        "name": f"{bem_prefix}/{block_name}",
        "version": "1.0.0",
        "title": title,
        "category": category,
        "icon": icon,
        "description": description,
        "keywords": keywords or [],
        "textdomain": bem_prefix,
        "editorScript": "file:./index.js",
        "editorStyle": "file:./editor.css",
        "style": "file:./style.css",
        "render": "file:./render.php",
        "supports": default_supports,
        "attributes": attributes,
        "example": {
            "attributes": {}
        }
    }
    
    return block_json


def generate_editor_js_with_controls(
    block_name: str,
    attributes: Dict,
    bem_prefix: str = 'img2html',
    custom_controls: Optional[str] = None,
    include_media_upload: bool = False
) -> str:
    """
    Genera index.js completo con controles nativos de Gutenberg.
    """
    block_name_full = f"{bem_prefix}/{block_name}"
    
    # Generar imports de controles
    imports = """import { registerBlockType } from '@wordpress/blocks';
import { 
    InspectorControls,
    useBlockProps,
    BlockControls,
    AlignmentToolbar,
    PanelColorSettings,
    __experimentalPanelColorGradientSettings as PanelColorGradientSettings,
    __experimentalUseMultipleOriginColorsAndGradients as useMultipleOriginColorsAndGradients
} from '@wordpress/block-editor';
import {
    PanelBody,
    ToggleControl,
    RangeControl,
    SelectControl,
    TextControl,
    Button,
    __experimentalUnitControl as UnitControl,
    __experimentalSpacingSizesControl as SpacingSizesControl
} from '@wordpress/components';
import { __ } from '@wordpress/i18n';
import ServerSideRender from '@wordpress/server-side-render';
"""
    
    # Generar atributos dinámicos desde theme.json
    theme_attributes = """
    // Atributos de theme.json (colores, tipografías, spacing)
    const colors = useMultipleOriginColorsAndGradients();
    const blockProps = useBlockProps({
        className: classnames('{bem_prefix}-{block_name}', {
            'has-background': attributes.backgroundColor || attributes.gradient,
            'has-text-color': attributes.textColor,
        }),
        style: {
            backgroundColor: attributes.backgroundColor,
            color: attributes.textColor,
            fontSize: attributes.fontSize,
            fontFamily: attributes.fontFamily,
            fontWeight: attributes.fontWeight,
            lineHeight: attributes.lineHeight,
            marginTop: attributes.style?.spacing?.margin?.top,
            marginBottom: attributes.style?.spacing?.margin?.bottom,
            paddingTop: attributes.style?.spacing?.padding?.top,
            paddingBottom: attributes.style?.spacing?.padding?.bottom,
            paddingLeft: attributes.style?.spacing?.padding?.left,
            paddingRight: attributes.style?.spacing?.padding?.right,
        }
    });
"""
    
    # Generar controles del inspector
    inspector_controls = f"""
    <InspectorControls>
        {/* Panel de Color */}
        <PanelColorGradientSettings
            title={__('Color Settings', '{bem_prefix}')}
            settings={[
                {{
                    colorValue: attributes.backgroundColor,
                    label: __('Background Color', '{bem_prefix}'),
                    onChange: (value) => setAttributes({{ backgroundColor: value }}),
                }},
                {{
                    colorValue: attributes.textColor,
                    label: __('Text Color', '{bem_prefix}'),
                    onChange: (value) => setAttributes({{ textColor: value }}),
                }},
            ]}
            {...colors}
        />
        
        {/* Panel de Tipografía */}
        <PanelBody title={__('Typography', '{bem_prefix}')} initialOpen={false}>
            <SelectControl
                label={__('Font Size', '{bem_prefix}')}
                value={attributes.fontSize}
                options={[
                    {{ label: __('Default', '{bem_prefix}'), value: '' }},
                    {{ label: __('Small', '{bem_prefix}'), value: 'small' }},
                    {{ label: __('Medium', '{bem_prefix}'), value: 'medium' }},
                    {{ label: __('Large', '{bem_prefix}'), value: 'large' }},
                    {{ label: __('Extra Large', '{bem_prefix}'), value: 'xlarge' }},
                ]}
                onChange={(value) => setAttributes({{ fontSize: value }})}
            />
            <SelectControl
                label={__('Font Weight', '{bem_prefix}')}
                value={attributes.fontWeight}
                options={[
                    {{ label: __('Default', '{bem_prefix}'), value: '' }},
                    {{ label: __('Normal', '{bem_prefix}'), value: 'normal' }},
                    {{ label: __('Bold', '{bem_prefix}'), value: 'bold' }},
                ]}
                onChange={(value) => setAttributes({{ fontWeight: value }})}
            />
            <RangeControl
                label={__('Line Height', '{bem_prefix}')}
                value={attributes.lineHeight}
                onChange={(value) => setAttributes({{ lineHeight: value }})}
                min={1}
                max={3}
                step={0.1}
            />
        </PanelBody>
        
        {/* Panel de Spacing */}
        <PanelBody title={__('Spacing', '{bem_prefix}')} initialOpen={false}>
            <UnitControl
                label={__('Margin Top', '{bem_prefix}')}
                value={attributes.style?.spacing?.margin?.top}
                onChange={(value) => setAttributes({{
                    style: {{
                        ...attributes.style,
                        spacing: {{
                            ...attributes.style?.spacing,
                            margin: {{
                                ...attributes.style?.spacing?.margin,
                                top: value
                            }}
                        }}
                    }}
                }})}
            />
            <UnitControl
                label={__('Margin Bottom', '{bem_prefix}')}
                value={attributes.style?.spacing?.margin?.bottom}
                onChange={(value) => setAttributes({{
                    style: {{
                        ...attributes.style,
                        spacing: {{
                            ...attributes.style?.spacing,
                            margin: {{
                                ...attributes.style?.spacing?.margin,
                                bottom: value
                            }}
                        }}
                    }}
                }})}
            />
            <UnitControl
                label={__('Padding Top', '{bem_prefix}')}
                value={attributes.style?.spacing?.padding?.top}
                onChange={(value) => setAttributes({{
                    style: {{
                        ...attributes.style,
                        spacing: {{
                            ...attributes.style?.spacing,
                            padding: {{
                                ...attributes.style?.spacing?.padding,
                                top: value
                            }}
                        }}
                    }}
                }})}
            />
            <UnitControl
                label={__('Padding Bottom', '{bem_prefix}')}
                value={attributes.style?.spacing?.padding?.bottom}
                onChange={(value) => setAttributes({{
                    style: {{
                        ...attributes.style,
                        spacing: {{
                            ...attributes.style?.spacing,
                            padding: {{
                                ...attributes.style?.spacing?.padding,
                                bottom: value
                            }}
                        }}
                    }}
                }})}
            />
        </PanelBody>
        
        {/* Controles personalizados del bloque */}
        {custom_controls or ''}
        
        {/* Media Upload si está habilitado */}
        {include_media_upload && (
            <PanelBody title={__('Media', '{bem_prefix}')} initialOpen={false}>
                <MediaUploadCheck>
                    <MediaUpload
                        onSelect={(media) => {{
                            setAttributes({{
                                imageId: media.id,
                                imageUrl: media.url,
                                imageWebp: media.url,
                                imageThumb: media.sizes?.thumbnail?.url || media.url
                            }});
                        }}}
                        allowedTypes={{['image']}}
                        value={{attributes.imageId}}
                        render={{({{ open }}) => (
                            <Button onClick={{open}} isSecondary>
                                {{attributes.imageId ? __('Cambiar imagen', '{bem_prefix}') : __('Seleccionar imagen', '{bem_prefix}')}}
                            </Button>
                        )}}
                    />
                    {{attributes.imageUrl && (
                        <div style={{{{ marginTop: '10px' }}}}>
                            <img src={{attributes.imageUrl}} alt="" style={{{{ maxWidth: '100%', height: 'auto' }}}} />
                            <Button onClick={{() => setAttributes({{ imageId: 0, imageUrl: '', imageWebp: '', imageThumb: '' }})}} isDestructive isSmall style={{{{ marginTop: '10px' }}}}>
                                {{__('Eliminar imagen', '{bem_prefix}')}}
                            </Button>
                        </div>
                    )}}
                </MediaUploadCheck>
            </PanelBody>
        )}
    </InspectorControls>
"""
    
    # Generar edit component
    edit_component = f"""
registerBlockType('{block_name_full}', {{
    edit: ({{
        attributes,
        setAttributes,
        isSelected
    }}) => {{
        const blockProps = useBlockProps({{
            className: '{bem_prefix}-{block_name}-editor',
        }});
        
        return (
            <>
                <BlockControls>
                    <AlignmentToolbar
                        value={attributes.align}
                        onChange={(value) => setAttributes({{ align: value }})}
                    />
                </BlockControls>
                
                {inspector_controls}
                
                <div {{...blockProps}}>
                    <ServerSideRender
                        block="{block_name_full}"
                        attributes={{attributes}}
                    />
                </div>
            </>
        );
    }},
    
    save: () => null // Dynamic block, rendered server-side
}});
"""
    
    return imports + edit_component


def generate_enhanced_attributes(base_attributes: Dict) -> Dict:
    """
    Agrega atributos de theme.json a los atributos base del bloque.
    """
    enhanced = base_attributes.copy()
    
    # Atributos de color
    enhanced['backgroundColor'] = {
        "type": "string"
    }
    enhanced['textColor'] = {
        "type": "string"
    }
    enhanced['gradient'] = {
        "type": "string"
    }
    
    # Atributos de tipografía
    enhanced['fontSize'] = {
        "type": "string"
    }
    enhanced['fontFamily'] = {
        "type": "string"
    }
    enhanced['fontWeight'] = {
        "type": "string"
    }
    enhanced['lineHeight'] = {
        "type": "number"
    }
    
    # Atributos de spacing
    enhanced['style'] = {
        "type": "object",
        "default": {
            "spacing": {
                "margin": {
                    "top": None,
                    "bottom": None,
                    "left": None,
                    "right": None
                },
                "padding": {
                    "top": None,
                    "bottom": None,
                    "left": None,
                    "right": None
                }
            }
        }
    }
    
    # Atributos de layout
    enhanced['align'] = {
        "type": "string",
        "default": ""
    }
    
    return enhanced


def generate_render_with_theme_support(
    base_render: str,
    bem_prefix: str,
    block_name: str
) -> str:
    """
    Mejora el render.php para usar atributos de theme.json.
    """
    # Agregar clases y estilos dinámicos
    theme_support = f"""
// Atributos de theme.json
$block_classes = ['{bem_prefix}-{block_name}'];
$block_styles = [];

// Colores
if (!empty($attributes['backgroundColor'])) {{
    $block_classes[] = 'has-background';
    $block_classes[] = 'has-' . esc_attr($attributes['backgroundColor']) . '-background-color';
    $block_styles[] = 'background-color: var(--wp--preset--color--' . esc_attr($attributes['backgroundColor']) . ');';
}}
if (!empty($attributes['textColor'])) {{
    $block_classes[] = 'has-text-color';
    $block_classes[] = 'has-' . esc_attr($attributes['textColor']) . '-color';
    $block_styles[] = 'color: var(--wp--preset--color--' . esc_attr($attributes['textColor']) . ');';
}}

// Tipografía
if (!empty($attributes['fontSize'])) {{
    $block_classes[] = 'has-' . esc_attr($attributes['fontSize']) . '-font-size';
}}
if (!empty($attributes['fontFamily'])) {{
    $block_styles[] = 'font-family: var(--wp--preset--font-family--' . esc_attr($attributes['fontFamily']) . ');';
}}
if (!empty($attributes['fontWeight'])) {{
    $block_styles[] = 'font-weight: ' . esc_attr($attributes['fontWeight']) . ';';
}}
if (!empty($attributes['lineHeight'])) {{
    $block_styles[] = 'line-height: ' . esc_attr($attributes['lineHeight']) . ';';
}}

// Spacing
if (!empty($attributes['style']['spacing']['margin']['top'])) {{
    $block_styles[] = 'margin-top: ' . esc_attr($attributes['style']['spacing']['margin']['top']) . ';';
}}
if (!empty($attributes['style']['spacing']['margin']['bottom'])) {{
    $block_styles[] = 'margin-bottom: ' . esc_attr($attributes['style']['spacing']['margin']['bottom']) . ';';
}}
if (!empty($attributes['style']['spacing']['padding']['top'])) {{
    $block_styles[] = 'padding-top: ' . esc_attr($attributes['style']['spacing']['padding']['top']) . ';';
}}
if (!empty($attributes['style']['spacing']['padding']['bottom'])) {{
    $block_styles[] = 'padding-bottom: ' . esc_attr($attributes['style']['spacing']['padding']['bottom']) . ';';
}}
if (!empty($attributes['style']['spacing']['padding']['left'])) {{
    $block_styles[] = 'padding-left: ' . esc_attr($attributes['style']['spacing']['padding']['left']) . ';';
}}
if (!empty($attributes['style']['spacing']['padding']['right'])) {{
    $block_styles[] = 'padding-right: ' . esc_attr($attributes['style']['spacing']['padding']['right']) . ';';
}}

$wrapper_attrs = '';
if (!empty($block_classes)) {{
    $wrapper_attrs .= ' class="' . esc_attr(implode(' ', $block_classes)) . '"';
}}
if (!empty($block_styles)) {{
    $wrapper_attrs .= ' style="' . esc_attr(implode(' ', $block_styles)) . '"';
}}
"""
    
    # Insertar al inicio del render
    return theme_support + "\n" + base_render.replace('<?php', '').replace('<?php', theme_support, 1)

