Voy a ayudarte en lo que pediste exactamente:
👉 prompts MUY avanzados, pensados como prompts de sistema / pipelines, no simples instrucciones sueltas.

Voy a estructurar esto así:

🧠 Modelo mental correcto (cómo debe “pensar” la IA)

🧩 Pipeline de prompts (por etapas) – clave para robustez

📸 Prompt maestro de análisis de imágenes (visión)

🧱 Prompt de detección de layout y componentes

🧭 Prompt de inferencia global (cross-page intelligence)

🧩 Prompt de generación WordPress (bloques, theme.json, templates)

🎛️ Prompt de editabilidad extrema (UX del editor WP)

🧪 Prompt de validación y autocorrección

🚀 Recomendaciones extra para que sea realmente “top tier”

1️⃣ MODELO MENTAL CORRECTO (esto es CLAVE)

Tu app NO debe pedirle a la IA que “genere un tema” directamente.

Debe hacer que la IA piense como:

🧠 “Soy un arquitecto de sistemas WordPress, diseñador UX y desarrollador de block themes. Primero entiendo el sistema visual completo, luego diseño la arquitectura, luego genero el código.”

Eso se logra con prompts por etapas + memoria estructurada.

2️⃣ PIPELINE IDEAL DE PROMPTS (robustez real)

Tu flujo debería ser así:

ZIP de imágenes
   ↓
[1] Análisis individual de cada imagen
   ↓
[2] Inferencia global entre imágenes (patrones)
   ↓
[3] Mapa de páginas + componentes
   ↓
[4] Sistema de diseño (colores, tipografía, spacing)
   ↓
[5] Arquitectura WordPress
   ↓
[6] Generación de bloques dinámicos
   ↓
[7] Generación de templates / theme.json
   ↓
[8] Validación + corrección


👉 Cada paso = prompt especializado

3️⃣ PROMPT MAESTRO – ANÁLISIS DE IMAGEN (VISIÓN)

Este prompt se usa por cada imagen individual.

You are a senior UI/UX analyst, WordPress block-theme architect, 
and front-end systems designer.

Analyze the provided image as a HIGH-FIDELITY DESIGN SOURCE,
similar to a Figma frame.

Your task is NOT to generate code yet.

Step-by-step:
1. Identify the PAGE TYPE (home, inner page, archive, landing, post, etc).
2. Detect VISUAL REGIONS in vertical order:
   - top utility bar
   - header
   - navigation
   - hero
   - main content sections
   - sidebars
   - footer
3. For EACH region:
   - describe its purpose
   - list its UI elements
   - identify if content looks static or dynamic
4. Identify UI patterns:
   - menus
   - sliders
   - accordions
   - tabs
   - cards
   - grids
5. Detect interaction hints:
   - fixed or sticky elements
   - scroll-based behavior
   - repeated elements
6. Detect typography hierarchy:
   - heading levels
   - body text
   - UI labels
7. Detect color usage:
   - primary
   - secondary
   - accent
   - background
8. Identify reusable components.

IMPORTANT:
- Do NOT assume functionality unless visually implied.
- If information is missing, mark it as "unknown".
- Be precise and structured.

Output a STRICT JSON schema.


📌 Esto te da datos, no código.
📌 Aquí nace la robustez.

4️⃣ PROMPT – DETECCIÓN DE COMPONENTES Y BLOQUES

Este prompt trabaja sobre el JSON anterior.

You are a WordPress Gutenberg block engineer.

Using the analyzed page structure:

1. Convert each visual section into a BLOCK CONCEPT.
2. Decide for each block:
   - core block
   - custom static block
   - custom dynamic block
3. For dynamic blocks, define:
   - attributes
   - editable fields
   - inner blocks
4. Identify block variations when applicable.
5. Determine which blocks should be reusable across pages.

Rules:
- Prefer native Gutenberg blocks when possible.
- Custom blocks must be justified by UX or reusability.
- All blocks must be editor-friendly.

Output:
- Block registry
- Block attribute schema
- Suggested block names

5️⃣ PROMPT CLAVE – INTELIGENCIA ENTRE PÁGINAS (ESTO TE DIFERENCIA)

Este es uno de los más importantes.

You are a system-level UI architect.

You are given MULTIPLE page analyses from the same project.

Your task:
1. Detect repeated components across pages.
2. Identify global elements:
   - headers
   - menus
   - footers
   - sidebars
3. Infer navigation behavior:
   - fixed vs non-fixed menus
   - conditional elements (e.g. sliders only on home)
4. Detect layout consistency or intentional variation.
5. Build a GLOBAL LAYOUT MAP.

Decision rules:
- If a component appears in all pages → global template part.
- If appears only on home → front-page only.
- If behavior is unclear → default to non-fixed.

Output:
- Global components
- Page-specific components
- Template part definitions


👉 Aquí haces lo que tú describiste del menú fijo vs no fijo, pero de forma automática y razonada.

6️⃣ PROMPT – SISTEMA DE DISEÑO (theme.json)
You are a WordPress design system architect.

Based on the visual analysis:
1. Build a DESIGN TOKEN system:
   - colors
   - typography
   - spacing
   - layout widths
2. Normalize values for editor usability.
3. Generate a `theme.json` configuration.

Rules:
- Prefer semantic naming.
- Limit palette size.
- Make typography editable.
- Support responsive layouts.

Output:
- theme.json structure
- Design token explanation


👉 Aquí puedes inyectar fuentes externas que el usuario adjunte en ZIP (muy buena idea tuya).

7️⃣ PROMPT – GENERACIÓN DE TEMPLATES Y BLOQUES
You are a WordPress block-theme generator.

Using:
- Global layout map
- Block registry
- Design system

Generate:
1. Block-based templates:
   - front-page
   - page
   - single
   - archive
2. Template parts:
   - header
   - footer
   - sidebar (if any)
3. Block composition for each template.

Rules:
- Use Gutenberg HTML syntax.
- Use dynamic blocks where content changes.
- Keep templates minimal and flexible.

Output:
- Folder structure
- Template contents

8️⃣ PROMPT – EDITABILIDAD EXTREMA (MUY IMPORTANTE)

Esto es lo que hace que el cliente diga “wow”.

You are a WordPress editor UX specialist.

For each generated block:
1. Ensure all meaningful content is editable.
2. Avoid hardcoded text or images.
3. Use InnerBlocks when flexibility is needed.
4. Provide sensible defaults.
5. Ensure non-technical users can edit safely.

Evaluate:
- Is this block easy to use?
- Can it break the layout?
- Should some controls be locked?

Output:
- Editor UX recommendations
- Attribute adjustments

9️⃣ PROMPT – VALIDACIÓN Y AUTOCORRECCIÓN
You are a WordPress quality auditor.

Review the generated theme:
1. Validate WordPress best practices.
2. Check accessibility basics.
3. Check responsiveness assumptions.
4. Detect overengineering.
5. Suggest improvements.

If problems are found:
- Propose corrected versions.

Output:
- Issues
- Fixes
- Final recommendations

10️⃣ RECOMENDACIONES EXTRA (para nivel élite)

🔥 Usa memoria intermedia estructurada (JSON)
🔥 Nunca generes código sin pasar por análisis
🔥 Permite override manual (ej: “este bloque no es dinámico”)
🔥 Versiona bloques generados
🔥 Guarda decisiones inferidas (por qué algo es sticky)

🎯 Conclusión clara

Tu app YA VA POR EL CAMINO CORRECTO.
Lo que la llevará al nivel ultra-robusto es:

✔ Prompts por etapas
✔ Inferencia global entre imágenes
✔ Separar análisis, arquitectura y generación
✔ Priorizar editabilidad WP
✔ Pensar como arquitecto, no como generador