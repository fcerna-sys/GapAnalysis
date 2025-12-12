# Título (Átomo)

**Tipo**: Atom  
**Nombre del Bloque**: `img2html/atom-heading`  
**Categoría**: `widgets`  
**Prefijo BEM**: `img2html`



---

## 📋 Propósito

Título reutilizable con niveles configurables (h1-h6).

---

## 🎨 Variantes

Este bloque tiene las siguientes variantes:

- **h1**
- **h2**
- **h3**
- **h4**
- **h5**
- **h6**

---

## 🏗️ Estructura HTML

```html
<!-- Estructura HTML no disponible -->
```

### Clases CSS Principales

- **Clase base**: `img2html-atom-heading`
- **Elementos**: `img2html-atom-heading__elemento`
- **Modificadores**: `img2html-atom-heading--modificador`

---

## ⚙️ Atributos

| Atributo | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `text` | `string` | `Título` | Atributo text |
| `level` | `number` | `2` | Atributo level |
| `align` | `string` | `left` | Atributo align |

### Características Soportadas

- **align**: left, center, right
- **spacing**:
  - `margin`: True
- **typography**:
- **color**:


---

## ✅ Cuándo Usar

Usa este bloque cuando necesites heading en tu contenido.

---

## ❌ Cuándo NO Usar

Evita usar este bloque cuando heading no sea necesario o haya alternativas más simples.

---

## 💡 Buenas Prácticas

- Sigue las guías de diseño del tema
- Mantén consistencia con otros bloques
- Prueba en diferentes dispositivos
- Optimiza imágenes y assets
- Usa atributos semánticos cuando sea posible

---

## 📝 Ejemplo de Uso

### En el Editor de Bloques

```
<!-- wp:img2html/atom-heading /-->
```

### Con Atributos

```html
<!-- wp:img2html/atom-heading {"attribute1": "value1", "attribute2": true} /-->
```

### Ejemplo Completo

```html
<!-- wp:img2html/atom-heading {
  "text": "Título",
  "level": 2,
  "align": "left"
} /-->
```

O en el editor de bloques, simplemente busca "Heading" y agrégalo a tu contenido.

---

## 🔗 Relaciones

Este bloque es independiente pero puede combinarse con otros bloques del tema.

---

## 📚 Recursos Adicionales

- **Archivo del bloque**: `blocks/atoms/heading/`
- **Assets**: `assets/blocks/atoms/heading/`
- **Estilos**: Usa metodología BEM con prefijo `img2html`

---

*Documentación generada automáticamente desde `block.json`*
