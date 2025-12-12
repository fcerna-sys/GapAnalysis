# Integración Completa con Gutenberg Block API

## Resumen

Se ha implementado un sistema completo de integración con Gutenberg Block API que permite generar bloques nativos de WordPress con controles avanzados del editor.

## Módulo: `gutenberg_integration.py`

### Funciones Principales

#### 1. `generate_enhanced_block_json()`
Genera un `block.json` completo con soporte para:
- **Color**: background, text, gradients, link
- **Tipografía**: fontSize, lineHeight, fontFamily, fontWeight, fontStyle, etc.
- **Spacing**: margin, padding, blockGap
- **Layout**: constrained, flex, grid
- **Dimensions**: minHeight
- **Position**: sticky

#### 2. `generate_enhanced_attributes()`
Agrega automáticamente atributos de `theme.json`:
- `backgroundColor`, `textColor`, `gradient`
- `fontSize`, `fontFamily`, `fontWeight`, `lineHeight`
- `style.spacing.margin` y `style.spacing.padding`
- `align`

#### 3. `generate_editor_js_with_controls()`
Genera `index.js` completo con:
- **Controles nativos**: PanelColorGradientSettings, PanelBody de Tipografía y Spacing
- **Media Upload**: Integración con MediaUpload de WordPress
- **AlignmentToolbar**: Control de alineación en BlockControls
- **ServerSideRender**: Para bloques dinámicos

#### 4. `generate_render_with_theme_support()`
Mejora `render.php` para:
- Aplicar clases dinámicas según atributos
- Generar estilos inline desde atributos
- Integrar con paleta de colores del tema
- Soporte para tipografías del tema

## Uso

### Ejemplo: Bloque Hero

```python
from gutenberg_integration import (
    generate_enhanced_block_json,
    generate_enhanced_attributes,
    generate_editor_js_with_controls,
    generate_render_with_theme_support
)

# Atributos base
base_attributes = {
    "title": {"type": "string", "default": "Título"},
    "subtitle": {"type": "string", "default": "Subtítulo"},
    "imageUrl": {"type": "string", "default": ""},
    "imageId": {"type": "number", "default": 0}
}

# Agregar atributos de theme.json
attributes = generate_enhanced_attributes(base_attributes)

# Generar block.json
block_json = generate_enhanced_block_json(
    block_name="hero",
    title="Hero",
    description="Bloque Hero",
    category="img2html",
    icon="cover-image",
    attributes=attributes,
    bem_prefix="img2html",
    keywords=["hero", "banner"]
)

# Generar editor JS con controles personalizados
custom_controls = """
    <PanelBody title={__('Hero Settings')} initialOpen={true}>
        <TextControl
            label={__('Title')}
            value={attributes.title}
            onChange={(value) => setAttributes({ title: value })}
        />
    </PanelBody>
"""

editor_js = generate_editor_js_with_controls(
    block_name="hero",
    attributes=attributes,
    bem_prefix="img2html",
    custom_controls=custom_controls,
    include_media_upload=True  # Habilitar media upload
)

# Mejorar render.php
base_render = _render_hero(css_framework, bem_prefix)
enhanced_render = generate_render_with_theme_support(
    base_render, 
    bem_prefix, 
    "hero"
)
```

## Controles Disponibles

### Controles Nativos de Gutenberg

1. **PanelColorGradientSettings**
   - Selector de colores de fondo
   - Selector de colores de texto
   - Gradientes

2. **PanelBody de Tipografía**
   - Font Size (SelectControl)
   - Font Weight (SelectControl)
   - Line Height (RangeControl)

3. **PanelBody de Spacing**
   - Margin Top/Bottom (UnitControl)
   - Padding Top/Bottom/Left/Right (UnitControl)

4. **MediaUpload**
   - Selector de imágenes desde Media Library
   - Preview de imagen seleccionada
   - Botón para eliminar imagen

5. **AlignmentToolbar**
   - Alineación: left, center, right, wide, full

### Controles Personalizados

Cada bloque puede tener controles personalizados:
- `ToggleControl`: Checkboxes
- `TextControl`: Campos de texto
- `SelectControl`: Dropdowns
- `RangeControl`: Sliders numéricos
- `Button`: Botones de acción

## Estructura de Archivos Generados

```
blocks/
  {block-name}/
    block.json          # Configuración completa con supports
    index.js            # Editor con controles nativos
    editor.css          # Estilos del editor
    style.css           # Estilos del frontend
    render.php          # Render con soporte de theme.json
```

## Integración con theme.json

Los bloques generados:
- ✅ Usan colores de la paleta del tema
- ✅ Respetan tipografías definidas en theme.json
- ✅ Aplican espaciados del sistema de spacing
- ✅ Soportan gradientes y colores personalizados
- ✅ Se integran con el sistema de diseño global

## Próximos Pasos

1. **Aplicar a todos los bloques**: Extender la integración a:
   - Hero ✅ (parcialmente implementado)
   - Section
   - Cards
   - Gallery
   - Text+Image
   - Header
   - Footer
   - Form
   - Menu
   - Sidebar
   - Search
   - Pagination

2. **Controles Avanzados**:
   - Repeater fields para arrays
   - Validación de atributos
   - Preview mejorado en el editor
   - Placeholders amigables

3. **Validación**:
   - Validar URLs
   - Validar rangos numéricos
   - Validar formatos de email

4. **Preview Mejorado**:
   - Vista previa en tiempo real
   - Placeholders con contenido de ejemplo
   - Indicadores visuales de estado

## Ejemplo de block.json Generado

```json
{
  "$schema": "https://schemas.wp.org/trunk/block.json",
  "apiVersion": 3,
  "name": "img2html/hero",
  "supports": {
    "align": ["wide", "full"],
    "spacing": {
      "margin": true,
      "padding": true,
      "blockGap": true
    },
    "color": {
      "background": true,
      "text": true,
      "gradients": true
    },
    "typography": {
      "fontSize": true,
      "lineHeight": true,
      "fontFamily": true,
      "fontWeight": true
    },
    "layout": {
      "default": {
        "type": "constrained"
      }
    }
  },
  "attributes": {
    "title": {"type": "string"},
    "backgroundColor": {"type": "string"},
    "textColor": {"type": "string"},
    "fontSize": {"type": "string"},
    "style": {
      "type": "object",
      "default": {
        "spacing": {
          "margin": {"top": null, "bottom": null},
          "padding": {"top": null, "bottom": null}
        }
      }
    }
  }
}
```

## Beneficios

- ✅ **Bloques nativos**: Integración completa con Gutenberg
- ✅ **Controles visuales**: Edición desde el panel derecho
- ✅ **Consistencia**: Uso de valores de theme.json
- ✅ **Flexibilidad**: Atributos dinámicos configurables
- ✅ **Experiencia mejorada**: Controles familiares para usuarios de WordPress


