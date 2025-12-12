# Miembro del equipo (Molécula)

**Tipo**: Molecule  
**Nombre del Bloque**: `img2html/molecule-team-member`  
**Categoría**: `widgets`  
**Prefijo BEM**: `img2html`



---

## 📋 Propósito

Tarjeta de miembro con avatar, nombre y rol

---

## 🎨 Variantes

Este bloque no tiene variantes predefinidas. Se puede personalizar mediante atributos.

---

## 🏗️ Estructura HTML

```html
<!-- Estructura HTML no disponible -->
```

### Clases CSS Principales

- **Clase base**: `img2html-molecule-team-member`
- **Elementos**: `img2html-molecule-team-member__elemento`
- **Modificadores**: `img2html-molecule-team-member--modificador`

---

## ⚙️ Atributos

| Atributo | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `name` | `string` | `Nombre` | Atributo name |
| `role` | `string` | `Rol` | Atributo role |
| `avatarUrl` | `string` | `` | Atributo avatarUrl |

### Características Soportadas

- **spacing**:
  - `margin`: True
- **color**:
  - `background`: True


---

## ✅ Cuándo Usar

Usa este bloque cuando necesites team member en tu contenido.

---

## ❌ Cuándo NO Usar

Evita usar este bloque cuando team member no sea necesario o haya alternativas más simples.

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
<!-- wp:img2html/molecule-team-member /-->
```

### Con Atributos

```html
<!-- wp:img2html/molecule-team-member {"attribute1": "value1", "attribute2": true} /-->
```

### Ejemplo Completo

```html
<!-- wp:img2html/molecule-team-member {
  "name": "Nombre",
  "role": "Rol",
  "avatarUrl": ""
} /-->
```

O en el editor de bloques, simplemente busca "Team Member" y agrégalo a tu contenido.

---

## 🔗 Relaciones

Este bloque es independiente pero puede combinarse con otros bloques del tema.

---

## 📚 Recursos Adicionales

- **Archivo del bloque**: `blocks/molecules/team-member/`
- **Assets**: `assets/blocks/molecules/team-member/`
- **Estilos**: Usa metodología BEM con prefijo `img2html`

---

*Documentación generada automáticamente desde `block.json`*
