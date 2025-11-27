Guía de Desarrollo: GapAnalysis

Bienvenido a la documentación técnica de GapAnalysis. Este proyecto es un motor avanzado para convertir diseños visuales (imágenes/capturas) en temas de WordPress FSE (Full Site Editing) semánticos y de alta fidelidad, utilizando OCR, Análisis de Visión por Computadora y Modelos de Lenguaje Grande (LLMs).

1. Arquitectura del Sistema

El sistema opera como una tubería (pipeline) secuencial orquestada por app.py.

graph TD
    A[Usuario sube ZIP] --> B(app.py /upload)
    B --> C[analyzer.py: Análisis Estructural]
    C --> D[ocr.py: Extracción de Texto]
    D --> E[analyzer.py: Extracción de ADN de Diseño]
    E --> F{ThemeBuilder}
    F --> G[Generación de Scaffolding (Prompts JSON)]
    F --> H[ai_refine.py: Refinamiento con IA]
    H --> I[Generación de Archivos Finales]
    I --> J[Empaquetado ZIP]


Componentes Clave

app.py (Orquestador):

Maneja las rutas web (/upload, /convert).

Gestiona la carga de archivos y el almacenamiento temporal.

Coordina la llamada a los submódulos.

analyzer.py (El "Ojo" Analítico):

analyze_images(paths): Clasifica imágenes basándose en nombres de archivo (ej: 'hero', 'footer') e infiere el orden de las secciones.

extract_design_dna(paths): Utiliza colorgram.py (o fallback a PIL) para extraer la paleta de colores dominante (Primario, Secundario, Fondo, Texto) ignorando grises/blancos no esenciales.

segment_image(...): (Experimental) Utiliza OpenCV/PIL para detectar cortes horizontales en diseños largos y dividirlos en secciones lógicas.

ocr.py (Lector de Texto):

Intenta usar Google Cloud Vision si hay credenciales.

Hace fallback a Tesseract (local) si no hay API de Google.

Extrae texto crudo para alimentar el contexto de la IA.

ai_refine.py (El "Cerebro" Generativo):

Construye el prompt maestro para el LLM (Gemini/OpenAI).

Modo Estricto: Configurado con temperature=0.0 para evitar alucinaciones.

Multimodalidad: Codifica imágenes en Base64 y las envía al modelo para "clonación visual".

Parsea la respuesta JSON y escribe los archivos del tema (theme.json, templates/*.html, etc.).

wp_theme/prompts/ (Sistema de Conocimiento):

Contiene JSONs modulares (01_theme_json.json, patterns.json, etc.) que definen la estructura base de un tema de WordPress moderno.

runner.py: Un motor offline que puede construir un tema base usando solo estos JSONs sin necesidad de IA (útil para scaffolding rápido).

2. Configuración del Entorno de Desarrollo

Prerrequisitos

Python 3.10+

Tesseract OCR instalado en el sistema (y en el PATH).

(Opcional) Credenciales de Google Cloud Vision.

(Opcional pero recomendado) Clave de API de Google Gemini o OpenAI.

Instalación

Clonar el repositorio.

Crear entorno virtual: python -m venv venv y activarlo.

Instalar dependencias: pip install -r requirements.txt.

Configurar .env:

GOOGLE_API_KEY=tu_clave_aqui
# Opcional para OCR avanzado
GOOGLE_APPLICATION_CREDENTIALS=ruta/a/service-account.json


Ejecución

python app.py


El servidor iniciará en http://localhost:8000.

3. Flujo de Trabajo para Contribuidores

A. Mejorar la IA (Prompt Engineering)

Si deseas mejorar la calidad del código generado por la IA:

Edita ai_refine.py. Busca la variable prompt.

Modifica las instrucciones del sistema.

Tip: Mantén las instrucciones de "JSON válido" y "Fidelidad visual" muy claras.

Si agregas nuevos archivos al output (ej: sidebar.html), asegúrate de actualizar el validador _extract_json.

B. Mejorar el Análisis Visual (analyzer.py)

Para mejorar la detección de colores o la segmentación:

Colores: Modifica extract_design_dna. Puedes ajustar los umbrales de _is_grayscale o la lógica de selección del color "Primario" (actualmente busca el más saturado).

Slicing: La función segment_image usa detección de bordes y energía de filas. Puedes integrar modelos de ML como YOLO o SAM (Segment Anything) aquí para un recorte más inteligente de elementos UI.

C. Actualizar la Base de Conocimiento WordPress

El proyecto usa "semillas" JSON para construir la estructura del tema.

Para agregar nuevos Patrones: Edita wp_theme/patterns.json y agrega el archivo HTML correspondiente en wp_theme/patterns/.

Para cambiar los Estilos por Defecto: Edita wp_theme/theme.json.

4. Puntos de Extensión Futura

Ideas para desarrolladores que quieran llevar el proyecto al siguiente nivel:

Soporte para block.json:

Actualmente, el sistema genera Patrones HTML. El siguiente paso lógico es generar Bloques Nativos personalizados (React/JSX) registrando block.json y compilando el JS.

Integración con Figma API:

En lugar de subir un ZIP con imágenes, permitir conectar directamente a la URL de un archivo Figma, extraer los nodos como imágenes y procesarlos.

Vista Previa en Vivo:

Integrar un "visor" de WordPress (o un simulador de Gutenberg con wordpress/components) en el frontend de la app para ver el resultado antes de descargar el ZIP.

Refinamiento Iterativo (Chat con el Diseño):

Permitir al usuario escribir: "El header quedó muy alto, redúcelo" y re-ejecutar ai_refine.py con el contexto anterior para ajustar solo ese archivo.

5. Solución de Problemas Comunes

Error: "JSONDecodeError": La IA devolvió texto antes o después del JSON.

Solución: ai_refine.py tiene una función _extract_json que intenta limpiar bloques markdown. Revisa si el modelo está siendo muy "verboso" y ajusta el prompt para pedir "SOLO JSON".

Colores Incorrectos:

Solución: Verifica que la imagen tenga colores sólidos claros. analyzer.py puede confundirse con degradados complejos. Ajusta extract_design_dna.

Tesseract no encontrado:

Solución: Instala Tesseract Binary y asegúrate de que pytesseract pueda encontrar el ejecutable. En Windows, a veces requiere pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'.

Licencia: [Tu Licencia Aquí]
Mantenedor: [Tu Nombre/Equipo]