"""
Módulo para funciones de editor JavaScript de bloques.
Contiene TODAS las funciones _editor_* y _generate_*_editor_js.
Código completo migrado desde blocks_builder_backup.py
"""


def _generate_slider_editor_js(bem_prefix: str = 'img2html') -> str:
    """Genera el JavaScript del editor para el bloque Slider."""
    return f"""import {{ registerBlockType }} from '@wordpress/blocks';
import {{ 
    InspectorControls, 
    MediaUpload, 
    MediaUploadCheck,
    useBlockProps,
    RichText
}} from '@wordpress/block-editor';
import {{ 
    PanelBody, 
    Button, 
    ToggleControl, 
    RangeControl,
    SelectControl,
    TextControl
}} from '@wordpress/components';
import {{ __ }} from '@wordpress/i18n';
import './editor.css';

registerBlockType('{bem_prefix}/slider', {{
    edit: ({{ attributes, setAttributes }}) => {{
        const {{
            showSlider,
            fullWidth,
            showArrows,
            showDots,
            autoplay,
            autoplaySpeed,
            transitionSpeed,
            height,
            slides = []
        }} = attributes;

        const blockProps = useBlockProps({{
            className: '{bem_prefix}-slider-editor'
        }});

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
                                        placeholder={__('Ej: Título descriptivo del slide', 'img2html')}
                                        help={__('💡 Tip: Sé conciso. Máximo 8-10 palabras.', 'img2html')}
                                    />

                                    <TextControl
                                        label={__('Subtítulo', 'img2html')}
                                        value={slide.subtitle}
                                        onChange={(value) => updateSlide(index, 'subtitle', value)}
                                        placeholder={__('Ej: Descripción complementaria', 'img2html')}
                                        help={__('Complementa el título sin repetir información.', 'img2html')}
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

def _editor_simple_section(bem_prefix: str = 'img2html') -> str:
    return f"""import {{ registerBlockType }} from '@wordpress/blocks';
import {{ InspectorControls, MediaUpload, MediaUploadCheck, useBlockProps, RichText }} from '@wordpress/block-editor';
import {{ PanelBody, SelectControl, Button, TextareaControl, TextControl }} from '@wordpress/components';

registerBlockType('{bem_prefix}/text-image', {{
  edit: ({{ attributes, setAttributes }}) => {{
    const {{ layout, title, body, imageUrl, bgStyle, padding }} = attributes;
    const blockProps = useBlockProps({{ className: '{bem_prefix}-text-image-editor' }});
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

def _editor_sidebar(bem_prefix: str = 'img2html') -> str:
    return f"""import {{ registerBlockType }} from '@wordpress/blocks';
import {{ InspectorControls, useBlockProps, TextControl }} from '@wordpress/block-editor';
import {{ PanelBody, ToggleControl, Button, SelectControl }} from '@wordpress/components';
import {{ __ }} from '@wordpress/i18n';

registerBlockType('{bem_prefix}/sidebar', {{
  edit: ({{ attributes, setAttributes }}) => {{
    const {{ title, links = [], showRecent, showCategories, showTags, styleVariant, padding, border, linkStyle }} = attributes;
    const blockProps = useBlockProps({{ className: '{bem_prefix}-sidebar-editor' }});

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

def _editor_search(bem_prefix: str = 'img2html') -> str:
    return f"""import {{ registerBlockType }} from '@wordpress/blocks';
import {{ InspectorControls, useBlockProps }} from '@wordpress/block-editor';
import {{ PanelBody, SelectControl, ToggleControl, TextControl }} from '@wordpress/components';
import {{ __ }} from '@wordpress/i18n';

registerBlockType('{bem_prefix}/search-extended', {{
  edit: ({{ attributes, setAttributes }}) => {{
    const {{ size, rounded, buttonInside, placeholder, showIcon }} = attributes;
    const blockProps = useBlockProps({{ className: '{bem_prefix}-search-editor' }});

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

def _editor_pagination(bem_prefix: str = 'img2html') -> str:
    return f"""import {{ registerBlockType }} from '@wordpress/blocks';
import {{ InspectorControls, useBlockProps }} from '@wordpress/block-editor';
import {{ PanelBody, SelectControl, ToggleControl, RangeControl }} from '@wordpress/components';
import {{ __ }} from '@wordpress/i18n';

registerBlockType('{bem_prefix}/pagination', {{
  edit: ({{ attributes, setAttributes }}) => {{
    const {{ mode, align, size, gap, showPageCount }} = attributes;
    const blockProps = useBlockProps({{ className: '{bem_prefix}-pagination-editor' }});

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

def _editor_header(bem_prefix: str = 'img2html') -> str:
    return f"""import {{ registerBlockType }} from '@wordpress/blocks';
import {{ InspectorControls, useBlockProps }} from '@wordpress/block-editor';
import {{ PanelBody, ToggleControl, TextControl }} from '@wordpress/components';
import {{ __ }} from '@wordpress/i18n';

registerBlockType('{bem_prefix}/header', {{
  edit: ({{ attributes, setAttributes }}) => {{
    const {{ sticky, transparent, scrollChange, height, ctaText, ctaUrl, ctaShow }} = attributes;
    const blockProps = useBlockProps({{ className: '{bem_prefix}-header-editor' }});

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

def _editor_footer(bem_prefix: str = 'img2html') -> str:
    return f"""import {{ registerBlockType }} from '@wordpress/blocks';
import {{ InspectorControls, useBlockProps }} from '@wordpress/block-editor';
import {{ PanelBody, RangeControl, SelectControl, ToggleControl, TextControl }} from '@wordpress/components';
import {{ __ }} from '@wordpress/i18n';

registerBlockType('{bem_prefix}/footer', {{
  edit: ({{ attributes, setAttributes }}) => {{
    const {{ columns, bg, legal, showSocial }} = attributes;
    const blockProps = useBlockProps({{ className: '{bem_prefix}-footer-editor' }});

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
}});
"""

def _editor_form(bem_prefix: str = 'img2html') -> str:
    return f"""import {{ registerBlockType }} from '@wordpress/blocks';
import {{ InspectorControls, useBlockProps }} from '@wordpress/block-editor';
import {{ PanelBody, ToggleControl, TextControl }} from '@wordpress/components';
import {{ __ }} from '@wordpress/i18n';

registerBlockType('{bem_prefix}/form', {{
  edit: ({{ attributes, setAttributes }}) => {{
    const {{ showPhone, submitText, successMessage, errorMessage }} = attributes;
    const blockProps = useBlockProps({{ className: '{bem_prefix}-form-editor' }});

    return (
      <div {{...blockProps}}>
        <InspectorControls>
          <PanelBody title={{__('Configuración del Formulario', 'img2html')}} initialOpen={{true}}>
            <ToggleControl
              label={{__('Mostrar campo teléfono', 'img2html')}}
              checked={{showPhone}}
              onChange={{(value) => setAttributes({{ showPhone: value }})}}
            />
            <TextControl
              label={{__('Texto del botón', 'img2html')}}
              value={{submitText}}
              onChange={{(value) => setAttributes({{ submitText: value }})}}
            />
            <TextControl
              label={{__('Mensaje de éxito', 'img2html')}}
              value={{successMessage}}
              onChange={{(value) => setAttributes({{ successMessage: value }})}}
            />
            <TextControl
              label={{__('Mensaje de error', 'img2html')}}
              value={{errorMessage}}
              onChange={{(value) => setAttributes({{ errorMessage: value }})}}
            />
          </PanelBody>
        </InspectorControls>
        <div className="preview">Formulario de contacto</div>
      </div>
    );
  }},
  save: () => null
}});
"""

def _editor_menu(bem_prefix: str = 'img2html') -> str:
    return f"""import {{ registerBlockType }} from '@wordpress/blocks';
import {{ InspectorControls, useBlockProps }} from '@wordpress/block-editor';
import {{ PanelBody, ToggleControl, TextControl }} from '@wordpress/components';
import {{ __ }} from '@wordpress/i18n';

registerBlockType('{bem_prefix}/menu', {{
  edit: ({{ attributes, setAttributes }}) => {{
    const {{ sticky, transparent, ctaText, ctaUrl, ctaShow, showSocial }} = attributes;
    const blockProps = useBlockProps({{ className: '{bem_prefix}-menu-editor' }});

    return (
      <div {{...blockProps}}>
        <InspectorControls>
          <PanelBody title={{__('Configuración del Menú', 'img2html')}} initialOpen={{true}}>
            <ToggleControl
              label={{__('Sticky', 'img2html')}}
              checked={{sticky}}
              onChange={{(value) => setAttributes({{ sticky: value }})}}
            />
            <ToggleControl
              label={{__('Transparente', 'img2html')}}
              checked={{transparent}}
              onChange={{(value) => setAttributes({{ transparent: value }})}}
            />
            <TextControl
              label={{__('CTA Texto', 'img2html')}}
              value={{ctaText}}
              onChange={{(value) => setAttributes({{ ctaText: value }})}}
            />
            <TextControl
              label={{__('CTA URL', 'img2html')}}
              value={{ctaUrl}}
              onChange={{(value) => setAttributes({{ ctaUrl: value }})}}
            />
            <ToggleControl
              label={{__('Mostrar CTA', 'img2html')}}
              checked={{ctaShow}}
              onChange={{(value) => setAttributes({{ ctaShow: value }})}}
            />
            <ToggleControl
              label={{__('Mostrar redes sociales', 'img2html')}}
              checked={{showSocial}}
              onChange={{(value) => setAttributes({{ showSocial: value }})}}
            />
          </PanelBody>
        </InspectorControls>
        <div className="preview">Menú navegación</div>
      </div>
    );
  }},
  save: () => null
}});
"""

__all__ = [
    '_generate_slider_editor_js',
    '_editor_simple_section',
    '_editor_sidebar',
    '_editor_search',
    '_editor_pagination',
    '_editor_header',
    '_editor_footer',
    '_editor_form',
    '_editor_menu',
]
