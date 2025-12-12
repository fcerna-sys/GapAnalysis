# Lista de features (Molécula)

**Tipo**: Molecule  
**Nombre del Bloque**: `img2html/molecule-features-list`  
**Categoría**: `widgets`  
**Prefijo BEM**: `img2html`



---

## 📋 Propósito

Lista de características con título

---

## 🎨 Variantes

Este bloque no tiene variantes predefinidas. Se puede personalizar mediante atributos.

---

## 🏗️ Estructura HTML

```html
<!-- Estructura HTML no disponible -->
```

### Clases CSS Principales

- **Clase base**: `img2html-molecule-features-list`
- **Elementos**: `img2html-molecule-features-list__elemento`
- **Modificadores**: `img2html-molecule-features-list--modificador`

---

## ⚙️ Atributos

| Atributo | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `title` | `string` | `Características` | Atributo title |
| `items` | `array` | `['Rápido', 'Seguro', 'Escalable']` | Atributo items |

### Características Soportadas

- **spacing**:
  - `margin`: True
- **color**:
  - `background`: True


---

## ✅ Cuándo Usar

Usa este bloque cuando necesites features list en tu contenido.

---

## ❌ Cuándo NO Usar

Evita usar este bloque cuando features list no sea necesario o haya alternativas más simples.

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
<!-- wp:img2html/molecule-features-list /-->
```

### Con Atributos

```html
<!-- wp:img2html/molecule-features-list {"attribute1": "value1", "attribute2": true} /-->
```

### Ejemplo Completo

```html
<!-- wp:img2html/molecule-features-list {
  "title": "Características",
  "items": [
    "Rápido",
    "Seguro",
    "Escalable"
  ]
} /-->
```

O en el editor de bloques, simplemente busca "Features List" y agrégalo a tu contenido.

---

## 🔗 Relaciones

Este bloque es independiente pero puede combinarse con otros bloques del tema.

---

## 📚 Recursos Adicionales

- **Archivo del bloque**: `blocks/molecules/features-list/`
- **Assets**: `assets/blocks/molecules/features-list/`
- **Estilos**: Usa metodología BEM con prefijo `img2html`

---

*Documentación generada automáticamente desde `block.json`*
