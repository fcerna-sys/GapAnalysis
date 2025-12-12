Assets por bloque (CSS/JS)

- Definir assets en `blocks-manifest.php` por slug de bloque.
- Claves soportadas: `style` (CSS), `script` (JS), `deps_style`, `deps_script`, `version`.
- El loader (`php/block_assets.php`) encola en editor y front‑end según presencia de bloque.

Ejemplo:

```
'core/gallery' => [
  'style' => ['assets/blocks/core-gallery.css'],
  'script' => ['assets/blocks/core-gallery.js'],
  'deps_script' => ['wp-dom-ready']
]
```