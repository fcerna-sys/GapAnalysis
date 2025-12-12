"""
Sistema de generación de documentación automática para bloques y patterns.
Genera documentación completa en Markdown basada en block.json.
"""
import os
import json
from typing import Dict, List, Optional


def generate_comprehensive_block_docs(theme_dir: str, bem_prefix: str = 'img2html'):
    """
    Genera documentación completa para todos los bloques.
    Incluye: propósito, variantes, estructura HTML, atributos, buenas prácticas, cuándo usar/no usar.
    """
    blocks_dir = os.path.join(theme_dir, 'blocks')
    docs_dir = os.path.join(theme_dir, 'docs', 'components')
    os.makedirs(docs_dir, exist_ok=True)
    
    # Documentar átomos
    atoms_dir = os.path.join(blocks_dir, 'atoms')
    if os.path.isdir(atoms_dir):
        for atom_name in os.listdir(atoms_dir):
            atom_path = os.path.join(atoms_dir, atom_name)
            if os.path.isdir(atom_path):
                _document_block(atom_path, docs_dir, 'atom', atom_name, bem_prefix)
    
    # Documentar moléculas
    molecules_dir = os.path.join(blocks_dir, 'molecules')
    if os.path.isdir(molecules_dir):
        for molecule_name in os.listdir(molecules_dir):
            molecule_path = os.path.join(molecules_dir, molecule_name)
            if os.path.isdir(molecule_path):
                _document_block(molecule_path, docs_dir, 'molecule', molecule_name, bem_prefix)
    
    # Documentar organismos
    organisms_dir = os.path.join(blocks_dir, 'organisms')
    if os.path.isdir(organisms_dir):
        for organism_name in os.listdir(organisms_dir):
            organism_path = os.path.join(organisms_dir, organism_name)
            if os.path.isdir(organism_path):
                _document_block(organism_path, docs_dir, 'organism', organism_name, bem_prefix)
    
    # Generar índice de documentación
    _generate_docs_index(docs_dir, blocks_dir, bem_prefix)
    
    print(f"✓ Documentación completa generada en {docs_dir}/")


def _document_block(block_dir: str, docs_dir: str, block_type: str, block_name: str, bem_prefix: str):
    """Genera documentación completa para un bloque individual."""
    block_json_path = os.path.join(block_dir, 'block.json')
    if not os.path.isfile(block_json_path):
        return
    
    try:
        with open(block_json_path, 'r', encoding='utf-8') as f:
            block_data = json.load(f)
    except Exception:
        return
    
    render_php_path = os.path.join(block_dir, 'render.php')
    html_structure = _extract_html_structure(render_php_path)
    
    # Información del bloque
    block_full_name = block_data.get('name', f"{bem_prefix}/{block_type}-{block_name}")
    title = block_data.get('title', block_name.replace('-', ' ').title())
    description = block_data.get('description', '')
    category = block_data.get('category', '')
    keywords = block_data.get('keywords', [])
    attributes = block_data.get('attributes', {})
    supports = block_data.get('supports', {})
    
    # Determinar propósito y variantes
    purpose = _get_block_purpose(block_type, block_name, description)
    variants = _get_block_variants(block_type, block_name, attributes)
    best_practices = _get_best_practices(block_type, block_name)
    when_to_use = _get_when_to_use(block_type, block_name)
    when_not_to_use = _get_when_not_to_use(block_type, block_name)
    
    # Generar documentación Markdown
    doc_content = f"""# {title}

**Tipo**: {block_type.title()}  
**Nombre del Bloque**: `{block_full_name}`  
**Categoría**: `{category}`  
**Prefijo BEM**: `{bem_prefix}`

{f"**Keywords**: {', '.join(keywords)}" if keywords else ""}

---

## 📋 Propósito

{purpose}

---

## 🎨 Variantes

{variants}

---

## 🏗️ Estructura HTML

```html
{html_structure}
```

### Clases CSS Principales

- **Clase base**: `{bem_prefix}-{block_type}-{block_name}`
- **Elementos**: `{bem_prefix}-{block_type}-{block_name}__elemento`
- **Modificadores**: `{bem_prefix}-{block_type}-{block_name}--modificador`

---

## ⚙️ Atributos

"""
    
    # Documentar atributos
    if attributes:
        doc_content += "| Atributo | Tipo | Default | Descripción |\n"
        doc_content += "|----------|------|---------|-------------|\n"
        for attr_name, attr_data in attributes.items():
            attr_type = attr_data.get('type', 'unknown')
            attr_default = attr_data.get('default', 'N/A')
            attr_desc = _get_attribute_description(block_type, block_name, attr_name)
            if isinstance(attr_default, bool):
                attr_default = 'true' if attr_default else 'false'
            elif isinstance(attr_default, (list, dict)):
                attr_default = str(attr_default)
            doc_content += f"| `{attr_name}` | `{attr_type}` | `{attr_default}` | {attr_desc} |\n"
    else:
        doc_content += "Este bloque no tiene atributos configurables.\n"
    
    # Supports
    if supports:
        doc_content += "\n### Características Soportadas\n\n"
        for support_key, support_value in supports.items():
            if isinstance(support_value, bool):
                if support_value:
                    doc_content += f"- ✅ **{support_key}**: Soportado\n"
            elif isinstance(support_value, dict):
                doc_content += f"- **{support_key}**:\n"
                for k, v in support_value.items():
                    if v:
                        doc_content += f"  - `{k}`: {v}\n"
            elif isinstance(support_value, list):
                doc_content += f"- **{support_key}**: {', '.join(map(str, support_value))}\n"
    
    doc_content += f"""

---

## ✅ Cuándo Usar

{when_to_use}

---

## ❌ Cuándo NO Usar

{when_not_to_use}

---

## 💡 Buenas Prácticas

{best_practices}

---

## 📝 Ejemplo de Uso

### En el Editor de Bloques

```
<!-- wp:{block_full_name} /-->
```

### Con Atributos

```html
<!-- wp:{block_full_name} {{"attribute1": "value1", "attribute2": true}} /-->
```

### Ejemplo Completo

{_get_usage_example(block_type, block_name, block_full_name, attributes)}

---

## 🔗 Relaciones

{_get_block_relationships(block_type, block_name, bem_prefix)}

---

## 📚 Recursos Adicionales

- **Archivo del bloque**: `blocks/{block_type}s/{block_name}/`
- **Assets**: `assets/blocks/{block_type}s/{block_name}/`
- **Estilos**: Usa metodología BEM con prefijo `{bem_prefix}`

---

*Documentación generada automáticamente desde `block.json`*
"""
    
    # Guardar documentación
    doc_filename = f"{block_type}-{block_name}.md"
    doc_path = os.path.join(docs_dir, doc_filename)
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(doc_content)


def _extract_html_structure(render_php_path: str) -> str:
    """Extrae la estructura HTML del render.php."""
    if not os.path.isfile(render_php_path):
        return "<!-- Estructura HTML no disponible -->"
    
    try:
        with open(render_php_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extraer solo las líneas HTML (sin PHP)
        html_lines = []
        in_php = False
        for line in content.split('\n'):
            stripped = line.strip()
            if '<?php' in stripped:
                in_php = True
                continue
            if '?>' in stripped:
                in_php = False
                continue
            if not in_php and stripped and not stripped.startswith('//'):
                # Limpiar variables PHP pero mantener estructura
                cleaned = line.replace('<?php echo ', '').replace('<?=', '').replace('?>', '')
                cleaned = cleaned.replace('esc_attr(', '').replace('esc_html(', '').replace('esc_url(', '')
                cleaned = cleaned.replace('$attributes', '[attributes]').replace('$', '')
                html_lines.append(cleaned)
        
        if html_lines:
            return '\n'.join(html_lines[:30])  # Limitar a 30 líneas
        return "<!-- Estructura HTML no disponible -->"
    except Exception:
        return "<!-- Error al extraer estructura HTML -->"


def _get_block_purpose(block_type: str, block_name: str, description: str) -> str:
    """Obtiene el propósito del bloque."""
    purposes = {
        'atom-button': 'Botón básico reutilizable. Componente fundamental para acciones y navegación.',
        'atom-heading': 'Título reutilizable con niveles configurables (h1-h6).',
        'atom-input': 'Campo de entrada básico para formularios.',
        'atom-icon': 'Icono SVG o de fuente. Componente visual básico.',
        'atom-badge': 'Etiqueta o badge para destacar información.',
        'atom-link': 'Enlace básico reutilizable.',
        'atom-image': 'Imagen optimizada con lazy loading y atributos configurables.',
        'molecule-card': 'Tarjeta que combina imagen, título, texto y botón. Componente compuesto.',
        'molecule-form-field': 'Campo de formulario completo con label y validación.',
        'molecule-testimonial': 'Testimonio con cita, autor y opcionalmente imagen.',
        'molecule-nav-item': 'Item de navegación con enlace e icono opcional.',
        'molecule-pricing-item': 'Item de tabla de precios con características.',
        'organism-slider': 'Slider completo con múltiples diapositivas, controles y autoplay.',
        'organism-hero': 'Sección hero de página con título, subtítulo, imagen de fondo y CTA.',
        'organism-section': 'Sección multipropósito con contenido flexible y layouts configurables.',
        'organism-cards-grid': 'Grid de tarjetas con número variable de columnas.',
        'organism-gallery': 'Galería de imágenes con grid automático y opción de popup.',
        'organism-header': 'Header global del sitio con logo, menú y botones.',
        'organism-footer': 'Footer global con columnas, enlaces y widgets.',
        'organism-form': 'Formulario de contacto completo con validación.',
        'organism-menu': 'Menú de navegación con soporte para dropdowns.',
        'organism-sidebar': 'Sidebar dinámico con enlaces y widgets opcionales.',
        'organism-search': 'Buscador extendido con opciones de estilo.',
        'organism-pagination': 'Paginación para posts y archivos.',
        'organism-cta': 'Call to Action completo con título, descripción y botones.',
        'organism-text-image': 'Sección con texto e imagen en diferentes layouts.',
    }
    
    key = f"{block_type}-{block_name}"
    return purposes.get(key, description or f"Componente {block_type} para {block_name}.")


def _get_block_variants(block_type: str, block_name: str, attributes: Dict) -> str:
    """Obtiene las variantes disponibles del bloque."""
    variants_info = {
        'atom-button': ['primary', 'secondary', 'outline', 'small', 'medium', 'large', 'full-width'],
        'atom-heading': ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'],
        'organism-hero': ['full-height', 'half-height', 'with-video', 'with-form'],
        'organism-section': ['light', 'dark', 'with-image-background', 'full-width', 'container'],
        'organism-cards-grid': ['2-columns', '3-columns', '4-columns'],
    }
    
    key = f"{block_type}-{block_name}"
    variants = variants_info.get(key, [])
    
    # También buscar variantes en atributos
    variant_attrs = []
    for attr_name, attr_data in attributes.items():
        if attr_name in ['variant', 'style', 'size', 'type', 'layout']:
            if attr_data.get('type') == 'string' and 'default' in attr_data:
                variant_attrs.append(f"`{attr_name}`: {attr_data.get('default')}")
    
    if variants:
        return f"Este bloque tiene las siguientes variantes:\n\n" + "\n".join(f"- **{v}**" for v in variants)
    elif variant_attrs:
        return "Variantes configurables mediante atributos:\n\n" + "\n".join(f"- {v}" for v in variant_attrs)
    else:
        return "Este bloque no tiene variantes predefinidas. Se puede personalizar mediante atributos."


def _get_best_practices(block_type: str, block_name: str) -> str:
    """Obtiene buenas prácticas para el bloque."""
    practices = {
        'atom-button': """- Usa botones primarios para acciones principales
- Limita a 1-2 botones primarios por sección
- Usa botones secundarios para acciones secundarias
- Asegúrate de que el texto del botón sea descriptivo
- Mantén consistencia en el estilo de botones en todo el sitio""",
        'organism-slider': """- Limita a 3-5 slides para mejor rendimiento
- Usa imágenes optimizadas (WebP cuando sea posible)
- Configura autoplay solo si es necesario
- Asegúrate de que los textos sean legibles sobre las imágenes
- Incluye alt text descriptivo en todas las imágenes""",
        'organism-hero': """- Usa imágenes de alta calidad pero optimizadas
- Mantén el texto conciso y directo
- El CTA debe ser claro y visible
- Considera el contraste entre texto e imagen de fondo
- Usa overlay oscuro si el texto no es legible""",
        'organism-form': """- Valida todos los campos en frontend y backend
- Usa campos requeridos solo cuando sea necesario
- Proporciona mensajes de error claros
- Considera usar reCAPTCHA para prevenir spam
- Envía confirmación por email al usuario""",
    }
    
    key = f"{block_type}-{block_name}"
    return practices.get(key, """- Sigue las guías de diseño del tema
- Mantén consistencia con otros bloques
- Prueba en diferentes dispositivos
- Optimiza imágenes y assets
- Usa atributos semánticos cuando sea posible""")


def _get_when_to_use(block_type: str, block_name: str) -> str:
    """Obtiene cuándo usar el bloque."""
    usage = {
        'atom-button': """- Para acciones principales (enviar formulario, comprar, etc.)
- En CTAs (Call to Action)
- Para navegación secundaria
- En cards y tarjetas para acciones""",
        'organism-slider': """- Para mostrar múltiples imágenes o contenido destacado
- En la página principal para destacar productos/servicios
- Para testimonios rotativos
- Cuando necesites contenido visual impactante""",
        'organism-hero': """- En la página principal
- Al inicio de páginas de landing
- Para destacar contenido importante
- Cuando necesites una primera impresión fuerte""",
        'organism-form': """- Para formularios de contacto
- Para suscripciones a newsletter
- Para solicitudes de cotización
- Para cualquier recopilación de datos del usuario""",
    }
    
    key = f"{block_type}-{block_name}"
    return usage.get(key, f"Usa este bloque cuando necesites {block_name.replace('-', ' ')} en tu contenido.")


def _get_when_not_to_use(block_type: str, block_name: str) -> str:
    """Obtiene cuándo NO usar el bloque."""
    not_usage = {
        'organism-slider': """- En páginas con mucho contenido (puede ralentizar)
- Para contenido crítico (los usuarios pueden no ver todos los slides)
- En móviles si no es esencial
- Si tienes más de 7-8 slides (considera una galería)""",
        'organism-hero': """- En páginas internas que no lo necesiten
- Si ya tienes otro hero en la misma página
- Cuando el contenido es muy largo (ocupa mucho espacio)""",
        'atom-button': """- Para enlaces de navegación (usa enlaces normales)
- Para acciones destructivas sin confirmación
- Múltiples botones primarios en la misma sección""",
    }
    
    key = f"{block_type}-{block_name}"
    return not_usage.get(key, f"Evita usar este bloque cuando {block_name.replace('-', ' ')} no sea necesario o haya alternativas más simples.")


def _get_attribute_description(block_type: str, block_name: str, attr_name: str) -> str:
    """Obtiene descripción de un atributo."""
    descriptions = {
        ('atom-button', 'text'): 'Texto que se muestra en el botón',
        ('atom-button', 'url'): 'URL de destino del botón',
        ('atom-button', 'variant'): 'Estilo del botón (primary, secondary, outline)',
        ('organism-slider', 'showSlider'): 'Activar o desactivar el slider',
        ('organism-slider', 'autoplay'): 'Reproducir automáticamente los slides',
        ('organism-hero', 'title'): 'Título principal de la sección hero',
        ('organism-hero', 'subtitle'): 'Subtítulo o descripción',
    }
    
    key = (f"{block_type}-{block_name}", attr_name)
    return descriptions.get(key, f"Atributo {attr_name}")


def _get_usage_example(block_type: str, block_name: str, block_full_name: str, attributes: Dict) -> str:
    """Genera ejemplo de uso completo."""
    example_attrs = {}
    for attr_name, attr_data in list(attributes.items())[:3]:  # Limitar a 3 atributos
        example_attrs[attr_name] = attr_data.get('default', 'value')
    
    attrs_json = json.dumps(example_attrs, ensure_ascii=False, indent=2)
    
    return f"""```html
<!-- wp:{block_full_name} {attrs_json} /-->
```

O en el editor de bloques, simplemente busca "{block_name.replace('-', ' ').title()}" y agrégalo a tu contenido."""


def _get_block_relationships(block_type: str, block_name: str, bem_prefix: str) -> str:
    """Obtiene relaciones con otros bloques."""
    relationships = {
        'molecule-card': f"""Este bloque usa:
- `{bem_prefix}/atom-heading` para el título
- `{bem_prefix}/atom-button` para el botón
- `{bem_prefix}/atom-image` para la imagen (opcional)""",
        'organism-cards-grid': f"""Este bloque contiene:
- Múltiples instancias de `{bem_prefix}/molecule-card`""",
        'organism-hero': f"""Este bloque puede contener:
- `{bem_prefix}/atom-heading` para títulos
- `{bem_prefix}/atom-button` para CTAs""",
    }
    
    key = f"{block_type}-{block_name}"
    return relationships.get(key, f"Este bloque es independiente pero puede combinarse con otros bloques del tema.")


def _generate_docs_index(docs_dir: str, blocks_dir: str, bem_prefix: str):
    """Genera índice de toda la documentación."""
    index_content = f"""# Documentación de Componentes

Documentación completa de todos los bloques del tema `{bem_prefix}`.

## 📚 Índice

### Átomos

Componentes básicos reutilizables:

"""
    
    atoms_dir = os.path.join(blocks_dir, 'atoms')
    if os.path.isdir(atoms_dir):
        for atom_name in sorted(os.listdir(atoms_dir)):
            atom_path = os.path.join(atoms_dir, atom_name)
            if os.path.isdir(atom_path):
                doc_file = f"atom-{atom_name}.md"
                if os.path.isfile(os.path.join(docs_dir, doc_file)):
                    index_content += f"- [{atom_name.replace('-', ' ').title()}](atom-{atom_name}.md)\n"
    
    index_content += "\n### Moléculas\n\nCombinaciones de átomos:\n\n"
    
    molecules_dir = os.path.join(blocks_dir, 'molecules')
    if os.path.isdir(molecules_dir):
        for molecule_name in sorted(os.listdir(molecules_dir)):
            molecule_path = os.path.join(molecules_dir, molecule_name)
            if os.path.isdir(molecule_path):
                doc_file = f"molecule-{molecule_name}.md"
                if os.path.isfile(os.path.join(docs_dir, doc_file)):
                    index_content += f"- [{molecule_name.replace('-', ' ').title()}](molecule-{molecule_name}.md)\n"
    
    index_content += "\n### Organismos\n\nComponentes complejos:\n\n"
    
    organisms_dir = os.path.join(blocks_dir, 'organisms')
    if os.path.isdir(organisms_dir):
        for organism_name in sorted(os.listdir(organisms_dir)):
            organism_path = os.path.join(organisms_dir, organism_name)
            if os.path.isdir(organism_path):
                doc_file = f"organism-{organism_name}.md"
                if os.path.isfile(os.path.join(docs_dir, doc_file)):
                    index_content += f"- [{organism_name.replace('-', ' ').title()}](organism-{organism_name}.md)\n"
    
    index_content += f"""

---

## 🔍 Búsqueda Rápida

### Por Tipo de Uso

- **Navegación**: `organism-header`, `organism-menu`, `organism-sidebar`
- **Contenido**: `organism-hero`, `organism-section`, `organism-text-image`
- **Formularios**: `organism-form`, `molecule-form-field`, `atom-input`
- **Medios**: `organism-gallery`, `organism-slider`, `atom-image`
- **Acciones**: `atom-button`, `organism-cta`, `organism-pagination`

### Por Complejidad

- **Simple**: Átomos (button, heading, input, icon, badge, link, image)
- **Intermedio**: Moléculas (card, form-field, nav-item, testimonial, pricing-item)
- **Complejo**: Organismos (slider, hero, section, cards-grid, gallery, header, footer, form, menu, sidebar, search, pagination, cta, text-image)

---

*Documentación generada automáticamente*
"""
    
    index_path = os.path.join(docs_dir, 'README.md')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)


def generate_patterns_documentation(theme_dir: str, bem_prefix: str = 'img2html'):
    """Genera documentación completa para todos los patterns."""
    patterns_dir = os.path.join(theme_dir, 'patterns')
    docs_patterns_dir = os.path.join(theme_dir, 'docs', 'patterns')
    os.makedirs(docs_patterns_dir, exist_ok=True)
    
    if not os.path.isdir(patterns_dir):
        return
    
    # Leer patterns_meta.json si existe
    meta_path = os.path.join(patterns_dir, 'patterns_meta.json')
    patterns_meta = []
    if os.path.isfile(meta_path):
        try:
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta_data = json.load(f)
                patterns_meta = meta_data.get('patterns', [])
        except Exception:
            pass
    
    # Documentar cada pattern
    for pattern_file in os.listdir(patterns_dir):
        if not pattern_file.endswith('.php'):
            continue
        
        pattern_path = os.path.join(patterns_dir, pattern_file)
        pattern_slug = os.path.splitext(pattern_file)[0]
        
        # Buscar metadata
        pattern_info = next((p for p in patterns_meta if p.get('filename') == pattern_file), {})
        
        _document_pattern(pattern_path, docs_patterns_dir, pattern_slug, pattern_info, bem_prefix)
    
    # Generar índice de patterns
    _generate_patterns_index(docs_patterns_dir, patterns_meta, bem_prefix)
    
    print(f"✓ Documentación de patterns generada en {docs_patterns_dir}/")


def _document_pattern(pattern_path: str, docs_dir: str, pattern_slug: str, pattern_info: Dict, bem_prefix: str):
    """Genera documentación para un pattern individual."""
    try:
        with open(pattern_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return
    
    # Extraer metadata del header PHP
    title = pattern_info.get('title', pattern_slug.replace('-', ' ').title())
    description = pattern_info.get('description', '')
    categories = pattern_info.get('categories', [])
    sync_status = pattern_info.get('syncStatus', 'unsynced')
    
    # Extraer contenido HTML
    html_content = content.split('?>', 1)[-1].strip() if '?>' in content else content
    
    doc_content = f"""# {title}

**Slug**: `{bem_prefix}/{pattern_slug}`  
**Tipo**: {'🔄 Sincronizado' if sync_status == 'synced' else '📄 Reutilizable'}  
**Categorías**: {', '.join(f'`{c}`' for c in categories)}

---

## 📋 Descripción

{description}

---

## 🔄 Estado de Sincronización

{'**Sincronizado (Synced)**: Este pattern se actualiza globalmente. Los cambios se reflejan en todas las instancias.' if sync_status == 'synced' else '**Reutilizable (Unsynced)**: Este pattern se puede insertar múltiples veces con contenido independiente.'}

---

## 🏗️ Estructura

```html
{html_content[:500]}...
```

---

## ✅ Cuándo Usar

{_get_pattern_usage(pattern_slug)}

---

## 📝 Cómo Insertar

1. En el Editor del Sitio, ve a la página o template donde quieres insertar el pattern
2. Haz clic en el botón "+" para agregar un bloque
3. Busca "{title}" en la categoría de patterns
4. Selecciona el pattern para insertarlo

---

## ⚙️ Personalización

{'Como este pattern está sincronizado, los cambios se aplican globalmente. Edita desde el Editor del Sitio → Patterns.' if sync_status == 'synced' else 'Cada instancia de este pattern se puede editar independientemente. Haz clic en el pattern insertado para editarlo.'}

---

## 🔗 Bloques Relacionados

Este pattern puede contener los siguientes bloques:
{_get_pattern_blocks(html_content, bem_prefix)}

---

*Documentación generada automáticamente*
"""
    
    doc_filename = f"{pattern_slug}.md"
    doc_path = os.path.join(docs_dir, doc_filename)
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(doc_content)


def _get_pattern_usage(pattern_slug: str) -> str:
    """Obtiene cuándo usar un pattern."""
    usage = {
        'header-global': 'En todas las páginas del sitio. Se inserta automáticamente en templates.',
        'footer-global': 'En todas las páginas del sitio. Se inserta automáticamente en templates.',
        'cta-primary': 'En páginas de landing, al final de posts, o en secciones destacadas.',
        'hero-section': 'En la página principal o páginas de landing importantes.',
        'cards-grid': 'Para mostrar servicios, productos, o características en formato de grid.',
        'testimonials-section': 'En páginas de servicios, productos, o landing pages.',
    }
    
    return usage.get(pattern_slug, f"Usa este pattern cuando necesites {pattern_slug.replace('-', ' ')} en tu contenido.")


def _get_pattern_blocks(html_content: str, bem_prefix: str) -> str:
    """Extrae los bloques usados en el pattern."""
    import re
    blocks = re.findall(r'wp:([^/\s]+)', html_content)
    unique_blocks = sorted(set(blocks))
    
    if unique_blocks:
        return "\n".join(f"- `{bem_prefix}/{b}`" if b.startswith(bem_prefix) else f"- `{b}`" for b in unique_blocks[:10])
    return "No se detectaron bloques específicos."


def _generate_patterns_index(docs_dir: str, patterns_meta: List[Dict], bem_prefix: str):
    """Genera índice de documentación de patterns."""
    index_content = f"""# Documentación de Patterns

Documentación completa de todos los patterns del tema `{bem_prefix}`.

## 📚 Índice

### Patterns Sincronizados

Estos patterns se actualizan globalmente:

"""
    
    synced = [p for p in patterns_meta if p.get('syncStatus') == 'synced']
    for pattern in synced:
        slug = pattern.get('slug', '').replace(f'{bem_prefix}/', '')
        title = pattern.get('title', slug)
        doc_file = f"{slug}.md"
        if os.path.isfile(os.path.join(docs_dir, doc_file)):
            index_content += f"- [{title}]({doc_file})\n"
    
    index_content += "\n### Patterns Reutilizables\n\nEstos patterns se pueden insertar múltiples veces:\n\n"
    
    unsynced = [p for p in patterns_meta if p.get('syncStatus') != 'synced']
    for pattern in unsynced:
        slug = pattern.get('slug', '').replace(f'{bem_prefix}/', '')
        title = pattern.get('title', slug)
        doc_file = f"{slug}.md"
        if os.path.isfile(os.path.join(docs_dir, doc_file)):
            index_content += f"- [{title}]({doc_file})\n"
    
    index_content += "\n---\n\n*Documentación generada automáticamente*\n"
    
    index_path = os.path.join(docs_dir, 'README.md')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)


