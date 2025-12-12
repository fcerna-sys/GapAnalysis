# Testimonial (Molécula)

- Nombre: `img2html/molecule-testimonial`
- Clase base BEM: `img2html-testimonial`
- Propósito: testimonial pequeño con avatar, texto y autor

## Atributos
- `text`: cita del testimonial
- `author`: nombre del autor
- `role`: rol/cargo del autor
- `avatarUrl`: URL del avatar

## Estructura
```html
<div class="img2html-testimonial">
  <div class="img2html-testimonial__header">
    <img class="img2html-testimonial__avatar" />
    <div class="img2html-testimonial__meta">
      <strong class="img2html-testimonial__author">Autor</strong>
      <span class="img2html-testimonial__role">Cargo</span>
    </div>
  </div>
  <blockquote class="img2html-testimonial__text">Excelente servicio.</blockquote>
</div>
```

## Buenas prácticas
- Usa `role` con tono atenuado (coherente con el tema).
- Mantén imágenes cuadradas para avatares (`border-radius:50%`).
- Evita texto demasiado largo en `text`; usa párrafos separados si es necesario.
