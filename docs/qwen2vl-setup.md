# Guía de Configuración de Qwen2-VL

Esta guía explica cómo configurar y usar Qwen2-VL 7B Instruct con LM Studio para la aplicación img2html.

## ¿Qué es Qwen2-VL?

Qwen2-VL es un modelo de lenguaje multimodal de visión que puede:
- Analizar imágenes en detalle
- Extraer texto de imágenes (OCR)
- Entender componentes UI y layouts
- Generar código basado en análisis visual

## Ventajas de usar Qwen2-VL

1. **Ejecución local**: No necesitas APIs externas ni credenciales
2. **Privacidad**: Las imágenes nunca salen de tu máquina
3. **Costo**: Gratis después de la descarga inicial del modelo
4. **Control**: Tienes control total sobre el modelo y su configuración

## Requisitos

- LM Studio instalado (https://lmstudio.ai)
- Al menos 8GB de RAM (recomendado 16GB)
- Modelo Qwen2-VL-7B-Instruct-GGUF-Q4_K_M (~4.5GB)

## Instalación Paso a Paso

### 1. Instalar LM Studio

1. Descarga LM Studio desde https://lmstudio.ai
2. Instala la aplicación
3. Abre LM Studio

### 2. Descargar el Modelo

1. En LM Studio, ve a la pestaña "Search"
2. Busca "Qwen2-VL-7B-Instruct"
3. Selecciona la versión **GGUF Q4_K_M** (recomendada)
4. Haz clic en "Download"
5. Espera a que se complete la descarga (~4.5GB)

### 3. Cargar el Modelo

1. Ve a la pestaña "Chat" o "Local Server"
2. Selecciona el modelo "Qwen2-VL-7B-Instruct" de la lista
3. El modelo se cargará en memoria (puede tardar unos minutos la primera vez)

### 4. Activar el Servidor API

1. En LM Studio, ve a "Local Server" (o "Server" en versiones anteriores)
2. Asegúrate de que el servidor esté activo
3. Verifica que el puerto sea **1234** (o anota el puerto que uses)
4. El endpoint será: `http://localhost:1234/v1/chat/completions`

### 5. Configurar la Aplicación

Crea o edita el archivo `.env` en la raíz del proyecto:

```env
# Configuración de LM Studio (opcional, estos son los valores por defecto)
LM_STUDIO_ENDPOINT=http://localhost:1234/v1/chat/completions
LM_STUDIO_MODEL=qwen2-vl-7b-instruct
```

## Uso

### OCR con Qwen2-VL

La aplicación usará automáticamente Qwen2-VL para OCR cuando:
- No hay credenciales de Google Vision en `.env`
- LM Studio está activo y accesible

**Orden de prioridad:**
1. Google Vision (si hay credenciales)
2. Qwen2-VL vía LM Studio
3. Tesseract (fallback)

### Generación de Temas con Qwen2-VL

Para usar Qwen2-VL en la generación de temas:

1. Edita `wp_theme/prompts/runtime.json`
2. Asegúrate de que el modelo LM Studio esté habilitado:

```json
{
  "remote_models": [
    {
      "name": "qwen2-vl-7b-instruct",
      "provider": "lmstudio",
      "endpoint": "http://localhost:1234/v1/chat/completions",
      "tokens": [],
      "enabled": true
    }
  ]
}
```

3. La aplicación usará Qwen2-VL automáticamente según la estrategia configurada

## Optimizaciones

### Reducción de Tamaño de Imágenes

La aplicación optimiza automáticamente las imágenes antes de enviarlas:
- Redimensiona imágenes grandes (máx 2048x2048px)
- Comprime a JPEG con calidad 85%
- Reduce significativamente el tamaño del payload

### Análisis Visual Profundo

Puedes habilitar análisis visual más profundo en `analyzer.py`:

```python
from analyzer import enhance_section_with_vision

# Enriquecer una sección con análisis visual
section = enhance_section_with_vision(section, use_qwen2vl=True)
```

Esto detectará:
- Componentes UI (botones, cards, navegación)
- Tipografías y tamaños
- Layouts y columnas
- Colores exactos
- Espaciados y márgenes

## Solución de Problemas

### El modelo no responde

1. Verifica que LM Studio esté ejecutándose
2. Verifica que el servidor API esté activo
3. Comprueba el puerto en la configuración
4. Revisa los logs de LM Studio

### Respuestas lentas

1. Reduce el tamaño máximo de imágenes en `ai_refine.py`:
   ```python
   _optimize_image_for_ai(image_path, max_width=1024, max_height=1024)
   ```
2. Usa un modelo más pequeño (Q4_K_M es un buen balance)
3. Cierra otras aplicaciones que usen RAM

### Errores de JSON

La aplicación tiene validación robusta de JSON y fallbacks automáticos:
- Si Qwen2-VL falla, intenta con Google Gemini (si está disponible)
- Si ambos fallan, usa el fallback básico sin IA

### El modelo no detecta bien los colores

1. Asegúrate de que las imágenes tengan buena calidad
2. Verifica que las imágenes no estén demasiado comprimidas
3. Considera usar análisis visual profundo para mejor detección

## Mejores Prácticas

1. **Mantén LM Studio activo**: El modelo tarda en cargar, es mejor dejarlo activo
2. **Usa imágenes optimizadas**: La aplicación las optimiza automáticamente, pero imágenes muy grandes pueden ser lentas
3. **Monitorea la RAM**: Qwen2-VL usa bastante memoria, asegúrate de tener suficiente
4. **Prueba primero con pocas imágenes**: Para verificar que todo funciona correctamente

## Comparación con Otros Modelos

| Característica | Qwen2-VL | Google Vision | Tesseract |
|----------------|----------|---------------|-----------|
| Ejecución | Local | Cloud | Local |
| Costo | Gratis | Pago | Gratis |
| Privacidad | Alta | Baja | Alta |
| Calidad OCR | Alta | Muy Alta | Media |
| Análisis Visual | Sí | Sí | No |
| Requisitos | 8GB+ RAM | API Key | Instalación local |

## Recursos Adicionales

- [Documentación de Qwen2-VL](https://github.com/QwenLM/Qwen2-VL)
- [LM Studio Documentation](https://lmstudio.ai/docs)
- [Guía de WordPress FSE](docs/wordpress.md)



