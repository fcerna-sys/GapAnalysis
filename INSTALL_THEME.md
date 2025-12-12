# Guía de Instalación del Tema en WordPress

## Método 1: Instalación Automática (Recomendado)

### Desde la Interfaz Web

1. **Genera el tema** desde la aplicación web
2. **Ve a la página de resultados** después de la conversión
3. **Usa el botón "Instalar en WordPress"** (si está disponible)
   - La aplicación detectará automáticamente WordPress en `wordpress/`
   - O especifica la ruta manualmente

### Desde la API

```bash
curl -X POST http://localhost:8001/install_theme \
  -d "wordpress_dir=C:/laragon/www/wordpress" \
  -d "theme_slug=mi-tema"
```

## Método 2: Instalación Manual

### Paso 1: Descargar el Tema

1. En la aplicación, haz clic en **"Descargar Tema"**
2. Se descargará un archivo `wp_theme.zip`

### Paso 2: Instalar en WordPress

1. **Accede a WordPress Admin**
   - Ve a `http://localhost/wordpress/wp-admin`
   - Inicia sesión

2. **Ve a Temas**
   - Apariencia → Temas
   - O `http://localhost/wordpress/wp-admin/themes.php`

3. **Añadir Nuevo Tema**
   - Haz clic en "Añadir nuevo"
   - Haz clic en "Subir tema"
   - Selecciona el archivo `wp_theme.zip`
   - Haz clic en "Instalar ahora"

4. **Activar el Tema**
   - Después de la instalación, haz clic en "Activar"

## Método 3: Instalación Manual (Carpeta)

### Copiar Directamente

1. **Extrae el ZIP** del tema
2. **Copia la carpeta** `wp_theme` a:
   ```
   wordpress/wp-content/themes/
   ```
3. **Renombra la carpeta** (opcional):
   ```
   wordpress/wp-content/themes/mi-tema/
   ```
4. **Activa el tema** desde WordPress Admin

### Usando Python

```python
from theme_builder import install_theme_to_wordpress

# Instalar tema
install_theme_to_wordpress(
    theme_dir='wp_theme',
    wordpress_dir='wordpress',
    theme_slug='mi-tema-personalizado'
)
```

## Verificación

Después de instalar, verifica:

1. **El tema aparece en la lista de temas**
   - Apariencia → Temas
   - Debe aparecer "Img2HTML AI Theme"

2. **Los patterns están disponibles**
   - Editor de bloques → Patterns
   - Debe aparecer la categoría "Img2HTML"
   - Deben aparecer los patterns generados

3. **Los colores están configurados**
   - Editor → Estilos
   - La paleta de colores debe coincidir con el diseño

4. **Los templates funcionan**
   - Crea una nueva página
   - Verifica que use el template correcto

## Solución de Problemas

### El tema no aparece

- Verifica que `style.css` tenga el header correcto
- Asegúrate de que `functions.php` exista
- Verifica permisos de archivos (755 para carpetas, 644 para archivos)

### Los patterns no aparecen

- Verifica que `patterns/` tenga archivos `.html`
- Revisa `functions.php` - debe tener `img2html_register_patterns()`
- Limpia cache de WordPress

### Los colores no se aplican

- Revisa `theme.json` → `settings.color.palette`
- Verifica que los slugs coincidan
- Limpia cache del navegador

### Errores PHP

- Revisa los logs de PHP
- Verifica sintaxis de `theme.json`
- Asegúrate de que todos los archivos requeridos existan

## Estructura Requerida

El tema debe tener al menos:

```
wp_theme/
├── style.css          # REQUERIDO - Header del tema
├── functions.php      # REQUERIDO - Funciones PHP
├── index.php          # REQUERIDO - Archivo de seguridad
└── theme.json         # Opcional pero recomendado - Config FSE
```

## Personalización Post-Instalación

Después de instalar, puedes:

1. **Personalizar colores** desde el editor de WordPress
2. **Editar templates** desde el editor de bloques
3. **Modificar patterns** desde Apariencia → Editor de patrones
4. **Agregar funciones** en `php/` (se cargan automáticamente)

## Notas

- El tema es compatible con WordPress 6.7+
- Requiere PHP 8.0+
- Es un tema de bloques (FSE) - no usa archivos PHP tradicionales para templates
- Los templates están en `templates/*.html` (formato FSE)




