OBJETIVO DEL SISTEMA (definición clara)

A partir de imágenes analizadas por IA, generar un tema WordPress que:

tenga estructura, bloques y estilos

pero además pre-cargue contenido dinámico real:

textos

imágenes

secciones

páginas

Todo eso insertado automáticamente en la base de datos al instalar el tema, mediante:

un script SQL o

un script SH (WP-CLI recomendado)

🧠 PRINCIPIO CLAVE (muy importante)

❌ NO guardar textos reales en el theme
✅ El theme solo define estructura y presentación

👉 Todo el contenido detectado en la imagen debe ir a la base de datos:

posts

pages

media

custom post types

block content (Gutenberg)

Esto es 100% correcto y profesional.

🧱 ARQUITECTURA PROPUESTA (visión general)
image → IA → data estructurada (JSON)
                    ↓
           ┌──────────────────┐
           │ theme generator  │ → theme WP (bloques, styles)
           └──────────────────┘
                    ↓
           ┌──────────────────┐
           │ content exporter │ → SQL o SH (WP-CLI)
           └──────────────────┘
                    ↓
             WordPress install

📦 1. FORMATO DE DATOS INTERMEDIO (CLAVE)

Antes de pensar en SQL o SH, todo lo que la IA detecta debe convertirse a un JSON estructurado.

📄 Ejemplo de content.json
{
  "pages": [
    {
      "slug": "home",
      "title": "Inicio",
      "template": "front-page",
      "blocks": [
        {
          "type": "hero",
          "data": {
            "title": "Creamos experiencias digitales",
            "subtitle": "Diseño moderno y escalable",
            "cta_text": "Contactanos",
            "cta_url": "/contacto"
          }
        },
        {
          "type": "card-grid",
          "items": [
            {
              "title": "Servicio 1",
              "text": "Descripción del servicio",
              "image": "service-1.jpg"
            }
          ]
        }
      ]
    }
  ]
}


📌 Este JSON es el contrato entre:

IA

generador de theme

generador de contenido

🧠 2. MAPEO IA → WORDPRESS (reglas claras)

Tu amigo debe respetar estas reglas:

📝 Textos detectados en la imagen

➡️ Van a bloques Gutenberg

wp:heading

wp:paragraph

wp:button

bloques custom del theme

Nunca hardcodeados en PHP.

🖼️ Imágenes detectadas
Flujo correcto:

Copiar imagen a:

/wp-content/uploads/YYYY/MM/


❌ NO dejarlas en /theme/assets/

Insertar en la DB:

wp_posts (post_type = attachment)

wp_postmeta (metadata imagen)

Usar el ID del attachment en los bloques

📌 Esto es obligatorio para:

responsive images

SEO

editor

🧰 3. FORMA RECOMENDADA DE INSERTAR CONTENIDO
⭐ OPCIÓN RECOMENDADA: WP-CLI (SH)

Mucho mejor que SQL puro.

📄 Ejemplo: import-content.sh
wp media import images/*.jpg --title="Hero Image"

wp post create \
  --post_type=page \
  --post_title="Inicio" \
  --post_name="home" \
  --post_status=publish \
  --post_content="$(cat home.blocks.html)"


✅ Ventajas:

WordPress se encarga de IDs

menos errores

portable

seguro

🧩 4. GENERACIÓN DE BLOQUES (HTML GUTENBERG)

Tu app debe generar contenido en formato Gutenberg, no HTML plano.

Ejemplo:
<!-- wp:mytheme/hero {"title":"Creamos experiencias digitales"} /-->

<!-- wp:paragraph -->
<p>Diseño moderno y escalable</p>
<!-- /wp:paragraph -->


Ese HTML:

se guarda en post_content

WordPress lo interpreta como bloques

📌 Clave para FSE real

🧬 5. MAPEO BLOQUE ↔ CONTENIDO

Define una tabla clara para el programador:

Bloque	Fuente IA	Destino WP
hero.title	texto grande	wp:heading
hero.subtitle	texto chico	wp:paragraph
hero.image	imagen	attachment + block attr
card.title	texto	wp:heading
card.text	texto	wp:paragraph

👉 Sin esto, el sistema se rompe.

🗃️ 6. DÓNDE SE INSERTA CADA COSA EN WP
📄 Páginas

wp_posts

post_type = page

📝 Posts / blog

wp_posts

post_type = post

🖼️ Imágenes

wp_posts → attachment

wp_postmeta → _wp_attached_file, _wp_attachment_metadata

🎨 Tema

solo estructura

nada de contenido real

🧩 7. EJECUCIÓN AUTOMÁTICA AL ACTIVAR EL THEME (opcional)

Si quieres algo más mágico:

add_action('after_switch_theme', function () {
  if (file_exists(get_theme_file_path('import-content.sh'))) {
    // mostrar instrucción o ejecutar vía WP-CLI
  }
});


⚠️ NO ejecutar SQL automáticamente sin confirmación.

📋 8. CHECKLIST (entregable)

Pásale esto tal cual:

✅ Debe hacer

Convertir salida IA → JSON estructurado

Generar bloques Gutenberg válidos

Insertar imágenes como attachments

Insertar páginas/posts por WP-CLI

Usar IDs reales de media

Mantener el theme libre de contenido

❌ No debe hacer

Hardcodear textos en PHP

Guardar imágenes solo en el theme

Usar HTML plano fuera de bloques

Insertar contenido directo con SQL sin WP

🏁 CONCLUSIÓN CLARA

Lo que estás planteando es:

🔥 Un generador de themes + contenido inicial tipo demo profesional

Eso:

es exactamente lo que hacen themes premium

está muy bien pensado

y tu arquitectura lo soporta perfectamente

Si quieres, en el próximo mensaje puedo:

escribir el pseudo-código exacto del importador

definir el esquema JSON final

o ayudarte a diseñar el WP-CLI completo

