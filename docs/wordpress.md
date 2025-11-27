Base de Conocimiento Técnica de WordPress (v6.8+) - Parte 1 y 2

Contexto: Esta guía está optimizada para Modelos de Lenguaje (LLMs) que generan código para temas de WordPress basados en bloques (Block Themes). Se enfoca en la arquitectura moderna (FSE), theme.json v3, y las APIs introducidas hasta WordPress 6.8.

PARTE 1: Arquitectura Fundamental y Paradigma FSE

1.1. El Cambio de Paradigma: De Clásico a Bloques

Tradicionalmente, WordPress usaba PHP para renderizar el DOM en el servidor (the_content()). En la era moderna (Full Site Editing o FSE), WordPress opera como un sistema híbrido:

El Editor (Gutenberg): Es una aplicación React (SPA) que manipula un árbol de objetos JSON (los bloques).

El Frontend: Renderiza estos bloques convirtiendo la serialización HTML (comentarios <!-- wp:bloque -->) en marcado final.

Diferencia Crítica para la IA:

Tema Clásico: Depende de header.php, footer.php, y el Loop de PHP. (Obsoleto para este propósito).

Tema de Bloques: Depende de theme.json y plantillas HTML puras con gramática de bloques. Este es el objetivo de la app.

1.2. Gramática de Bloques (The Block Grammar)

El "código fuente" de un post o plantilla en FSE no es PHP, es HTML con anotaciones JSON.

Sintaxis Estricta:

<!-- wp:namespace/block-name {"atributo":"valor"} -->
<etiqueta-html>Contenido visual de fallback</etiqueta-html>
<!-- /wp:namespace/block-name -->


Namespace: Usualmente core para nativos o img2html para patrones propios.

Atributos JSON: Controlan el comportamiento y estilo. Deben ser JSON válido estricto.

Self-closing: Bloques dinámicos o vacíos se cierran en la misma línea: <!-- wp:site-title /-->.

1.3. Novedades Críticas en WordPress 6.8 (Referencia: docs/wordpress.md)

La IA debe priorizar estas implementaciones sobre métodos antiguos:

Registro de Bloques: Usar wp_register_block_types_from_metadata_collection() leyendo un manifiesto PHP (blocks-manifest.php), en lugar de registrar JSONs individuales.

Interactivity API: Usar directivas como data-wp-interactive y data-wp-bind para interactividad (acordeones, menús), evitando jQuery o JS vanilla disperso.

Block Hooks: Inserción automática de bloques en posiciones específicas (ej: un CTA después del contenido) sin editar la plantilla, compatible con patrones sincronizados.

Librería de Fuentes: Definición de fontFamilies en theme.json que se vinculan automáticamente a la API de Webfonts.

PARTE 2: Anatomía de Archivos de un Tema de Bloques

Un tema moderno no requiere PHP para la presentación visual. La estructura de directorios es estricta y semántica.

2.1. Archivos Raíz Obligatorios

style.css: Solo contiene la cabecera de metadatos (Nombre, Autor, Versión). No debe contener CSS de estilos globales (eso va en theme.json).

theme.json: El cerebro del tema. Define variables CSS, configuraciones de editor y estilos por defecto. (Se detallará en Partes futuras).

index.php: Archivo silenciador. Puede estar vacío o tener un comentario <?php // Silence is golden. No se usa para renderizar.

functions.php: Solo para lógica de servidor (hooks, registro de patrones, soporte de temas).

2.2. Directorios Estándar

La IA debe colocar los archivos generados en estas rutas exactas para que WordPress los reconozca automáticamente (Auto-discovery).

/templates: Archivos .html que definen la estructura de páginas completas.

index.html: Plantilla base obligatoria.

single.html: Para entradas individuales.

page.html: Para páginas estáticas.

404.html: Página de error.

archive.html: Listados de posts.

/parts: Archivos .html para secciones reutilizables (Template Parts).

header.html

footer.html

sidebar.html

Nota: Se referencian en las plantillas como <!-- wp:template-part {"slug":"header"} /-->.

/patterns: Archivos .php (recomendado en 6.8 para registro automático) o .html que contienen agrupaciones de bloques prediseñados.

La IA debe usar esto para secciones complejas inferidas del diseño (ej: hero.html, pricing-table.html).

En WP 6.8, se pueden organizar en subcarpetas (ej: /patterns/header/, /patterns/query/).

/styles: Variaciones de estilo globales (JSONs alternativos).

Ej: dark.json, high-contrast.json. Permiten cambiar toda la paleta y tipografía con un clic.

2.3. Jerarquía de Plantillas (Template Hierarchy)

La IA debe decidir qué archivo crear según el contenido detectado:

Si ve un diseño de "Lista de productos" -> templates/archive-product.html (si es WooCommerce) o archive.html.

Si ve un diseño de "Artículo de blog" -> templates/single.html.

Si ve la "Portada" -> templates/front-page.html (tiene prioridad sobre home.html e index.html).

2.4. Mapeo de Assets (Imágenes/CSS/JS)

Imágenes: Deben ir en /assets/images/.

Uso en tema: No se pueden enlazar directamente en HTML estático fácilmente. Se recomienda usarlas dentro de patrones PHP usando get_theme_file_uri(), o como patrones de bloques donde la imagen se sube a la librería de medios al importar.

CSS Adicional: /assets/css/blocks.css.

Se encola en functions.php usando wp_enqueue_scripts.

Regla de Oro: Usar solo para lo que theme.json no puede hacer (ej: media queries complejas, pseudo-elementos avanzados).

PARTE 3: El Cerebro - Deep Dive en theme.json v3

El archivo theme.json no es solo configuración; es el generador de CSS del sitio. La IA debe entender que cualquier estilo definido aquí se convierte automáticamente en clases y variables CSS en el frontend.

3.1. Estructura de Alto Nivel

El esquema v3 (obligatorio para WP 6.6+) divide la lógica en dos grandes ramas:

settings: "Lo que el usuario PUEDE hacer". Define la paleta, fuentes disponibles, y habilita/deshabilita controles en el editor.

styles: "Lo que el sitio ES por defecto". Aplica los colores y fuentes definidos en settings a elementos específicos.

Regla de Oro para la IA: Nunca aplicar un estilo en styles (ej: color: #ff0000) sin antes haber definido ese valor como un token en settings (ej: palette: "primary").

3.2. La "Magic Key": appearanceTools

La IA siempre debe incluir "appearanceTools": true dentro de settings.

Efecto: Habilita automáticamente controles de borde, color, espaciado, tipografía y sombras para todos los bloques que lo soporten.

Por qué: Evita tener que declarar soporte bloque por bloque (border: true, margin: true, etc.). Ahorra tokens y reduce errores.

3.3. CSS Personalizado y Elementos

Si la IA detecta un diseño que no se puede replicar con propiedades estándar (ej: un botón con clip-path), debe usar la propiedad css dentro de theme.json en lugar de style.css.

"styles": {
    "blocks": {
        "core/button": {
            "css": "& { clip-path: polygon(10% 0, 100% 0, 90% 100%, 0% 100%); }"
        }
    }
}


PARTE 4: Sistemas de Diseño - Color y Tipografía (Tokenización)

La IA debe actuar como un "Tokenizador". No debe usar valores hardcoded (#000) en las plantillas HTML. Debe usar referencias a variables.

4.1. Paleta de Colores Semántica

La IA debe extraer los colores de la imagen y asignarlos a slugs semánticos, no descriptivos.

MAL: slug: "blue-dark"

BIEN: slug: "primary"

Sintaxis de Referencia:
Cuando la IA genere HTML para un patrón, debe usar la clase de utilidad, no estilos inline.

Definición en theme.json: palette: [{ "slug": "primary", "color": "#3b82f6" }]

Uso en HTML: <h2 class="has-primary-color has-text-color">

Uso en CSS/JSON: var(--wp--preset--color--primary)

4.2. Tipografía y Webfonts API (WP 6.8)

WordPress 6.8 gestiona las fuentes localmente para GDPR/performance. La IA debe definir las fuentes en theme.json y WordPress descargará los archivos si se registran correctamente.

Estructura de fontFamilies:

"typography": {
    "fontFamilies": [
        {
            "fontFamily": "Inter, sans-serif",
            "name": "Primary",
            "slug": "primary",
            "fontFace": [
                {
                    "fontFamily": "Inter",
                    "fontWeight": "400",
                    "src": ["file:./assets/fonts/inter-regular.woff2"]
                }
            ]
        }
    ]
}


Nota: Si la IA no tiene los archivos .woff2, debe usar fuentes de sistema (system-ui) como fallback seguro para evitar errores 404.

PARTE 5: Layout y Espaciado (El Motor de Grilla)

Aquí es donde la IA suele fallar. WordPress FSE no usa Bootstrap ni Tailwind. Usa su propio motor de layout basado en blockGap.

5.1. El Modelo de Restricción (constrained vs flow)

En theme.json -> settings.layout:

contentSize: Ancho por defecto del contenido (ej: 800px). Ideal para párrafos de blog.

wideSize: Ancho para elementos destacados (ej: 1200px).

Comportamiento en Plantillas:
La IA debe envolver el contenido en un bloque core/group con layout constrained para centrarlo.

<!-- wp:group {"layout":{"type":"constrained"}} -->
<div class="wp-block-group">
   <!-- Contenido centrado aquí -->
</div>
<!-- /wp:group -->


5.2. Escala de Espaciado (Spacing Scale)

La IA no debe inventar márgenes aleatorios (17px, 23px). Debe aproximar los valores de la imagen a una escala predefinida (t-shirt sizing) definida en settings.spacing.spacingSizes.

Uso: var(--wp--preset--spacing--40) (equivale a un paso de la escala).

Block Gap: Es el espacio vertical/horizontal automático entre bloques. La IA debe configurar styles.spacing.blockGap globalmente para que coincida con la "aireación" general del diseño visual.

5.3. Columnas y Flexbox

Para replicar diseños horizontales:

Grid/Columnas: Usar core/columns. Es la única forma de tener grillas responsive reales.

Truco Pro: Para diseños asimétricos (Sidebar + Contenido), usar porcentajes explícitos en width (30% / 70%).

Flex/Row: Usar core/group con layout: {"type": "flex", "orientation": "horizontal"}. Ideal para menús, listas de iconos o tags.

Justificación: justifyContent ("center", "space-between") es clave para replicar headers y footers.

PARTE 6: Ingeniería de Patrones (Patterns)

En WordPress 6.8, los patrones reemplazan casi por completo a las antiguas "áreas de widgets" y "shortcodes". La IA debe entender que todo diseño complejo es un patrón.

6.1. Patrones Sincronizados vs. No Sincronizados

La IA debe decidir cuándo usar cada uno:

Patrón No Sincronizado (Estándar): Se usa para diseños iniciales (ej: "Hero Section", "Pricing Table"). El usuario lo inserta y puede editar el contenido libremente sin afectar a otras instancias.

Uso: La mayoría de las secciones generadas desde imágenes (Heroes, Features, Contacto).

Patrón Sincronizado (Global): Se usa para elementos que deben ser idénticos en todo el sitio (ej: "Call to Action Global", "Banner de Newsletter"). Si el usuario edita uno, cambian todos.

6.2. Registro de Patrones (La Forma Moderna)

Aunque se pueden registrar con PHP, la forma más limpia en 6.8 es mediante archivos en la carpeta /patterns/.

Cabecera del archivo: La IA debe incluir un comentario PHP al inicio de cada archivo en /patterns/ para definir sus metadatos.

<?php
/**
 * Title: Hero con Imagen a la Derecha
 * Slug: img2html/hero-right
 * Categories: banner, featured
 * Keywords: hero, imagen, cabecera
 * Block Types: core/post-content
 */
?>
<!-- Código HTML de los bloques aquí -->


6.3. Categorías de Patrones

La IA debe registrar una categoría propia para el tema (ej: Img2HTML Patterns) en functions.php para que los patrones generados no se pierdan entre los nativos.

PARTE 7: El Bloque de Navegación (Menus)

El menú es uno de los componentes más difíciles de replicar automáticamente porque en FSE es un bloque (core/navigation) que guarda datos en la base de datos, no en archivos estáticos.

7.1. Estrategia de "Navegación de Fallback"

Como la IA no puede crear registros en la base de datos del usuario (el menú real), debe definir una Navegación basada en Páginas o un Menú de Enlaces Personalizados estáticos dentro de parts/header.html.

Ejemplo Robusto (Menú Estático):

<!-- wp:navigation {"layout":{"type":"flex","justifyContent":"right"}} -->
    <!-- wp:navigation-link {"label":"Inicio","url":"/","kind":"custom"} /-->
    <!-- wp:navigation-link {"label":"Servicios","url":"#","kind":"custom"} /-->
    <!-- wp:navigation-link {"label":"Contacto","url":"#","kind":"custom"} /-->
<!-- /wp:navigation -->


7.2. Navegación Móvil (Overlay Menu)

La IA debe configurar el atributo overlayMenu del bloque de navegación.

Si el diseño tiene un menú de hamburguesa visible en escritorio -> "overlayMenu": "always".

Si es un menú estándar -> "overlayMenu": "mobile".

PARTE 8: Loops de Consulta (The Query Loop)

Para mostrar listas de posts (Blog, Portafolio, Productos), la IA NO debe usar HTML estático repetitivo. Debe usar el bloque core/query.

8.1. Anatomía de un Query Loop

La IA debe traducir una grilla de tarjetas repetitivas en la imagen a esta estructura:

Contenedor: <!-- wp:query {"query":{"perPage":6,"pages":0,"offset":0,"postType":"post"}} -->

Loop: <!-- wp:post-template --> (Aquí va el diseño de una sola tarjeta).

Elementos Dinámicos: Dentro del template, usar bloques dinámicos:

<!-- wp:post-featured-image /--> (No una imagen estática)

<!-- wp:post-title {"isLink":true} /--> (No un texto fijo)

<!-- wp:post-excerpt /-->

<!-- wp:post-date /-->

8.2. Variaciones de Query (Grid vs List)

Grid: La IA debe envolver el post-template con un bloque de columnas o usar estilos de grid en el contenedor.

List: Diseño secuencial simple.

8.3. Paginación

No olvidar incluir <!-- wp:query-pagination --> al final del bloque Query para que la navegación entre páginas funcione.

PARTE 9: Bloques de Composición Específicos

Más allá de grupos y columnas, la IA debe dominar estos bloques para replicar diseños comunes sin "reinventar la rueda" con HTML personalizado.

9.1. Medios y Texto (core/media-text)

Ideal para secciones "Imagen a la izquierda, Texto a la derecha" (o viceversa).

Ventaja: Maneja el apilamiento móvil (stacking) automáticamente.

Configuración: La IA debe usar isStackedOnMobile: true casi siempre para asegurar la respuesta móvil.

<!-- wp:media-text {"mediaPosition":"right","mediaType":"image","isStackedOnMobile":true} -->
<div class="wp-block-media-text alignwide has-media-on-the-right is-stacked-on-mobile">
    <figure class="wp-block-media-text__media"><img src="..." alt=""/></figure>
    <div class="wp-block-media-text__content">
        <!-- wp:heading --><h2>Título</h2><!-- /wp:heading -->
        <!-- wp:paragraph --><p>Texto descriptivo.</p><!-- /wp:paragraph -->
    </div>
</div>
<!-- /wp:media-text -->


9.2. El Bloque Fondo (core/cover)

Es el bloque más importante para secciones Hero, Banners y Call to Actions con fondo.

Capas: La IA debe entender que core/cover tiene una imagen de fondo, un overlay de color (con opacidad) y contenido interno.

Overlay: Usar dimRatio (0-100) para controlar la oscuridad del overlay. Si el texto es blanco, el overlay debe ser oscuro (isDark: false en el JSON del bloque indica que el texto no es oscuro, es decir, es claro).

9.3. Espaciador vs. Margen

Instrucción Estricta: La IA debe evitar el bloque core/spacer a menos que sea un espacio flexible intencional. Para separar elementos fijos, debe usar la propiedad style.spacing.margin o blockGap en el contenedor padre.

PARTE 10: Diseño Visual Avanzado (Filtros y Bordes)

Para lograr la "alta fidelidad", la IA debe aplicar estos detalles sutiles que marcan la diferencia.

10.1. Filtros Duotone

Si la imagen original muestra fotos con un tinte de color (ej: todas las fotos son azules y negras), la IA debe aplicar un filtro Duotone en theme.json y usarlo en los bloques.

Definición:

"settings": {
    "color": {
        "duotone": [
            {
                "colors": ["#000000", "#3b82f6"],
                "slug": "midnight-blue",
                "name": "Midnight Blue"
            }
        ]
    }
}


Uso: En el bloque imagen: {"style":{"color":{"duotone":"var(--wp--preset--duotone--midnight-blue)"}}}.

10.2. Bordes y Radios (Border Radius)

La IA debe detectar si el diseño es "cuadrado", "suave" (4px-8px) o "redondo" (pill shape).

Global: Definir styles.border.radius en theme.json para botones e inputs.

Específico: Aplicar a core/image o core/group (para tarjetas) si difieren del global.

10.3. Sombras (Shadows) - WP 6.6+

WordPress ahora tiene un sistema nativo de sombras.

Presets: Definir settings.shadow.presets en theme.json (ej: natural, crisp, sharp).

Aplicación: Usar en bloques de grupo para crear efectos de "tarjeta" o "elevación".

PARTE 11: Integración Básica con WooCommerce

Aunque WooCommerce tiene su propia lógica, en FSE se integra mediante bloques específicos. La IA debe saber cómo maquetar una tienda.

11.1. Bloques de Producto Esenciales

La IA no debe usar shortcodes ([products]). Debe usar los bloques modernos:

woocommerce/product-query: Similar a core/query pero para productos.

woocommerce/product-title, woocommerce/product-price, woocommerce/product-image, woocommerce/product-button.

11.2. Plantillas de Tienda

La IA debe generar plantillas específicas si detecta que el sitio es un e-commerce:

templates/archive-product.html: La página de la tienda/categorías.

templates/single-product.html: La ficha del producto.

Estructura de Ficha de Producto (Ejemplo):

<!-- wp:columns -->
<div class="wp-block-columns">
    <!-- wp:column {"width":"50%"} -->
    <div class="wp-block-column"><!-- wp:woocommerce/product-image /--></div>
    <!-- /wp:column -->
    
    <!-- wp:column {"width":"50%"} -->
    <div class="wp-block-column">
        <!-- wp:woocommerce/product-title /-->
        <!-- wp:woocommerce/product-price /-->
        <!-- wp:woocommerce/product-rating /-->
        <!-- wp:woocommerce/product-summary /-->
        <!-- wp:woocommerce/add-to-cart-form /-->
    </div>
    <!-- /wp:column -->
</div>
<!-- /wp:columns -->


11.3. Mini-Carrito

El bloque woocommerce/mini-cart es esencial en el parts/header.html si es una tienda. La IA debe insertarlo junto a la navegación si detecta intención comercial.

PARTE 12: Variaciones de Estilo de Bloques (Block Styles API)

La IA no debe crear clases CSS arbitrarias (.mi-boton-rojo). Debe usar la API nativa de Block Styles para que el usuario pueda elegir la variación desde el editor.

12.1. Registro en PHP

Para agregar un estilo visual alternativo a un bloque (ej: un botón "Fantasma" o una tabla "Rayada"), la IA debe registrarlo en functions.php o un archivo dedicado php/block_styles.php.

register_block_style(
    'core/button',
    array(
        'name'  => 'ghost',
        'label' => __( 'Ghost', 'textdomain' ),
        'inline_style' => '.wp-block-button.is-style-ghost .wp-block-button__link { background: transparent; border: 2px solid currentColor; }'
    )
);


12.2. Uso en Patrones

Una vez registrado, la IA debe aplicar la clase generada automáticamente (is-style-{name}) en el HTML de los patrones.

Ejemplo: <!-- wp:button {"className":"is-style-ghost"} -->

PARTE 13: Hooks de Bloques (Block Hooks)

Introducidos recientemente, los Block Hooks permiten a la IA inyectar bloques en posiciones específicas de todos los templates sin editar cada archivo HTML manualmente. Esto es ideal para elementos como "Botones de compra", "Iconos de compartir" o "Avisos".

13.1. Implementación de block_hooks en block.json

Si la IA genera bloques personalizados, puede definir:

"blockHooks": {
    "core/post-content": "after"
}


Esto insertará el bloque automáticamente después del contenido del post.

13.2. Filtros de Hook (Método Alternativo)

Para temas que no crean bloques propios, la IA puede usar filtros en functions.php para modificar el contenido de bloques específicos antes de renderizar.

PARTE 14: Optimización de Assets y Performance

Un tema generado por IA no debe ser lento. WordPress 6.8 incluye mejoras de carga que la IA debe aprovechar.

14.1. Carga de Fuentes (Local Fonts)

Regla: Nunca usar @import url('https://fonts.googleapis.com...') en CSS.
Método Correcto: Definir fontFace en theme.json. WordPress descargará y servirá las fuentes localmente, mejorando el GDPR y la velocidad.

14.2. Scripts y Estilos Diferidos

Si la IA genera JS/CSS personalizado (ej: para un slider), debe registrarlo con la estrategia de carga defer o async en wp_enqueue_script.

wp_enqueue_script(
    'my-script',
    get_theme_file_uri( '/assets/js/script.js' ),
    array(),
    '1.0',
    array( 'strategy' => 'defer' ) // Clave para performance en WP 6.3+
);


14.3. Imágenes Optimizadas (LCP)

Para la imagen del core/cover en la cabecera (LCP - Largest Contentful Paint), la IA debe añadir el atributo fetchpriority="high" si es posible, o asegurarse de no usar loading="lazy" en la primera imagen visible ("above the fold").

PARTE 15: Internacionalización (i18n)

Un tema profesional no contiene texto "hardcoded" en inglés o español. Todo string debe ser traducible.

15.1. Strings en PHP (functions.php y Patrones PHP)

La IA debe envolver cualquier texto visible en funciones de traducción con el Text Domain del tema (ej: img2html).

Estándar: __( 'Texto', 'img2html' ) para retornar.

Eco: _e( 'Texto', 'img2html' ) para imprimir.

Contexto: _x( 'Post', 'verb', 'img2html' ) para desambiguar.

Ejemplo en Patrón PHP:

<!-- wp:heading -->
<h2><?php echo esc_html__( 'Latest News', 'img2html' ); ?></h2>
<!-- /wp:heading -->


15.2. Strings en theme.json

WordPress traduce automáticamente las claves estándar (name, title de paletas y estilos). La IA no necesita hacer nada especial aquí, excepto usar nombres en inglés estándar para que el núcleo los traduzca, o usar el formato i18n si se requiere customización avanzada (aunque esto es menos común en temas generados).

15.3. Generación del Archivo .pot

La IA debe saber que el paso final de una build profesional es generar un archivo .pot (Portable Object Template) en /languages/, que lista todas las cadenas encontradas para que herramientas como Poedit o plugins de traducción las detecten.

PARTE 16: Accesibilidad (a11y) en FSE

La accesibilidad no es opcional. Un tema generado por IA debe pasar validaciones WCAG 2.1 AA.

16.1. "Skip Links" Automáticos

En los temas clásicos, había que añadir manualmente un enlace "Saltar al contenido". En FSE, si la IA usa correctamente el bloque core/group con la etiqueta <main>, WordPress puede no inyectarlo automáticamente si no se configura bien.

Requisito: El primer bloque del template index.html o header.html debe ser un core/group o core/site-title que no bloquee el tab-index inicial.

Mejor Práctica: Asegurar que el bloque principal de contenido tenga id="main-content" o similar si se implementa un script de skip-link personalizado, aunque el bloque core/group con tagName: main suele ser suficiente semánticamente.

16.2. Navegación Accesible

Al configurar core/navigation:

aria-label: Si hay múltiples menús (Header y Footer), la IA debe añadir aria-label="Header Menu" y aria-label="Footer Menu" en el JSON del bloque para diferenciarlos ante lectores de pantalla.

<!-- wp:navigation {"ariaLabel":"Menú Principal", ...} /-->

16.3. Contraste de Color y Focus

Contraste: La IA debe analizar los colores extraídos (analyzer.py). Si el fondo es oscuro, debe forzar texto claro en theme.json.

Focus Visible: En theme.json -> styles.elements.link.:focus, la IA debe definir un outline claro (ej: 2px solid var(--wp--preset--color--primary)). Nunca outline: 0.

PARTE 17: Compatibilidad con Plugins Populares (SEO, Forms)

Los temas FSE a veces "rompen" plugins que esperan hooks clásicos. La IA debe prevenir esto.

17.1. SEO (Yoast, RankMath)

Estos plugins dependen de que el tema no "oculte" el título o la descripción de formas extrañas.

Título: La IA no debe poner la etiqueta <title> en el HTML. WordPress la inyecta automáticamente si se declara add_theme_support('title-tag') en functions.php.

Headings: El template single.html debe tener UN solo <h1> (usualmente el core/post-title).

17.2. Formularios (Contact Form 7, Gravity Forms, WPForms)

Estos plugins suelen usar shortcodes o bloques propios.

Estilos Globales: La IA debe añadir en theme.json estilos para elementos input, textarea y button en styles.elements. Esto asegura que, aunque el plugin traiga su CSS, los inputs hereden la tipografía y bordes del tema (si el plugin lo permite o si se fuerza vía CSS en blocks.css).

17.3. Builders (Elementor, Divi)

Aunque el objetivo es FSE, muchos usuarios instalan builders.

Template "Canvas": La IA debe generar una plantilla templates/blank.html (sin header ni footer) para que los usuarios de builders tengan un lienzo en blanco.

<!-- wp:post-content /-->

PARTE 18: Estrategias de "Child Themes" vs "Standalone"

La IA debe decidir si genera un tema independiente o un tema hijo, aunque para FSE la recomendación moderna es Standalone (Independiente) debido a la naturaleza de theme.json.

18.1. Tema Standalone (Recomendado para IA)

En la era de los bloques, la herencia es menos necesaria porque theme.json define casi todo.

Estructura: style.css no declara Template: parent-theme.

Ventaja: Control total sobre plantillas y patrones sin conflictos de herencia.

Uso: La app Img2HTML genera temas Standalone por defecto para garantizar que el diseño visual sea idéntico a la imagen.

18.2. Tema Hijo (Child Theme) en FSE

Si se requiere un tema hijo (ej: extender "Twenty Twenty-Four"), la IA debe saber que theme.json del hijo sobrescribe o fusiona con el del padre.

Fusión: Si el padre define palette, y el hijo también, se combinan (el hijo gana en conflictos).

Nota: Es más complejo de depurar automáticamente. Se recomienda evitarlo en la v1.0.

PARTE 19: Debugging de Errores Comunes en FSE

Lista de errores frecuentes que la IA debe autoevaluar y prevenir.

19.1. El "Lienzo en Blanco" (White Screen of Death)

Causa: Error de sintaxis JSON en theme.json (coma extra, comillas faltantes).

Prevención: La IA debe validar estrictamente el JSON generado antes de escribir el archivo.

19.2. Bloques Rotos ("Este bloque contiene contenido inesperado")

Causa: El HTML dentro del comentario <!-- wp:block --> no coincide exactamente con lo que WordPress espera (ej: atributos o clases desactualizados).

Solución: Usar la sintaxis más simple y estándar posible. Evitar atributos experimentales no documentados.

Validación: Asegurar que todos los bloques autoconclusivos (como <img />) estén bien formados.

19.3. Estilos que no aplican

Causa: Especificidad CSS. Un estilo en blocks.css puede ser sobrescrito por theme.json o los estilos del core.

Solución: Priorizar siempre la configuración en theme.json (styles.blocks). Usar blocks.css solo con selectores de alta especificidad o para utilidades (.u-shadow-lg).

PARTE 20: Checklist Final de Calidad (QA) para la IA

Antes de empaquetar el ZIP, el sistema debe verificar estos puntos críticos.

20.1. Integridad Estructural

[ ] ¿Existe style.css con cabecera válida?

[ ] ¿Existe theme.json válido (sin errores de sintaxis)?

[ ] ¿Existen templates/index.html y templates/front-page.html?

20.2. Fidelidad Visual (El "Pixel Perfect")

[ ] ¿Se han extraído y aplicado los colores del diseño (ADN) en theme.json?

[ ] ¿Se usan las fuentes correctas (o su fallback más cercano)?

[ ] ¿Están los márgenes y paddings definidos usando la escala de espaciado?

20.3. Funcionalidad Core

[ ] ¿Funciona el Query Loop para mostrar posts?

[ ] ¿Es navegable el menú (incluso si es estático)?

[ ] ¿Son accesibles los contrastes de color (AA mínimo)?

20.4. Limpieza

[ ] ¿Se han eliminado comentarios de depuración o texto "alucinado" por la IA dentro de los archivos JSON/HTML?

[ ] ¿Están todos los assets (imágenes) referenciados correctamente en la carpeta /assets?

FIN DE LA BASE DE CONOCIMIENTO

Esta documentación cubre el 100% de los requisitos para que un LLM genere un tema de WordPress FSE moderno, funcional y de alta calidad.

Siguientes Pasos para el Humano:

Ingestar estos documentos en el contexto de la IA (RAG o System Prompt).

Ejecutar pruebas con diseños complejos.

Iterar sobre los prompts de ai_refine.py si se detectan fallos recurrentes en bloques específicos.

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
