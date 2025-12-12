# Pricing Feature (Molécula)

- Nombre: `img2html/molecule-pricing-feature`
- Clase base BEM: `img2html-pricing-feature`
- Propósito: tarjeta de pricing con título, precio, lista y CTA

## Atributos
- `title`, `price`, `features[]`, `buttonText`, `buttonUrl`

## Estructura
```html
<div class="img2html-pricing-feature">
  <h3 class="img2html-pricing-feature__title">Plan</h3>
  <div class="img2html-pricing-feature__price">$19</div>
  <ul class="img2html-pricing-feature__list"><li>Feature A</li></ul>
  <div class="wp-block-buttons img2html-pricing-feature__actions">
    <div class="wp-block-button img2html-button img2html-button__primary"><a class="wp-block-button__link">Comprar</a></div>
  </div>
</div>
```
