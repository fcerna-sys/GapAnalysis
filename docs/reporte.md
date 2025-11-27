Reporte de Brechas: Código vs Objetivo FSE 2025

Este documento compara la implementación actual (Python/Flask) con los objetivos definidos en la Hoja de Ruta Técnica.

1. Estado de la Inferencia Visual (Crítico)

Objetivo: La IA debe "ver" el diseño para inferir Layouts (Grid/Flex).

Código Actual (ai_refine.py):

La función refine_and_generate_wp construye un payload solo de texto (HTML, CSS, INFO).

El modelo de IA recibe el contenido del OCR pero no la referencia visual.

Acción Requerida: Actualizar refine_and_generate_wp para codificar las imágenes en Base64 y enviarlas en el payload parts bajo la clave inline_data o image según la API de Gemini.

2. Tokenización y theme.json

Objetivo: Paleta de colores y tipografías extraídas del diseño.

Código Actual (ai_refine.py & analyzer.py):

analyzer.py solo procesa strings (nombres de archivo).

_fallback_wp usa una paleta estática predefinida:

"palette": [ {"name":"Primary","slug":"primary","color":"#3b82f6"}, ... ]


Acción Requerida:

Implementar extract_palette(image_paths) usando colorgram o PIL.

Pasar esta paleta dinámica al generador de theme.json.

3. Arquitectura de Prompts (Orquestación)

Objetivo: Uso de agentes especializados (Experto en JSON, Experto en Patrones).

Código Actual:

Existe una rica biblioteca en wp_theme/prompts/ (56 archivos).

app.py ignora esta biblioteca y usa un flujo lineal simple.

Acción Requerida:

Integrar la lógica de runner.py dentro de la ruta /convert de app.py.

El flujo debería ser: Upload -> Analyze -> Extract Colors -> (Loop through Prompts) -> Generate Theme.

4. Manejo de Imágenes (Slicing)

Objetivo: Separar elementos de interfaz de imágenes de contenido.

Código Actual (app.py):

zf.extractall(batch_dir) extrae todo.

El HTML generado incrusta las imágenes tal cual: <img src="assets/...".

Acción Requerida:

Si el input son diseños completos, se requiere un motor de recorte (Crop Engine).

Si el input son componentes sueltos, el código actual funciona pero necesita mejor lógica para decidir si una imagen es un core/image o un core/cover (fondo).

5. Mapeo a Bloques FSE

Objetivo: Usar bloques semánticos (core/navigation, core/query).

Código Actual:

El HTML intermedio es genérico (<section>, <div>).

La conversión a bloques depende 100% de la "alucinación" de la IA en un solo paso, sin contexto visual.

Acción Requerida:

Al enviar la imagen a la IA, solicitar explícitamente un mapeo JSON de regiones visuales a bloques de WordPress antes de generar el código.