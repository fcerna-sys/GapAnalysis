# Pipeline de Contenido (IA → JSON → WP‑CLI)

## Flujo
- IA produce `content/content.json` con páginas, bloques e imágenes.
- Generador crea `tools/import-content.sh` y `tools/import-content.ps1`.
- Scripts importan media y crean páginas usando contenido Gutenberg.

## Ubicación
- JSON: `wp_theme/content/content.json`
- Scripts: `wp_theme/tools/import-content.{sh,ps1}`
- Bloques generados: `wp_theme/tools/blocks/*.blocks.html`

## Ejecución
- Bash:
  - `bash wp-content/themes/<slug>/tools/import-content.sh`
- PowerShell:
  - `powershell -ExecutionPolicy Bypass -File wp-content/themes/<slug>/tools/import-content.ps1`

## Notas
- Se usan IDs reales de attachments en bloques `core/image`.
- El theme no guarda contenido real; solo genera artefactos para inserción.
- Extiende el mapeo en `php/content-pipeline.php` si añades nuevos tipos de bloque.
- Cuando es posible, se usan bloques atómicos del tema (`img2html/atom-*`) para headings, párrafos y botones.
- `features-list` soporta íconos por ítem (`icon`) y usa `img2html/atom-icon` con layout flex; si no hay iconos, se usa `core/list`.
 - Opcionales por ítem: `iconColor` (usa paleta `theme.json` como `primary`, `accent`, etc.) y `size` (px).

## Validación
- Apariencia → Content muestra errores y advertencias antes de generar.
- Errores bloquean la generación (slugs duplicados, JSON inválido).
- Advertencias no bloquean (imagenes faltantes, campos opcionales vacíos).
