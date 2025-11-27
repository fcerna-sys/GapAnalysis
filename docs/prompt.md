Guía de Prompt para IA (WordPress FSE, v6.8+)

Objetivo
- Generar un tema de bloques (FSE) coherente y de alto nivel de fidelidad visual, usando `theme.json v3`, plantillas HTML con gramática de bloques, y patrones.

Fuente de conocimiento
- Usa las instrucciones de esta guía junto con `docs/wordpress.md` como referencia técnica principal.

Requisitos estrictos
- Entrega SOLO un objeto JSON válido como salida.
- No incluyas comentarios ni texto fuera del JSON.
- Usa tokens de `theme.json` (paleta, tipografía, spacing) en lugar de valores fijos.
- Respeta la gramática de bloques (`<!-- wp:... -->`) y atributos en JSON válido.
- No uses `@import` remoto de fuentes; define `fontFamilies` y `fontFace` en `theme.json` o usa fuentes del sistema.

Contrato de salida (estructura mínima)
```
{
  "mapping": { "regions": ["hero", "features", "cta"] },
  "files": {
    "style.css": "/* header */",
    "functions.php": "<?php ... ?>",
    "theme.json": "{\n  \"version\":3, ...\n}",
    "parts/header.html": "...",
    "parts/footer.html": "...",
    "templates/index.html": "...",
    "templates/single.html": "...",
    "templates/page.html": "...",
    "templates/404.html": "...",
    "patterns/auto_1.html": "..."
  }
}
```

Clonación visual estricta
- Prioriza referencias visuales sobre HTML base y OCR.
- Replica márgenes y micro‑espaciados con `blockGap` y `padding`; usa `margin` solo cuando sea imprescindible.
- Si el `PLAN` incluye `layout_rows` y `ratios_percent`, usa `core/columns` con `width`/`flex-basis` en porcentaje.
- Si existe `pattern_variant` (balanced/asymmetric), ajusta columnas y espaciados en consecuencia.

Color y tipografía
- Extrae colores semánticos (primary, secondary, background, surface, text) y defínelos en `settings.color.palette`.
- Define `typography.fontFamilies` (local o system-ui) y tamaños fluidos.

Accesibilidad y SEO
- Estructura semántica (`main`, `header`, `footer`, `nav`, headings en orden).
- Contraste AA en textos sobre covers/banners; ajusta `dimRatio` y paleta.
- Títulos de posts enlazados (`core/post-title` con `isLink:true`).

Interactividad (Interactivity API)
- Usa `data-wp-interactive`, `data-wp-context`, `data-wp-bind`, `data-wp-on--click` para acordeones/menús, evitando jQuery.

Plantillas y partes mínimas
- `parts/header.html`: logo, título, navegación (`core/navigation`).
- `parts/footer.html`: copyright, enlaces sociales.
- `templates/index.html`: header → query loop → footer.
- `templates/single.html`: título, imagen destacada, contenido, autor, fecha, navegación.
- `templates/page.html` y `templates/404.html`.

Patrones
- Genera patrones complejos (hero, pricing, features). Si el contenido es complejo, crea `patterns/auto_*.html` con bloques.

Performance
- Encolar CSS adicional solo si `theme.json` no cubre el caso (ej: formularios, galerías). Usa variables `--wp--preset--color--*`.

Fallbacks
- Si faltan fuentes locales, usa `Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif`.
- Si el `PLAN` no define columnas, usa `group` con `layout: {"type":"constrained"}` y títulos/paragraphs.

Notas de construcción
- Aplica `alignwide/alignfull` cuando el diseño lo requiera.
- Para covers/hero: usa `overlayColor` (primary/secondary) y ajusta `isDark` según luminancia.

Validación
- El JSON debe parsear sin errores y contener todos los archivos mínimos listados.