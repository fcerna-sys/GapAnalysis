# Párrafo (Átomo)

**Tipo**: Atom  
**Nombre del Bloque**: `img2html/atom-paragraph`  
**Categoría**: `text`  
**Prefijo BEM**: `img2html`



---

## 📋 Propósito

Párrafo básico reutilizable

---

## 🎨 Variantes

Este bloque no tiene variantes predefinidas. Se puede personalizar mediante atributos.

---

## 🏗️ Estructura HTML

```html
<!-- Estructura HTML no disponible -->
```

### Clases CSS Principales

- **Clase base**: `img2html-atom-paragraph`
- **Elementos**: `img2html-atom-paragraph__elemento`
- **Modificadores**: `img2html-atom-paragraph--modificador`

---

## ⚙️ Atributos

| Atributo | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `text` | `string` | `Texto del párrafo` | Atributo text |
| `align` | `string` | `left` | Atributo align |

### Características Soportadas

- **spacing**:
  - `margin`: True
- **typography**:
- **color**:


---

## ✅ Cuándo Usar

Usa este bloque cuando necesites paragraph en tu contenido.

---

## ❌ Cuándo NO Usar

Evita usar este bloque cuando paragraph no sea necesario o haya alternativas más simples.

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
<!-- wp:img2html/atom-paragraph /-->
```

### Con Atributos

```html
<!-- wp:img2html/atom-paragraph {"attribute1": "value1", "attribute2": true} /-->
```

### Ejemplo Completo

```html
<!-- wp:img2html/atom-paragraph {
  "text": "Texto del párrafo",
  "align": "left"
} /-->
```

O en el editor de bloques, simplemente busca "Paragraph" y agrégalo a tu contenido.

---

## 🔗 Relaciones

Este bloque es independiente pero puede combinarse con otros bloques del tema.

---

## 📚 Recursos Adicionales

- **Archivo del bloque**: `blocks/atoms/paragraph/`
- **Assets**: `assets/blocks/atoms/paragraph/`
- **Estilos**: Usa metodología BEM con prefijo `img2html`

---

*Documentación generada automáticamente desde `block.json`*
