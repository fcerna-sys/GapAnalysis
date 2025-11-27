# GapAnalysis

Aplicación para clonar diseños desde imágenes a un tema WordPress FSE con extrema fidelidad visual.

## Características

- Clonación visual estricta (Modo Estricto) con prioridad a referencias visuales.
- Segmentación 2D (filas y columnas) y cálculo de proporciones (`ratios_percent`).
- Detección de patrones y variantes (hero split-screen balanceado vs asimétrico).
- Paleta de colores (DNA) robusta: ignora grises, incluye `primary` y `secondary`.
- Generación de layout FSE con `core/cover`, `core/columns`, `core/group`, respetando micro-espaciados (`blockGap`, `padding`).
- Overlay del hero calculado con paleta y luminancia; contraste automático de texto.
- Detección heurística de `border-radius` y aplicación global en CSS y contenedores.
- Tolerante a respuestas de IA: limpieza de markdown, extracción de JSON confiable.

## Requisitos

- Python 3.10+
- Dependencias:
  - Flask, Pillow, python-dotenv
  - colorgram.py (extracción de paleta)
  - opencv-python-headless (segmentación y heurísticas visuales)
  - google-generativeai (opcional), google-cloud-vision/pytesseract (OCR opcional)

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

## Uso

1. Inicia la app Flask y abre la UI.
2. Sube un ZIP con imágenes del diseño.
3. Activa “Slicing” (preciso) para columnas con proporciones.
4. Convierte y descarga el tema FSE.

## Pruebas

Ejecuta pruebas de unidad:

```
pytest -q
```

## Notas

- La fusión de paleta `DNA` se inyecta en `theme.json` para que el editor y los patrones usen los colores reales del diseño.
- El overlay del hero usa `primary` o `secondary` según luminancia; el texto se ajusta automáticamente para legibilidad.
- La detección de `border-radius` es heurística; si no es detectable, usa un valor seguro.