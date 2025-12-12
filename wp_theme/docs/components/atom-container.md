# Contenedor (Átomo)

- Nombre: `img2html/atom-container`
- Clase base BEM: `img2html-container`
- Propósito: contenedor simple con padding y fondo opcional

## Atributos
- `padding`: tamaño del relleno (por defecto `1rem`)
- `background`: color de fondo (usa la paleta del tema)
- `content`: contenido HTML interno

## Estructura
```html
<div class="img2html-container" style="padding:1rem;background:var(--wp--preset--color--background)">
  <!-- contenido -->
</div>
```

## Buenas prácticas
- Usa presets del tema para `background` y evita colores arbitrarios.
- Confía en BEM para estilos adicionales; evita CSS inline extensivo.
- Combínalo con `wp-block-group` cuando necesites layouts más complejos.
