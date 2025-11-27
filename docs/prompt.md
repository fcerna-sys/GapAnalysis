Prompt Maestro para Creación de Tema WordPress FSE (Full Site Editing)

Rol: Actúa como un Arquitecto de Software y Desarrollador Senior de WordPress, especializado en el desarrollo de temas de bloques (Block Themes), theme.json y los estándares más recientes de WordPress 6.7+.

Objetivo: Crear un tema de WordPress completo, minimalista y escalable basado en bloques, definiendo estilos globales y asegurando que todos los bloques nativos (Core Blocks) tengan un diseño coherente.

FASE 1: Configuración Global (theme.json)

Por favor, genera un archivo theme.json completo y detallado que incluya:

Schema Version: Versión 3.

Settings (Configuraciones):

Layout: Define contentSize (ej. 800px) y wideSize (ej. 1200px).

Typography: Habilita dropCap, fontStyle, fontWeight, textDecoration, etc. Define tamaños de fuente fluidos (usando clamp()).

Color Palette: Define una paleta semántica (Primary, Secondary, Background, Surface, Text, Accent).

Spacing: Define una escala de espaciado (spacing scale) para usar en márgenes y paddings.

Styles (Estilos Globales):

Typography: Asigna fuentes y alturas de línea para el body y encabezados (h1 a h6).

Elements: Estila elementos base como link (con estados :hover), button (sólidos y outline), y caption.

Block Styles (Estilos por Bloque - Cobertura Total):

Necesito que el theme.json defina estilos explícitos para TODAS las categorías de bloques nativos. No omitas ninguno:

Bloques de Texto: core/paragraph, core/heading, core/list, core/quote (con borde o ícono), core/code, core/preformatted, core/pullquote, core/table (con padding y bordes), core/verse.

Bloques de Medios: core/image, core/gallery, core/audio, core/cover (manejo de superposiciones), core/file, core/media-text, core/video.

Bloques de Diseño: core/button (y sus variaciones), core/columns, core/group (layouts flex/grid), core/more, core/separator (grosor y color), core/spacer.

Bloques de Widgets: core/archives, core/calendar, core/categories, core/latest-comments, core/latest-posts, core/search (input y botón integrados), core/social-icons, core/tag-cloud.

Bloques de Tema (FSE): core/site-logo, core/site-title, core/site-tagline, core/navigation, core/post-title, core/post-content, core/post-date, core/post-excerpt, core/post-featured-image, core/post-author, core/loginout, core/query-pagination.

Styles (Estilos Globales):

Typography: Asigna fuentes y alturas de línea para el body y encabezados (h1 a h6).

Elements: Estila elementos base como link (con estados :hover), button (sólidos y outline), y caption.

Block Styles (Estilos por Bloque):

Aquí es donde necesito cobertura total. Define estilos por defecto en el theme.json para:

core/button: Bordes, padding, transiciones.

core/quote: Estilo de borde izquierdo o comillas grandes.

core/code: Fondo gris suave y fuente monoespaciada.

core/table: Bordes colapsados y padding en celdas.

core/image: Bordes redondeados opcionales.

core/separator: Color y grosor.

core/navigation: Estilos para el menú.

FASE 2: Archivos de Estructura del Tema

Genera el código para los siguientes archivos esenciales:

style.css: Solo el encabezado de metadatos requerido por WordPress (Theme Name, Author, Description, Version, Requires at least, etc.).

functions.php:

Función para encolar (enqueue) estilos adicionales si fuera necesario (aunque priorizamos theme.json).

Registro de patrones de bloques personalizados si aplica.

Soporte para características del tema (add_theme_support).

FASE 3: Plantillas HTML (Block Templates)

Genera el código HTML con la sintaxis de comentarios de bloques de WordPress para las siguientes plantillas. Asegúrate de usar etiquetas semánticas (<main>, <header>, <footer>, <article>).

Partes de Plantilla (Template Parts):

parts/header.html: Logo del sitio, Título del sitio, Navegación.

parts/footer.html: Copyright, Enlaces sociales, Menú secundario.

Plantillas Principales:

templates/index.html: La plantilla por defecto. Debe incluir el header, un loop de consultas (Query Loop) para los posts, y el footer.

templates/single.html: Para entradas individuales. Debe mostrar Título, Imagen destacada, Contenido, Autor, Fecha y Navegación entre posts.

templates/page.html: Para páginas estáticas.

templates/404.html: Página de error con un buscador y mensaje amigable.

FASE 4: Componentes Visuales y Variaciones

Para asegurar que cubrimos "todos los componentes", por favor proporciona un archivo CSS adicional (blocks.css) o JSON extendido para casos borde que theme.json a veces no cubre bien, específicamente para:

Estilos de formularios (Inputs, Textarea, Submit).

Bloque de Galería (core/gallery).

Bloque de Archivo y Categorías (listas y dropdowns).

Bloque de Comentarios (Lista de comentarios, formulario de respuesta).

Nota Importante: Prioriza el uso de variables CSS generadas por WordPress (--wp--preset--color--primary, etc.) en todo el código personalizado.

Instrucciones de Salida:
Por favor, entrégame los archivos en bloques de código separados con su nombre de archivo correspondiente en la cabecera del bloque.
