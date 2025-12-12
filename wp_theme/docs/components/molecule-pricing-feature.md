# Pricing Feature (Molécula)

**Tipo**: Molecule  
**Nombre del Bloque**: `img2html/molecule-pricing-feature`  
**Categoría**: `widgets`  
**Prefijo BEM**: `img2html`



---

## 📋 Propósito

Feature de pricing con precio, lista de features y CTA

---

## 🎨 Variantes

Este bloque no tiene variantes predefinidas. Se puede personalizar mediante atributos.

---

## 🏗️ Estructura HTML

```html
<!-- Estructura HTML no disponible -->
```

### Clases CSS Principales

- **Clase base**: `img2html-molecule-pricing-feature`
- **Elementos**: `img2html-molecule-pricing-feature__elemento`
- **Modificadores**: `img2html-molecule-pricing-feature--modificador`

---

## ⚙️ Atributos

| Atributo | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `title` | `string` | `Plan Básico` | Atributo title |
| `price` | `string` | `$19` | Atributo price |
| `features` | `array` | `['Feature A', 'Feature B', 'Feature C']` | Atributo features |
| `buttonText` | `string` | `Comprar` | Atributo buttonText |
| `buttonUrl` | `string` | `#` | Atributo buttonUrl |

### Características Soportadas

- **spacing**:
  - `margin`: True
  - `padding`: True
- **color**:
  - `background`: True


---

## ✅ Cuándo Usar

Usa este bloque cuando necesites pricing feature en tu contenido.

---

## ❌ Cuándo NO Usar

Evita usar este bloque cuando pricing feature no sea necesario o haya alternativas más simples.

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
<!-- wp:img2html/molecule-pricing-feature /-->
```

### Con Atributos

```html
<!-- wp:img2html/molecule-pricing-feature {"attribute1": "value1", "attribute2": true} /-->
```

### Ejemplo Completo

```html
<!-- wp:img2html/molecule-pricing-feature {
  "title": "Plan Básico",
  "price": "$19",
  "features": [
    "Feature A",
    "Feature B",
    "Feature C"
  ]
} /-->
```

O en el editor de bloques, simplemente busca "Pricing Feature" y agrégalo a tu contenido.

---

## 🔗 Relaciones

Este bloque es independiente pero puede combinarse con otros bloques del tema.

---

## 📚 Recursos Adicionales

- **Archivo del bloque**: `blocks/molecules/pricing-feature/`
- **Assets**: `assets/blocks/molecules/pricing-feature/`
- **Estilos**: Usa metodología BEM con prefijo `img2html`

---

*Documentación generada automáticamente desde `block.json`*
