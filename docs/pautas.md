Guía de Implementación: Motor "Img2HTML" a WordPress FSE

Objetivo: Conectar el sistema de análisis visual y la biblioteca de prompts avanzados con el flujo de ejecución de la aplicación para generar temas de WordPress FSE profesionales y fieles al diseño original.

FASE 1: Habilitar la Visión Multimodal (El "Ojo")

El modelo de IA necesita ver las imágenes para entender la estructura (Grid vs Flex, Espaciados, Alineaciones), no solo leer el texto extraído por OCR.

Archivo Objetivo: ai_refine.py

1.1. Codificación de Imágenes

Modifica la función refine_and_generate_wp para aceptar las rutas de las imágenes originales, no solo el HTML/CSS.

import base64

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# En refine_and_generate_wp:
# 1. Recibe la lista de imágenes del plan ('plan' dict)
# 2. Itera sobre las 3-5 imágenes más representativas (Hero, Cuerpo, Footer)
# 3. Codifícalas y prepáralas para la API de Gemini


1.2. Construcción del Payload Multimodal

Actualiza la llamada a model.generate_content para incluir los datos binarios de la imagen.

# Pseudocódigo para estructura del contenido en Gemini
request_content = [
    {"role": "user", "parts": [{"text": prompt_maestro}]},
    {"role": "user", "parts": [{"text": "Aquí están las referencias visuales del diseño:"}]}
]

for img_path in selected_images:
    b64_data = encode_image(img_path)
    request_content.append({
        "role": "user", 
        "parts": [{
            "inline_data": {
                "mime_type": "image/jpeg", 
                "data": b64_data
            }
        }]
    })


FASE 2: Extracción de "ADN" de Diseño (El "Diseñador")

Necesitamos datos reales para el theme.json, no valores predeterminados.

Archivo Objetivo: analyzer.py

2.1. Integrar Extractor de Paleta

Añade una librería ligera como colorgram.py o extcolors a requirements.txt.

# analyzer.py
import colorgram

def extract_design_dna(image_paths):
    # Analiza la imagen 'hero' o la primera del set
    colors = colorgram.extract(image_paths[0], 6)
    palette = []
    
    # Mapeo inteligente (el color más oscuro suele ser texto, el más claro fondo, el más saturado acento)
    sorted_colors = sort_by_luminance(colors) 
    
    return {
        "palette": [
            {"slug": "background", "color": rgb_to_hex(sorted_colors[-1])},
            {"slug": "text", "color": rgb_to_hex(sorted_colors[0])},
            {"slug": "primary", "color": rgb_to_hex(find_most_saturated(colors))}
        ],
        "typography": {
            # Aquí podrías usar una API externa para detectar fuentes si quisieras ir más allá
            "fontFamily": "Inter, system-ui, sans-serif" 
        }
    }


FASE 3: El Cerebro Orquestador (El "Director")

Actualmente app.py ignora tus 56 prompts. Debemos hacer que los ejecute.

Archivo Objetivo: app.py y wp_theme/prompts/runner.py

3.1. Convertir runner.py en un Módulo Importable

Refactoriza runner.py para que tenga una clase ThemeBuilder que acepte el plan y el dna (colores/fuentes).

3.2. Flujo de Ejecución en app.py

Reemplaza la llamada monolítica en la ruta /convert por este flujo secuencial:

Inicialización: Crear estructura de carpetas (wp_theme/).

Generación Base: Ejecutar 01_theme_json_full.json inyectando la paleta extraída en la Fase 2.

Generación de Estructura: Ejecutar prompts para 02_template_parts.json y 03_templates.json.

Generación de Contenido: Usar la IA con Visión (Fase 1) para decidir qué patrón usar para cada sección de la imagen.

Ejemplo: "Veo una imagen con 3 columnas -> Ejecutar prompt 35_grid_layouts.json".

# En app.py /convert
dna = extract_design_dna(images)
builder = ThemeBuilder(output_dir='wp_theme', context=dna)

# Paso 1: Configuración Global
builder.run_prompt('01_theme_json_full.json')

# Paso 2: Generar Partes
builder.run_prompt('02_template_parts.json')

# Paso 3: Iterar sobre el plan de secciones
for section in plan['sections']:
    # Decidir qué patrón usar basándose en el nombre inferido o análisis visual
    pattern_type = identify_pattern(section['image']) # ej: 'hero', 'features', 'gallery'
    builder.run_prompt(f"patterns/{pattern_type}.json", context=section)


FASE 4: Estrategia de Bloques y Slicing

Cómo manejar las imágenes dentro del HTML.

Estrategia Recomendada: "Componentes, no Lienzos"

Si el usuario sube "Secciones" (ej. hero.jpg, services.jpg):

Tratarlas como Bloques de Fondo (core/cover) o referencias visuales.

El HTML generado debe intentar replicar el texto sobre la imagen usando bloques core/heading y core/paragraph, en lugar de solo poner la imagen plana.

Refinamiento del Prompt de Conversión:

Instrucción explícita: "Analiza la imagen adjunta. Identifica si es un diseño complejo o una foto simple. Si es diseño, replícalo usando bloques core/columns y core/group. Si es foto, usa core/image".

Checklist de Tareas Inmediatas

[ ] Dependencias: Agregar colorgram.py (o similar) a requirements.txt.

[ ] Analyzer: Implementar función extract_design_dna.

[ ] AI Refine: Actualizar para soportar envío de imágenes Base64 a Gemini.

[ ] Runner: Modificar los prompts JSON para aceptar variables dinámicas (como los colores extraídos).

[ ] App: Conectar el ThemeBuilder en la ruta /convert.

Al completar estos pasos, tu aplicación dejará de ser un "convertidor estático" y se convertirá en un "Generador de Temas Inteligente" que realmente aprovecha la potencia de los 56 prompts que ya has diseñado.