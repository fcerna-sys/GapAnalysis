# Guía de Construcción de Temas WordPress

Esta guía explica cómo se construye el tema WordPress FSE desde las imágenes.

## Proceso de Construcción

### 1. Análisis de Imágenes
- **analyzer.py**: Analiza las imágenes y detecta secciones, patrones, colores
- **ocr.py**: Extrae texto de las imágenes (Google Vision / Qwen2-VL / Tesseract)
- **Análisis visual**: Qwen2-VL analiza componentes UI, layouts, tipografías

### 2. Generación del Plan
El plan contiene:
- Secciones detectadas con sus imágenes
- Patrones identificados (hero, features, etc.)
- Layout rows con columnas y proporciones
- Paleta de colores (DNA)

### 3. Construcción del Tema

#### Archivos Generados

**style.css**
- Header del tema con metadatos
- Variables CSS con colores del DNA
- Estilos base y mejoras de accesibilidad

**theme.json**
- Configuración del tema FSE
- Paleta de colores
- Tipografías
- Espaciados y layouts

**templates/**
- `front-page.html`: Página principal basada en el plan
- `index.html`: Template por defecto
- `page.html`: Template para páginas
- `single.html`: Template para posts
- Otros templates según necesidad

**parts/**
- `header.html`: Header del sitio
- `footer.html`: Footer del sitio
- Otros template parts según necesidad

**patterns/**
- Patterns generados desde cada sección del plan
- Patterns basados en patrones detectados (hero, features, etc.)

**functions.php**
- Carga archivos PHP adicionales
- Registro de patterns
- Funciones del tema

### 4. Mejoras con theme_builder.py

El módulo `theme_builder.py` añade:

- **generate_style_css()**: Genera style.css completo con colores del DNA
- **enhance_theme_with_plan()**: Crea patterns desde las secciones
- **generate_pattern_from_section()**: Genera HTML FSE desde una sección
- **update_patterns_json()**: Actualiza patterns.json
- **update_theme_json_colors()**: Actualiza colores en theme.json
- **ensure_theme_structure()**: Asegura estructura completa
- **build_complete_theme()**: Construye tema completo
- **install_theme_to_wordpress()**: Instala tema en WordPress

## Instalación del Tema

### Opción 1: Manual
1. Descarga el ZIP del tema desde la aplicación
2. Ve a WordPress Admin → Apariencia → Temas
3. Añadir nuevo → Subir tema
4. Selecciona el ZIP y activa el tema

### Opción 2: Automática (Nueva)
1. Asegúrate de que WordPress esté en `wordpress/` relativo al proyecto
2. Usa la ruta `/install_theme` (POST) con:
   - `wordpress_dir`: Ruta a WordPress (opcional, se detecta automáticamente)
   - `theme_slug`: Nombre del tema (opcional)

### Opción 3: Desde código
```python
from theme_builder import install_theme_to_wordpress

install_theme_to_wordpress(
    theme_dir='wp_theme',
    wordpress_dir='wordpress',
    theme_slug='mi-tema'
)
```

## Estructura del Tema Generado

```
wp_theme/
├── style.css              # Header y estilos base
├── functions.php          # Funciones PHP
├── theme.json            # Configuración FSE
├── index.php             # Archivo requerido
├── templates/            # Templates FSE
│   ├── index.html
│   ├── front-page.html
│   ├── page.html
│   └── single.html
├── parts/                # Template parts
│   ├── header.html
│   └── footer.html
├── patterns/             # Block patterns
│   ├── hero.html
│   ├── features.html
│   └── ...
├── php/                  # Archivos PHP adicionales
├── assets/               # Recursos (imágenes, etc.)
└── patterns.json         # Catálogo de patterns
```

## Personalización

### Colores
Los colores se extraen del DNA y se aplican en:
- `theme.json` → `settings.color.palette`
- `style.css` → Variables CSS
- Patterns y templates

### Patterns
Cada sección del plan genera un pattern en `patterns/`:
- Nombre basado en el slug de la sección
- Estructura basada en el tipo de patrón detectado
- Colores y estilos del DNA

### Templates
- `front-page.html`: Generado desde el plan completo
- Otros templates: Basados en catálogos o generados por IA

## Mejoras con Qwen2-VL

Cuando Qwen2-VL está disponible:
- Análisis visual profundo mejora la detección de componentes
- Colores más precisos extraídos de las imágenes
- Mejor detección de layouts y espaciados
- Patterns más fieles al diseño original

## Troubleshooting

### El tema no aparece en WordPress
- Verifica que `style.css` tenga el header correcto
- Asegúrate de que `functions.php` exista
- Verifica permisos de archivos

### Los colores no se aplican
- Revisa `theme.json` → `settings.color.palette`
- Verifica que los slugs coincidan
- Limpia cache de WordPress

### Los patterns no aparecen
- Verifica `patterns.json`
- Asegúrate de que los archivos HTML existan en `patterns/`
- Revisa que `functions.php` registre los patterns

### El tema tiene errores
- Revisa los logs de PHP
- Verifica sintaxis de `theme.json`
- Asegúrate de que todos los archivos requeridos existan



