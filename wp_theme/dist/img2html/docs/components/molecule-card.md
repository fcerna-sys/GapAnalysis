# Card (Molécula)

**Tipo**: Molecule  
**Nombre del Bloque**: `img2html/molecule-card`  
**Categoría**: `widgets`  
**Prefijo BEM**: `img2html`



---

## 📋 Propósito

Tarjeta que combina imagen, título, texto y botón. Componente compuesto.

---

## 🎨 Variantes

Este bloque no tiene variantes predefinidas. Se puede personalizar mediante atributos.

---

## 🏗️ Estructura HTML

```html
<!-- Estructura HTML no disponible -->
```

### Clases CSS Principales

- **Clase base**: `img2html-molecule-card`
- **Elementos**: `img2html-molecule-card__elemento`
- **Modificadores**: `img2html-molecule-card--modificador`

---

## ⚙️ Atributos

| Atributo | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `title` | `string` | `Título` | Atributo title |
| `text` | `string` | `Descripción corta.` | Atributo text |
| `imageUrl` | `string` | `` | Atributo imageUrl |
| `buttonText` | `string` | `Ver más` | Atributo buttonText |
| `buttonUrl` | `string` | `#` | Atributo buttonUrl |

### Características Soportadas

- **spacing**:
  - `margin`: True
- **color**:
  - `background`: True


---

## ✅ Cuándo Usar

Usa este bloque cuando necesites card en tu contenido.

---

## ❌ Cuándo NO Usar

Evita usar este bloque cuando card no sea necesario o haya alternativas más simples.

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
<!-- wp:img2html/molecule-card /-->
```

### Con Atributos

```html
<!-- wp:img2html/molecule-card {"attribute1": "value1", "attribute2": true} /-->
```

### Ejemplo Completo

```html
<!-- wp:img2html/molecule-card {
  "title": "Título",
  "text": "Descripción corta.",
  "imageUrl": ""
} /-->
```

O en el editor de bloques, simplemente busca "Card" y agrégalo a tu contenido.

---

## 🔗 Relaciones

Este bloque usa:
- `img2html/atom-heading` para el título
- `img2html/atom-button` para el botón
- `img2html/atom-image` para la imagen (opcional)

---

## 📚 Recursos Adicionales

- **Archivo del bloque**: `blocks/molecules/card/`
- **Assets**: `assets/blocks/molecules/card/`
- **Estilos**: Usa metodología BEM con prefijo `img2html`

---

*Documentación generada automáticamente desde `block.json`*
