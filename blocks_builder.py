# Agregar función para generar editor JS de Hero con controles avanzados
def _generate_hero_editor_js(bem_prefix: str = 'img2html') -> str:
    """Genera index.js para Hero con controles avanzados incluyendo media upload."""
    from gutenberg_integration import generate_editor_js_with_controls
    
    custom_controls = f"""
        <PanelBody title={{__('Hero Settings', '{bem_prefix}')}} initialOpen={{true}}>
            <TextControl
                label={{__('Title', '{bem_prefix}')}}
                value={{attributes.title}}
                onChange={{(value) => setAttributes({{ title: value }})}}
            />
            <TextControl
                label={{__('Subtitle', '{bem_prefix}')}}
                value={{attributes.subtitle}}
                onChange={{(value) => setAttributes({{ subtitle: value }})}}
            />
            <ToggleControl
                label={{__('Show Button', '{bem_prefix}')}}
                checked={{attributes.showButton}}
                onChange={{(value) => setAttributes({{ showButton: value }})}}
            />
            {{attributes.showButton && (
                <>
                    <TextControl
                        label={{__('Button Text', '{bem_prefix}')}}
                        value={{attributes.buttonText}}
                        onChange={{(value) => setAttributes({{ buttonText: value }})}}
                    />
                    <TextControl
                        label={{__('Button URL', '{bem_prefix}')}}
                        value={{attributes.buttonUrl}}
                        onChange={{(value) => setAttributes({{ buttonUrl: value }})}}
                    />
                </>
            )}}
            <ToggleControl
                label={{__('Show Overlay', '{bem_prefix}')}}
                checked={{attributes.showOverlay}}
                onChange={{(value) => setAttributes({{ showOverlay: value }})}}
            />
            <SelectControl
                label={{__('Height', '{bem_prefix}')}}
                value={{attributes.height}}
                options={[
                    {{ label: __('Auto', '{bem_prefix}'), value: 'auto' }},
                    {{ label: __('60vh', '{bem_prefix}'), value: '60vh' }},
                    {{ label: __('70vh', '{bem_prefix}'), value: '70vh' }},
                    {{ label: __('100vh', '{bem_prefix}'), value: '100vh' }},
                ]}
                onChange={{(value) => setAttributes({{ height: value }})}}
            />
            <SelectControl
                label={{__('Text Align', '{bem_prefix}')}}
                value={{attributes.align}}
                options={[
                    {{ label: __('Left', '{bem_prefix}'), value: 'left' }},
                    {{ label: __('Center', '{bem_prefix}'), value: 'center' }},
                    {{ label: __('Right', '{bem_prefix}'), value: 'right' }},
                ]}
                onChange={{(value) => setAttributes({{ align: value }})}}
            />
        </PanelBody>
    """
    
    base_attributes = {
        "title": {"type": "string"},
        "subtitle": {"type": "string"},
        "buttonText": {"type": "string"},
        "buttonUrl": {"type": "string"},
        "showButton": {"type": "boolean"},
        "showOverlay": {"type": "boolean"},
        "height": {"type": "string"},
        "align": {"type": "string"},
        "imageUrl": {"type": "string"},
        "imageId": {"type": "number"},
        "imageWebp": {"type": "string"},
        "imageThumb": {"type": "string"}
    }
    
    return generate_editor_js_with_controls(
        block_name="hero",
        attributes=base_attributes,
        bem_prefix=bem_prefix,
        custom_controls=custom_controls,
        include_media_upload=True
    )

def _generate_hero_editor_css() -> str:
    """Genera CSS para el editor de Hero."""
    return """
.wp-block-img2html-hero-editor {
    min-height: 300px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f0f0f0;
    border: 2px dashed #ccc;
    padding: 2rem;
}
"""
