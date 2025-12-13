# Sistema Atómico (Átomos → Moléculas → Organismos)

## Estructura
- Directorio base: `blocks/`
- Grupos:
  - `atoms/` — bloques simples reutilizables (button, heading, paragraph, icon, input, badge, link, container)
  - `molecules/` — combinaciones de átomos (card, features-list, testimonial, team-member, pricing-feature)
  - `organisms/` — secciones completas (hero)

## Registro automático
- `functions.php` registra todos los bloques de `atoms`, `molecules`, `organisms` y también los que estén directamente en `blocks/`.
- No requiere pasos manuales: cualquier bloque con `block.json` será registrado.

## Convenciones
- Prefijo: `img2html/<tipo>-<slug>` por ejemplo `img2html/atom-button`.
- Archivos por bloque: `block.json`, `render.php`, `style.css`.
- BEM: utilizar `img2html_bem('<tipo>-<slug>')` para clases.
- Usar presets de `theme.json` (color, spacing, radius, fontSizes).

## Scaffolding
- Menú: Apariencia → Img2HTML Atomic.
- Formulario: elegir tipo (Átomo, Molécula, Organismo) y nombre.
- Crea directorio y archivos con contenido mínimo y BEM.

## Component Library
- La plantilla `templates/component-library.html` muestra ejemplos de átomos, moléculas y organismos.
- Puedes ampliar la página para incluir todos los bloques deseados.

## Buenas prácticas
- Evita estilos inline en `render.php`.
- Define variaciones `is-style-*` en `php/block_styles.php` y CSS en `blocks.css` o `assets/components/*`.
- Usa clases utilitarias mapeadas a presets (`has-lead-font-size`, `is-style-overline`).

