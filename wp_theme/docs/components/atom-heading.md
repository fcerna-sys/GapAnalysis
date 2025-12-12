# Título (Átomo)

- Nombre: `img2html/atom-heading`
- Clase base BEM: `img2html-heading`
- Propósito: encabezado reutilizable con alineación

## Atributos
- `text`: contenido del título
- `level`: nivel de encabezado (1–6)
- `align`: `left` | `center` | `right`

## Estructura
```html
<h2 class="img2html-heading img2html-heading--center">Título</h2>
```

## Buenas prácticas
- Mantén niveles coherentes (solo un `h1` por página).
- Usa los modificadores BEM para alineación; evita estilos inline.
- No habilites cambios de tipografía en el editor para consistencia.
