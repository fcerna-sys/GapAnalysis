# Link (Átomo)

**Tipo**: Atom  
**Nombre del Bloque**: `img2html/atom-link`  
**Categoría**: `text`  
**Prefijo BEM**: `img2html`



---

## 📋 Propósito

Enlace básico reutilizable.

---

## 🎨 Variantes

Este bloque no tiene variantes predefinidas. Se puede personalizar mediante atributos.

---

## 🏗️ Estructura HTML

```html
<!-- Estructura HTML no disponible -->
```

### Clases CSS Principales

- **Clase base**: `img2html-atom-link`
- **Elementos**: `img2html-atom-link__elemento`
- **Modificadores**: `img2html-atom-link--modificador`

---

## ⚙️ Atributos

| Atributo | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `text` | `string` | `Leer más` | Atributo text |
| `url` | `string` | `#` | Atributo url |
| `target` | `string` | `` | Atributo target |
| `rel` | `string` | `` | Atributo rel |

### Características Soportadas

- **spacing**:
  - `margin`: True
- **color**:


---

## ✅ Cuándo Usar

Usa este bloque cuando necesites link en tu contenido.

---

## ❌ Cuándo NO Usar

Evita usar este bloque cuando link no sea necesario o haya alternativas más simples.

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
<!-- wp:img2html/atom-link /-->
```

### Con Atributos

```html
<!-- wp:img2html/atom-link {"attribute1": "value1", "attribute2": true} /-->
```

### Ejemplo Completo

```html
<!-- wp:img2html/atom-link {
  "text": "Leer más",
  "url": "#",
  "target": ""
} /-->
```

O en el editor de bloques, simplemente busca "Link" y agrégalo a tu contenido.

---

## 🔗 Relaciones

Este bloque es independiente pero puede combinarse con otros bloques del tema.

---

## 📚 Recursos Adicionales

- **Archivo del bloque**: `blocks/atoms/link/`
- **Assets**: `assets/blocks/atoms/link/`
- **Estilos**: Usa metodología BEM con prefijo `img2html`

---

*Documentación generada automáticamente desde `block.json`*
