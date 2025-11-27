Guía de WordPress 6.8 para desarrolladores
29/04/2025  ·  Actualizado el 05/11/2025  ·  12 min de lectura

PUBLICADO POR

Imagen del autor
Alvaro Gómez

Álvaro es conocido por sus habilidades para copiar y pegar código, una actividad en la que ha prosperado —y fracasado— desde finales de la década de 1990. Tras muchos años creando sitios en WordPress como profesional independiente y más tarde con su propia agencia, GIGA4, Álvaro trabaja actualmente como embajador de producto de WordPress.com en Automattic. Bilbaíno y padre de Julia y Clara
ARTÍCULOS RELACIONADOS

Optimización y limpieza avanzada de la base de datos para un WordPress saneado
Carlos Longarela

Conoce los modelos de WordPress Studio 1.6.0
Magdalena Oliva

WordPress 6.8, nombre en clave «Cecil», incluye un montón de nuevos caramelitos para desarrolladores. Esta actualización afecta a muchas secciones del código del núcleo de WordPress, incluyendo la biblioteca de bloques completa, el rendimiento y los patrones. Además, hay también gran cantidad de mejoras en la calidad de la experiencia a la hora de crear plugins y temas.

¡Vamos a verlas!

Si quieres consultar información más detallada de cada cambio, échale un vistazo a la WordPress 6.8 Field Guide oficial del blog Make WordPress Core.

Registro de tipos de bloques más eficiente
Secciones en el libro de estilos
Actualizaciones en la biblioteca de bloques
Herramientas de diseño en más bloques
Organización de patrones
Actualizaciones de la API
Seguridad: uso de bcrypt para el hash de contraseñas
Mejoras de rendimiento
Y tú, ¿qué vas a crear con WordPress 6.8?
Registro de tipos de bloques más eficiente
En la versión 6.8 de WordPress se ha eliminado la necesidad de registrar manualmente los tipos de bloques gracias a la nueva función wp_​register_​block_​types_​from_metadata_collection(). Es un wrapper del archivo blocks-manifest.php y la función wp_register_block_metadata_collection() que se introdujeron en la versión 6.7.

Como todos los datos de los bloques se almacenan en PHP en blocks-manifest.php, puedes registrar todos los tipos de bloques de tu plugin sin tener que leer archivos JSON individuales. En general, es una forma más eficiente de registrar los tipos de bloques. Y sí, ¡también lo puedes usar para registrar un tipo de bloque único!

En WordPress 6.8, puedes registrar todos tus tipos de bloques con esta llamada:

1
2
3
4
wp_register_block_types_from_metadata_collection(
    __DIR__ . '/build',
    __DIR__ . '/build/blocks-manifest.php'
);
Échale un vistazo a la entrada del blog Make WordPress Core para leer más información o descubre cómo puedes usarlo para dar soporte a versiones de WordPress más antiguas.

Secciones en el libro de estilos
La página de tipografías del libro de estilos en WordPress, donde se ven los conjuntos de fuentes a la izquierda y los estilos de los encabezados a la derecha.
Una de las mejoras más importantes de la versión 6.8 es la actualización de la interfaz del libro de estilos, que separa los ajustes del estilo en diferentes secciones. Puedes probar y ver cómo quedará la tipografía de tu sitio seleccionando los diferentes conjuntos de fuentes.

Hay también algunas mejoras más en el libro de estilos. Ahora tiene su propia ruta para que puedas enlazar directamente a él. La nueva ruta de la URL es /wp-admin/site-editor.php?p=%2Fstyles&preview=stylebook. Además, se ha añadido la compatibilidad del libro de estilos con temas clásicos.

Actualizaciones en la biblioteca de bloques
WordPress 6.8 introduce bastantes mejoras en la biblioteca de bloques, tanto incluyendo algunos nuevos como ampliando las funcionalidades de otros que ya existían.

Nuevo bloque: Total de la consulta
Un cuadro rosa señalando los resultados totales y el rango de visualización en el bloque Total de la consulta en WordPress.
En la versión 6.8 de WordPress se introduce un nuevo bloque ideal para compartir información sobre la búsqueda de entradas: Total de la consulta. Se utiliza dentro de un bloque Bucle de consulta y tiene dos opciones de visualización:

Resultados totales, donde aparece el número total de elementos encontrados en la búsqueda.
Rango de visualización, que muestra los resultados que aparecen en este momento dentro del total de los resultados.
Lightbox en la galería
Un cuadro verde señalando la opción Agrandar al hacer clic en WordPress.
WordPress 6.8 trae también el efecto de caja de luz al bloque Galería. Se trata de la misma funcionalidad que ya funcionaba en los bloques de imagen individuales. Para establecer el efecto lightbox en la galería, haz clic en el botón Enlace en la barra de herramientas y selecciona la opción Agrandar al hacer clic.

Hay que mencionar que esta función no crea una presentación con efecto de caja de luz donde se ven todas las imágenes de la galería: se limita a aplicar la función lightbox a los bloques de imagen individuales.

Bloque Detalles
Encabezado y descripción en un bloque Detalles de WordPress.
Ahora puedes agrupar varios bloques Detalles con el atributo HTML name. Si múltiples elementos <details> comparten el mismo atributo name, los navegadores cerrarán de forma automática un elemento abierto cuando se haya abierto otro, creando un efecto acordeón. Puedes establecer el atributo name en la sección Avanzado → Atributo de nombre de la barra lateral.

Además, el bloque Detalles ahora también es compatible con el anclaje HTML. Puedes encontrarlo en la sección Avanzado → Anclaje HTML.

Otras funcionalidades interesantes
La versión 6.8 de WordPress incluye también muchas pequeñas mejoras en otros bloques, como:

El bloque Navegación ahora puede incluir texto no interactivo en formato RichText en el bloque de enlace.
El bloque Separador se puede configurar como un elemento <div> para un uso decorativo (<hr> se utiliza para establecer una separación temática del contenido).
El bloque Archivo ahora admite que se edite solo el contenido, de forma que se pueda editar mientras forma parte de patrones bloqueados.
En el bloque Fondo se puede establecer una resolución de imagen específica (también en las imágenes destacadas).
El bloque Iconos sociales ahora tiene la opción de añadir Discord y su icono.
El bloque Bucle de consulta ha recibido un par de nuevas funciones:
Ahora se puede ordenar las páginas según el orden del menú, tanto ascendente como descendente.
También puedes ignorar las entradas fijas en las consultas personalizadas.
Cambios notables en el CSS de los bloques
En WordPress 6.8 se incluyen también algunas mejoras generales en el CSS, que, aunque es poco probable que cause errores en los diseños de los temas, merece la pena mencionar:

El bloque Botones ahora tiene aplicado box-sizing: border-box, lo que lo hace más consistente con los demás bloques.
Los estilos de overlay del bloque Imagen ahora se gestionan mediante una directiva data-wp-bind--style en lugar en una etiqueta <style> inline.
Herramientas de diseño en más bloques
Se han actualizado las herramientas de diseño de muchos bloques del núcleo, mejorando así la coherencia a la hora de aplicar opciones de estilos en los bloques.

Esto significa que estas opciones ahora aparecen en la interfaz del editor de dichos bloques. Pero, si en algún bloque no aparece la herramienta, siempre puedes configurar los estilos asociados en theme.json.

Los bloques Archivos, Categorías, Contenido y Lista de páginas ahora tienen acceso a más herramientas de colores. Y muchos bloques ahora tienen la posibilidad de editar opciones de bordes:

Archivos
Comentarios
Enlace de comentarios
Recuento de comentarios
Contenido
Últimas entradas
Lista de páginas
Total de la consulta
RSS
En los bloques Contenido, Lista de páginas y RSS ahora se pueden utilizar herramientas para diseñar los espaciados.

Si quieres ver la lista completa, échale un vistazo a la tabla de herramientas de diseño de cada bloque (edición WordPress 6.8).

Organización de patrones
Ahora es posible organizar los patrones de formas mucho más intuitivas y sencillas.

Añadir patrones a subcarpetas 
Si tu tema incluye muchos patrones, habrás podido notar que aparecen en la carpeta /patterns en lo que parece ser una lista infinita sin ningún orden aparente.

Con la versión 6.8 de WordPress, podrás navegar de forma más sencilla organizando tus patrones personalizados en subcarpetas dentro de /patterns.

Por ejemplo, podrías separar los patrones de cabecera y los de pie de página de tu tema de esta manera:

/patterns
    /header
        centered.php
        default.php
    /footer
        default.php
        links.php
Categoría de patrones de inicio
En la interfaz, los patrones que han sido asignados al tipo de bloque core/post-content (el método para registrar un patrón de inicio) aparecen en la categoría Contenido inicial. Sirve como complemento de otra actualización por la que todos los patrones aparecen en una lista en el insertador.

Si no quieres que aparezca la ventana modal que ofrece el contenido inicial en las páginas nuevas, puedes desactivar esta opción en el botón que hay en la parte inferior de la ventana, o desde la pantalla Editor → menú de 3 puntos → Preferencias.

En la nueva versión, los desarrolladores de temas pueden añadir patrones de contenido inicial en todos los tipos de bloques: entradas, páginas y cualquier tipo de entrada personalizada que hayas registrado.

Actualizaciones de la API
La versión 6.8 introduce también algunas mejoras de la API para ayudar a que el desarrollo sea más sólido y extensible. Con estos cambios, se optimiza la forma en que los desarrolladores interactúan con los datos, insertan bloques y trabajan con patrones.

Interactividad
Se ha mejorado la directiva wp-each para gestionar mejor los datos comprobando primero si una propiedad se puede iterar en lugar de intentar hacer una llamada a su método .map directamente. Esto evitará errores cuando se utilicen valores no iterables.

En el blog Make WordPress Core han recopilado una guía de consejos de la versión 6.8. Estas recomendaciones te ayudarán a que tu código esté actualizado con los estándares más recientes y a que puedas mejorar tus interacciones con la API.

Hooks de bloque
La API Block Hooks ha recibido dos importantes actualizaciones. La primera expande el mecanismo de los ganchos de bloque al contenido de las entradas, de forma que podrás insertar dinámicamente bloques enganchados directamente en páginas y entradas. La segunda actualización hace que los ganchos de bloques puedan funcionar con patrones sincronizados.

Seguridad: uso de bcrypt para el hash de contraseñas
En la versión 6.8, el algoritmo que utiliza WordPress para la función hash y el almacenamiento de contraseñas de los usuarios en la base de datos se ha cambiado a bcrypt.

Antes utiliza phpass, pero bcrypt refuerza la seguridad de las contraseñas, ya que es necesaria una mayor cantidad de potencia computacional para penetrar el hash de contraseñas.

Si tu plugin utiliza las funciones wp_hash_password() o wp_check_password(), lo normal es que siga funcionando como siempre. Pero si gestionabas los hashes de phpass directamente, tendrás que actualizar tu código.

Échale un vistazo a la nota de desarrollo de la actualización para ver más detalles. También encontrarás información sobre las nuevas funciones wp_fast_hash() y wp_verify_fast_hash() que permiten aplicar hash a una cadena generada aleatoriamente con suficiente entropía.

Mejoras de rendimiento
Para terminar, WordPress 6.8 incluye un montón de mejoras de rendimiento para todos los sitios.

Carga especulativa
Se ha introducido la carga especulativa, que permite a los navegadores compatibles precargar o preprocesar URL. Esto puede hacer que las páginas se carguen casi al instante, porque ya están listas antes de que el usuario haga clic en ellas.

Esta novedad salió por primera vez en abril de 2024 en forma de plugin llamado Speculative Loading. Desde entonces, los colaboradores han ido puliendo el código hasta que ha estado lo bastante maduro como para integrarlo directamente en el núcleo de WordPress.

Esta nueva función viene con varios ganchos de filtro para que puedas modificar cómo funciona la carga especulativa:

wp_speculation_rules_href_exclude_paths: para excluir patrones de URL de la carga especulativa.
wp_speculation_rules_configuration: para modificar la configuración de la carga especulativa.
wp_load_speculation_rules: para incluir más reglas a la carga especulativa.
Advertencias de rendimiento de useSelect
Cuando tienes activado SCRIPT_DEBUG (como suele hacerse en entornos de desarrollo), WordPress ahora mostrará advertencias de rendimiento en la consola cuando useSelect se utilice de forma que provoque re-renderizados innecesarios. Este cambio viene genial para aquellos que quieran ampliar el editor de bloques, ya que les ayudará a escribir código más optimizado.

Nuevo filtro para cargar assets de bloques bajo demanda
Antes de la versión 6.8, el gancho de filtro should_load_separate_block_assets tenía dos funciones:

Cargar hojas de estilo separadas para los bloques del núcleo, en lugar de usar siempre la hoja de estilos combinada wp-block-library que incluye todo el CSS de los bloques.
Cargar scripts y estilos solo cuando se usan en una página específica.
Con la versión 6.8, se ha añadido un nuevo filtro llamado should_load_block_assets_on_demand, que se encarga específicamente del segundo caso: determinar cuándo cargar los assets. El filtro original sigue funcionando como antes, pero ahora se recomienda utilizarlo solo para decidir si las hojas de estilo deben ir separadas.

Y tú, ¿qué vas a crear con WordPress 6.8?
WordPress 6.8 sigue haciendo avanzar el software con API más limpias, mejor rendimiento y herramientas más potentes para crear sitios. Tanto si estás creando temas, manteniendo plugins o probando nuevas funcionalidades del editor de bloques, esta versión hará tu trabajo más eficiente y tu código más fácil de gestionar.

Al crear tu web con WordPress.com, tendrás acceso a todo esto de manera