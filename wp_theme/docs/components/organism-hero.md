# Hero (Organismo)

- Nombre: `img2html/organism-hero`
- Clase base BEM: `img2html-hero`
- Propósito: sección hero con título, subtítulo y acción

## Atributos
- `title`: texto principal
- `subtitle`: texto secundario
- `buttonText`: texto del botón
- `buttonUrl`: URL del botón

## Estructura
```html
<section class="img2html-hero">
  <h1 class="img2html-hero__title">Título</h1>
  <p class="img2html-hero__subtitle">Subtítulo</p>
  <div class="img2html-hero__actions">...</div>
</section>
```

## Buenas prácticas
- Evita sobrecargar el hero con controles; mantén el foco y contraste.
- Usa presets de `theme.json` para colores y tipografías.
