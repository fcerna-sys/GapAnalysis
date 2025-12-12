# Ícono (Átomo)

**Tipo**: Atom  
**Nombre del Bloque**: `img2html/atom-icon`  
**Categoría**: `widgets`  
**Prefijo BEM**: `img2html`



---

## 📋 Propósito

Icono SVG o de fuente. Componente visual básico.

---

## 🎨 Variantes

Este bloque no tiene variantes predefinidas. Se puede personalizar mediante atributos.

---

## 🏗️ Estructura HTML

```html
<!-- Estructura HTML no disponible -->
```

### Clases CSS Principales

- **Clase base**: `img2html-atom-icon`
- **Elementos**: `img2html-atom-icon__elemento`
- **Modificadores**: `img2html-atom-icon--modificador`

---

## ⚙️ Atributos

| Atributo | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `name` | `string` | `star` | Atributo name |
| `size` | `number` | `20` | Atributo size |

### Características Soportadas

- **spacing**:
  - `margin`: True
- **color**:
  - `text`: True


---

## ✅ Cuándo Usar

Usa este bloque cuando necesites icon en tu contenido.

---

## ❌ Cuándo NO Usar

Evita usar este bloque cuando icon no sea necesario o haya alternativas más simples.

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
<!-- wp:img2html/atom-icon /-->
```

### Con Atributos

```html
<!-- wp:img2html/atom-icon {"attribute1": "value1", "attribute2": true} /-->
```

### Ejemplo Completo

```html
<!-- wp:img2html/atom-icon {
  "name": "star",
  "size": 20
} /-->
```

O en el editor de bloques, simplemente busca "Icon" y agrégalo a tu contenido.

---

## 🔗 Relaciones

Este bloque es independiente pero puede combinarse con otros bloques del tema.

---

## 📚 Recursos Adicionales

- **Archivo del bloque**: `blocks/atoms/icon/`
- **Assets**: `assets/blocks/atoms/icon/`
- **Estilos**: Usa metodología BEM con prefijo `img2html`

---

*Documentación generada automáticamente desde `block.json`*
