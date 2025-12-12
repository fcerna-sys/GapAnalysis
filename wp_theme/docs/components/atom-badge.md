# Badge (Átomo)

**Tipo**: Atom  
**Nombre del Bloque**: `img2html/atom-badge`  
**Categoría**: `widgets`  
**Prefijo BEM**: `img2html`



---

## 📋 Propósito

Etiqueta o badge para destacar información.

---

## 🎨 Variantes

Variantes configurables mediante atributos:

- `variant`: default

---

## 🏗️ Estructura HTML

```html
<!-- Estructura HTML no disponible -->
```

### Clases CSS Principales

- **Clase base**: `img2html-atom-badge`
- **Elementos**: `img2html-atom-badge__elemento`
- **Modificadores**: `img2html-atom-badge--modificador`

---

## ⚙️ Atributos

| Atributo | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `text` | `string` | `Nuevo` | Atributo text |
| `variant` | `string` | `default` | Atributo variant |

### Características Soportadas

- **spacing**:
  - `margin`: True
- **color**:


---

## ✅ Cuándo Usar

Usa este bloque cuando necesites badge en tu contenido.

---

## ❌ Cuándo NO Usar

Evita usar este bloque cuando badge no sea necesario o haya alternativas más simples.

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
<!-- wp:img2html/atom-badge /-->
```

### Con Atributos

```html
<!-- wp:img2html/atom-badge {"attribute1": "value1", "attribute2": true} /-->
```

### Ejemplo Completo

```html
<!-- wp:img2html/atom-badge {
  "text": "Nuevo",
  "variant": "default"
} /-->
```

O en el editor de bloques, simplemente busca "Badge" y agrégalo a tu contenido.

---

## 🔗 Relaciones

Este bloque es independiente pero puede combinarse con otros bloques del tema.

---

## 📚 Recursos Adicionales

- **Archivo del bloque**: `blocks/atoms/badge/`
- **Assets**: `assets/blocks/atoms/badge/`
- **Estilos**: Usa metodología BEM con prefijo `img2html`

---

*Documentación generada automáticamente desde `block.json`*
