Faltantes y estado — implementación completa

ALTA
- Canonical versioning: creado `VERSION` raíz y sincronizado `version` en `block.json` desde `theme_builder.py`.
- Enforcement BEM/linting: integrado `blocks_builder/bem_validator.py` en `build_optimizer.validate_bem_in_theme`.

MEDIA
- Normalización final de patterns: `patterns.json` reescribe slugs con el prefijo real del tema.
- CSS atómico físico: asegurado `style.css` por bloque y copiado a `assets/blocks/components/` con minificado y manifest.
- Exportador de contenido: `import-content.sh`, `.ps1` y `.sql` generados desde `wp_theme/php/content-pipeline.php`.

BAJA
- Documentación por tema: añadido `wp_theme/README.md` con guía rápida.
- Locking y UX editor: `ensure_block_json_supports` aplica restricciones; `enhance_block_json_ux` se usa en generadores.

Verificación
- Build del tema ejecutado (`npm run build`).
- Seguridad endurecida: cabeceras HTTP y `DISALLOW_FILE_EDIT` en desarrollo.
