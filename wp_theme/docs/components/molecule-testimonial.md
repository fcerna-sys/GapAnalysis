# Testimonial (Molécula)

**Tipo**: Molecule  
**Nombre del Bloque**: `img2html/molecule-testimonial`  
**Categoría**: `widgets`  
**Prefijo BEM**: `img2html`



---

## 📋 Propósito

Testimonio con cita, autor y opcionalmente imagen.

---

## 🎨 Variantes

Este bloque no tiene variantes predefinidas. Se puede personalizar mediante atributos.

---

## 🏗️ Estructura HTML

```html
<!-- Estructura HTML no disponible -->
```

### Clases CSS Principales

- **Clase base**: `img2html-molecule-testimonial`
- **Elementos**: `img2html-molecule-testimonial__elemento`
- **Modificadores**: `img2html-molecule-testimonial--modificador`

---

## ⚙️ Atributos

| Atributo | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `text` | `string` | `Excelente servicio.` | Atributo text |
| `author` | `string` | `Nombre` | Atributo author |
| `role` | `string` | `Cargo` | Atributo role |
| `avatarUrl` | `string` | `` | Atributo avatarUrl |

### Características Soportadas

- **spacing**:
  - `margin`: True
- **color**:
  - `background`: True


---

## ✅ Cuándo Usar

Usa este bloque cuando necesites testimonial en tu contenido.

---

## ❌ Cuándo NO Usar

Evita usar este bloque cuando testimonial no sea necesario o haya alternativas más simples.

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
<!-- wp:img2html/molecule-testimonial /-->
```

### Con Atributos

```html
<!-- wp:img2html/molecule-testimonial {"attribute1": "value1", "attribute2": true} /-->
```

### Ejemplo Completo

```html
<!-- wp:img2html/molecule-testimonial {
  "text": "Excelente servicio.",
  "author": "Nombre",
  "role": "Cargo"
} /-->
```

O en el editor de bloques, simplemente busca "Testimonial" y agrégalo a tu contenido.

---

## 🔗 Relaciones

Este bloque es independiente pero puede combinarse con otros bloques del tema.

---

## 📚 Recursos Adicionales

- **Archivo del bloque**: `blocks/molecules/testimonial/`
- **Assets**: `assets/blocks/molecules/testimonial/`
- **Estilos**: Usa metodología BEM con prefijo `img2html`

---

*Documentación generada automáticamente desde `block.json`*
