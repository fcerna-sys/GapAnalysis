# GapAnalysis

Motor de IA avanzado para transformar diseños visuales (PNG/JPG de Figma, Photoshop o capturas) en temas WordPress Full Site Editing (FSE) funcionales, accesibles y semánticos. A diferencia de convertidores tradicionales, entiende el diseño y lo replica con alta fidelidad.

## Características

- Clonación visual estricta (Nuclear Mode) con prioridad absoluta a referencias visuales.
- Multimodalidad real: envía imágenes a modelos de visión (Gemini 1.5 Pro / GPT‑4 Turbo / Qwen2-VL) como fuente de verdad.
- **Soporte para Qwen2-VL 7B Instruct**: Usa LM Studio para ejecutar Qwen2-VL localmente sin necesidad de APIs externas.
  - OCR con Qwen2-VL cuando no hay credenciales de Google Vision
  - Generación de temas WordPress usando análisis visual profundo
  - Análisis de componentes UI, tipografías, layouts y espaciados
- Temperatura cero: ejecución determinista para evitar alucinaciones y respetar columnas/espaciados.
- Segmentación 2D (filas y columnas) y cálculo de proporciones (`ratios_percent`).
- Detección de patrones y variantes (hero split-screen balanceado vs asimétrico).
- Paleta de colores (DNA) robusta: ignora grises, incluye `primary` y `secondary`.
- Generación de layout FSE con `core/cover`, `core/columns`, `core/group`, respetando micro-espaciados (`blockGap`, `padding`).
- Overlay del hero calculado con paleta y luminancia; contraste automático de texto.
- Detección heurística de `border-radius` y aplicación global en CSS y contenedores.
- Tolerante a respuestas de IA: limpieza de markdown, extracción de JSON confiable.
- Optimización automática de imágenes: redimensiona y comprime antes de enviar a la IA.

## Requisitos

- Python 3.10+
- Dependencias:
  - Flask, Pillow, python-dotenv, requests
  - colorgram.py (extracción de paleta)
  - opencv-python-headless (segmentación y heurísticas visuales)
  - google-generativeai (opcional), google-cloud-vision/pytesseract (OCR opcional)
 - Tesseract OCR instalado en el sistema y disponible en `PATH` (si se usa OCR local).
 - **LM Studio** (opcional pero recomendado): Para usar Qwen2-VL 7B Instruct localmente
   - Descarga e instala LM Studio desde https://lmstudio.ai
   - Carga el modelo Qwen2-VL-7B-Instruct-GGUF-Q4_K_M
   - Asegúrate de que el servidor API esté activo (puerto 1234 por defecto)

Instalación:

```
pip install -r requirements.txt
```

Si tu entorno trae `opencv-python` de escritorio, cámbialo por `headless`:

```
pip uninstall -y opencv-python
pip install opencv-python-headless
```

## Configuración

- Define `.env` con tus claves según `wp_theme/prompts/runtime.json`.
- Variables típicas:
  - `GOOGLE_API_KEY` (Gemini)
  - `OPENAI_API_KEY` (OpenAI)
  - `GOOGLE_APPLICATION_CREDENTIALS` (ruta al Service Account para Vision)
  - `OLLAMA_ENDPOINT` (si usas runner local)
  - **`LM_STUDIO_ENDPOINT`** (opcional): Endpoint de LM Studio (por defecto: `http://localhost:1234/v1/chat/completions`)
  - **`LM_STUDIO_MODEL`** (opcional): Nombre del modelo en LM Studio (por defecto: `qwen2-vl-7b-instruct`)

### Configuración de Qwen2-VL con LM Studio

1. **Instala LM Studio**: Descarga desde https://lmstudio.ai
2. **Carga el modelo**: 
   - Busca "Qwen2-VL-7B-Instruct" en LM Studio
   - Descarga la versión GGUF Q4_K_M (recomendada para balance entre calidad y rendimiento)
   - Carga el modelo en LM Studio
3. **Activa el servidor API**:
   - En LM Studio, ve a "Local Server"
   - Asegúrate de que el servidor esté activo (puerto 1234 por defecto)
4. **Configuración opcional en `.env`**:
   ```env
   LM_STUDIO_ENDPOINT=http://localhost:1234/v1/chat/completions
   LM_STUDIO_MODEL=qwen2-vl-7b-instruct
   ```

**Orden de prioridad para OCR:**
1. Google Vision (si hay credenciales en `.env`)
2. Qwen2-VL vía LM Studio (si no hay credenciales de Google Vision)
3. Tesseract (fallback final)

**Orden de prioridad para generación de temas:**
1. Modelo configurado en `runtime.json` (Google/OpenAI/LM Studio)
2. Google Gemini (si hay API key)
3. Fallback básico sin IA

## Uso

1. Inicia la app Flask y abre la UI (`http://localhost:8001`).
2. Sube un ZIP con imágenes del diseño.
3. Activa “Slicing” (preciso) para columnas con proporciones.
4. Convierte y descarga:
   - Tema FSE (`wp_theme.zip`)
   - Sitio estático para previsualización rápida (`static_site.zip`)

## Pruebas

Ejecuta pruebas de unidad:

```
pytest -q
```

## Notas

- La fusión de paleta `DNA` se inyecta en `theme.json` para que el editor y los patrones usen los colores reales del diseño.
- El overlay del hero usa `primary` o `secondary` según luminancia; el texto se ajusta automáticamente para legibilidad.
- La detección de `border-radius` es heurística; si no es detectable, usa un valor seguro.

## Estructura del Proyecto

- `app.py`: Servidor Flask y orquestador del proceso.
- `ai_refine.py`: Lógica de prompts y conexión con LLMs (el "Cerebro").
  - Soporte para Google Gemini, OpenAI, Ollama y LM Studio (Qwen2-VL)
  - Prompts optimizados específicamente para Qwen2-VL
  - Optimización automática de imágenes antes de enviar
  - Validación robusta de JSON y manejo de errores con fallbacks
- `analyzer.py`: Análisis visual y segmentación (el "Ojo").
  - Análisis visual profundo con Qwen2-VL (opcional)
  - Detección de componentes UI, tipografías, layouts
  - Segmentación 2D y cálculo de proporciones
- `ocr.py`: Extracción de texto (Google Vision / Qwen2-VL / Tesseract).
  - Prioridad: Google Vision → Qwen2-VL → Tesseract
  - Optimización de imágenes para OCR
- `wp_theme/`: Plantilla base y catálogo de prompts (`wp_theme/prompts/`) para estructuras canónicas.

## Contribución

- Las contribuciones son bienvenidas. Revisa `docs/` para entender la arquitectura:
  - `docs/wordpress.md`: Guía de referencia FSE 6.8.
  - `docs/manual.md`: Manual técnico para desarrolladores.
  - `docs/prompt.md`: Contrato de salida y guía de prompt para la IA.

## Licencia

[Tu Licencia Aquí] — v1.0