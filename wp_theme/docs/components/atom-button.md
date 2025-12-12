# Botón (Átomo)

- Nombre: `img2html/atom-button`
- Clase base BEM: `img2html-button`
- Propósito: botón reutilizable con variantes

## Atributos
- `text`: texto del botón
- `url`: enlace
- `variant`: variante visual (`primary`, etc.)
- `fullWidth`: ancho completo

## Estructura
```html
<div class="wp-block-button img2html-button img2html-button__primary">
  <a class="wp-block-button__link">Acción</a>
</div>
```

## Buenas prácticas
- Usa la paleta del tema para `backgroundColor`
- Prefiere variantes BEM (`__primary`) sobre estilos en línea
