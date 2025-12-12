# Card (Molécula)

- Nombre: `img2html/molecule-card`
- Clase base BEM: `img2html-card`
- Propósito: tarjeta con imagen, título, texto y acciones

## Atributos
- `title`: título
- `text`: descripción
- `imageUrl`: imagen
- `buttonText`: texto del botón
- `buttonUrl`: URL del botón

## Estructura
```html
<div class="img2html-card">
  <figure class="img2html-card__imagen"><img /></figure>
  <h3 class="img2html-card__titulo">Título</h3>
  <p class="img2html-card__texto">Descripción corta.</p>
  <div class="img2html-card__acciones">
    <div class="wp-block-button img2html-button img2html-button__primary"><a class="wp-block-button__link">Ver más</a></div>
  </div>
</div>
```

## Buenas prácticas
- Mantén padding/margins con presets de `spacing`
- Usa `img2html-button` para acciones internas
