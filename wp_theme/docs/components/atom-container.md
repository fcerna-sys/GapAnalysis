# Contenedor (Átomo)

**Tipo**: Atom  
**Nombre del Bloque**: `img2html/atom-container`  
**Categoría**: `layout`  
**Prefijo BEM**: `img2html`



---

## 📋 Propósito

Contenedor simple con padding y fondo opcional

---

## 🎨 Variantes

Este bloque no tiene variantes predefinidas. Se puede personalizar mediante atributos.

---

## 🏗️ Estructura HTML

```html
<!-- Estructura HTML no disponible -->
```

### Clases CSS Principales

- **Clase base**: `img2html-atom-container`
- **Elementos**: `img2html-atom-container__elemento`
- **Modificadores**: `img2html-atom-container--modificador`

---

## ⚙️ Atributos

| Atributo | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `padding` | `string` | `1rem` | Atributo padding |
| `background` | `string` | `` | Atributo background |
| `content` | `string` | `` | Atributo content |

### Características Soportadas

- **spacing**:
  - `margin`: True
  - `padding`: True
- **color**:
  - `background`: True


---

## ✅ Cuándo Usar

Usa este bloque cuando necesites container en tu contenido.

---

## ❌ Cuándo NO Usar

Evita usar este bloque cuando container no sea necesario o haya alternativas más simples.

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
<!-- wp:img2html/atom-container /-->
```

### Con Atributos

```html
<!-- wp:img2html/atom-container {"attribute1": "value1", "attribute2": true} /-->
```

### Ejemplo Completo

```html
<!-- wp:img2html/atom-container {
  "padding": "1rem",
  "background": "",
  "content": ""
} /-->
```

O en el editor de bloques, simplemente busca "Container" y agrégalo a tu contenido.

---

## 🔗 Relaciones

Este bloque es independiente pero puede combinarse con otros bloques del tema.

---

## 📚 Recursos Adicionales

- **Archivo del bloque**: `blocks/atoms/container/`
- **Assets**: `assets/blocks/atoms/container/`
- **Estilos**: Usa metodología BEM con prefijo `img2html`

---

*Documentación generada automáticamente desde `block.json`*
