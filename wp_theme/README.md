Img2HTML Theme — Guía rápida

Instalación
- Copia `wp_theme/` a `wp-content/themes/img2html/` o usa el slug que prefieras.
- Activa el tema en WordPress Admin → Apariencia → Temas.

Build
- Node: `npm install` y `npm run build` para minificar y purgar CSS/JS.
- Scripts: `wp_theme/build.bat` en Windows.

Contenido (WP-CLI / PowerShell / SQL)
- Genera scripts desde Apariencia → Content.
- Archivos: `tools/import-content.sh`, `tools/import-content.ps1`, `tools/import-content.sql`.

Assets condicionales
- Se encolan por bloque según `blocks-manifest.php`.

Seguridad
- Cabeceras seguras y endurecimiento en `php/security.php`.
- `DISALLOW_FILE_EDIT` activo (solo en desarrollo, ajusta en producción).

Versionado
- `VERSION` raíz sincroniza `version` en `block.json`.

Patrones
- `patterns.json` normalizado con prefijo BEM del tema.
