# Input (Átomo)

**Tipo**: Atom  
**Nombre del Bloque**: `img2html/atom-input`  
**Categoría**: `widgets`  
**Prefijo BEM**: `img2html`



---

## 📋 Propósito

Campo de entrada básico para formularios.

---

## 🎨 Variantes

Variantes configurables mediante atributos:

- `type`: text

---

## 🏗️ Estructura HTML

```html
<!-- Estructura HTML no disponible -->
```

### Clases CSS Principales

- **Clase base**: `img2html-atom-input`
- **Elementos**: `img2html-atom-input__elemento`
- **Modificadores**: `img2html-atom-input--modificador`

---

## ⚙️ Atributos

| Atributo | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `type` | `string` | `text` | Atributo type |
| `placeholder` | `string` | `` | Atributo placeholder |
| `value` | `string` | `` | Atributo value |
| `fullWidth` | `boolean` | `false` | Atributo fullWidth |

### Características Soportadas

- **spacing**:
  - `margin`: True
- **color**:


---

## ✅ Cuándo Usar

Usa este bloque cuando necesites input en tu contenido.

---

## ❌ Cuándo NO Usar

Evita usar este bloque cuando input no sea necesario o haya alternativas más simples.

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
<!-- wp:img2html/atom-input /-->
```

### Con Atributos

```html
<!-- wp:img2html/atom-input {"attribute1": "value1", "attribute2": true} /-->
```

### Ejemplo Completo

```html
<!-- wp:img2html/atom-input {
  "type": "text",
  "placeholder": "",
  "value": ""
} /-->
```

O en el editor de bloques, simplemente busca "Input" y agrégalo a tu contenido.

---

## 🔗 Relaciones

Este bloque es independiente pero puede combinarse con otros bloques del tema.

---

## 📚 Recursos Adicionales

- **Archivo del bloque**: `blocks/atoms/input/`
- **Assets**: `assets/blocks/atoms/input/`
- **Estilos**: Usa metodología BEM con prefijo `img2html`

---

*Documentación generada automáticamente desde `block.json`*
