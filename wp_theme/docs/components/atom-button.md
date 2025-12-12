# Botón (Átomo)

**Tipo**: Atom  
**Nombre del Bloque**: `img2html/atom-button`  
**Categoría**: `widgets`  
**Prefijo BEM**: `img2html`



---

## 📋 Propósito

Botón básico reutilizable. Componente fundamental para acciones y navegación.

---

## 🎨 Variantes

Este bloque tiene las siguientes variantes:

- **primary**
- **secondary**
- **outline**
- **small**
- **medium**
- **large**
- **full-width**

---

## 🏗️ Estructura HTML

```html
<!-- Estructura HTML no disponible -->
```

### Clases CSS Principales

- **Clase base**: `img2html-atom-button`
- **Elementos**: `img2html-atom-button__elemento`
- **Modificadores**: `img2html-atom-button--modificador`

---

## ⚙️ Atributos

| Atributo | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `text` | `string` | `Acción` | Texto que se muestra en el botón |
| `url` | `string` | `#` | URL de destino del botón |
| `variant` | `string` | `primary` | Estilo del botón (primary, secondary, outline) |
| `fullWidth` | `boolean` | `false` | Atributo fullWidth |

### Características Soportadas

- **align**: left, center, right
- **spacing**:
  - `margin`: True
- **color**:
  - `background`: True


---

## ✅ Cuándo Usar

- Para acciones principales (enviar formulario, comprar, etc.)
- En CTAs (Call to Action)
- Para navegación secundaria
- En cards y tarjetas para acciones

---

## ❌ Cuándo NO Usar

- Para enlaces de navegación (usa enlaces normales)
- Para acciones destructivas sin confirmación
- Múltiples botones primarios en la misma sección

---

## 💡 Buenas Prácticas

- Usa botones primarios para acciones principales
- Limita a 1-2 botones primarios por sección
- Usa botones secundarios para acciones secundarias
- Asegúrate de que el texto del botón sea descriptivo
- Mantén consistencia en el estilo de botones en todo el sitio

---

## 📝 Ejemplo de Uso

### En el Editor de Bloques

```
<!-- wp:img2html/atom-button /-->
```

### Con Atributos

```html
<!-- wp:img2html/atom-button {"attribute1": "value1", "attribute2": true} /-->
```

### Ejemplo Completo

```html
<!-- wp:img2html/atom-button {
  "text": "Acción",
  "url": "#",
  "variant": "primary"
} /-->
```

O en el editor de bloques, simplemente busca "Button" y agrégalo a tu contenido.

---

## 🔗 Relaciones

Este bloque es independiente pero puede combinarse con otros bloques del tema.

---

## 📚 Recursos Adicionales

- **Archivo del bloque**: `blocks/atoms/button/`
- **Assets**: `assets/blocks/atoms/button/`
- **Estilos**: Usa metodología BEM con prefijo `img2html`

---

*Documentación generada automáticamente desde `block.json`*
