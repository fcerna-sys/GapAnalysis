# Hero (Organismo)

**Tipo**: Organism  
**Nombre del Bloque**: `img2html/organism-hero`  
**Categoría**: `layout`  
**Prefijo BEM**: `img2html`



---

## 📋 Propósito

Sección hero de página con título, subtítulo, imagen de fondo y CTA.

---

## 🎨 Variantes

Este bloque tiene las siguientes variantes:

- **full-height**
- **half-height**
- **with-video**
- **with-form**

---

## 🏗️ Estructura HTML

```html
<!-- Estructura HTML no disponible -->
```

### Clases CSS Principales

- **Clase base**: `img2html-organism-hero`
- **Elementos**: `img2html-organism-hero__elemento`
- **Modificadores**: `img2html-organism-hero--modificador`

---

## ⚙️ Atributos

| Atributo | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `title` | `string` | `Título destacado` | Título principal de la sección hero |
| `subtitle` | `string` | `Subtítulo breve` | Subtítulo o descripción |
| `buttonText` | `string` | `Empezar` | Atributo buttonText |
| `buttonUrl` | `string` | `#` | Atributo buttonUrl |

### Características Soportadas

- **spacing**:
  - `margin`: True
  - `padding`: True
- **color**:
  - `background`: True


---

## ✅ Cuándo Usar

- En la página principal
- Al inicio de páginas de landing
- Para destacar contenido importante
- Cuando necesites una primera impresión fuerte

---

## ❌ Cuándo NO Usar

- En páginas internas que no lo necesiten
- Si ya tienes otro hero en la misma página
- Cuando el contenido es muy largo (ocupa mucho espacio)

---

## 💡 Buenas Prácticas

- Usa imágenes de alta calidad pero optimizadas
- Mantén el texto conciso y directo
- El CTA debe ser claro y visible
- Considera el contraste entre texto e imagen de fondo
- Usa overlay oscuro si el texto no es legible

---

## 📝 Ejemplo de Uso

### En el Editor de Bloques

```
<!-- wp:img2html/organism-hero /-->
```

### Con Atributos

```html
<!-- wp:img2html/organism-hero {"attribute1": "value1", "attribute2": true} /-->
```

### Ejemplo Completo

```html
<!-- wp:img2html/organism-hero {
  "title": "Título destacado",
  "subtitle": "Subtítulo breve",
  "buttonText": "Empezar"
} /-->
```

O en el editor de bloques, simplemente busca "Hero" y agrégalo a tu contenido.

---

## 🔗 Relaciones

Este bloque puede contener:
- `img2html/atom-heading` para títulos
- `img2html/atom-button` para CTAs

---

## 📚 Recursos Adicionales

- **Archivo del bloque**: `blocks/organisms/hero/`
- **Assets**: `assets/blocks/organisms/hero/`
- **Estilos**: Usa metodología BEM con prefijo `img2html`

---

*Documentación generada automáticamente desde `block.json`*
