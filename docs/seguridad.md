Seguridad — estado, riesgos y plan práctico

Resumen actual:
- No se ejecuta PHP autogenerado; se escriben archivos (reduce RCE).
- Sanitización activa en puntos críticos del pipeline: `sanitize_title`, `sanitize_text_field`, `wp_kses_post`, `check_admin_referer`, `current_user_can`.
- Carga condicional por manifest solo encola assets de bloques presentes.

Riesgos a vigilar:
- Normalización de slugs/prefijos: evitar path traversal y nombres no válidos.
- Uso de SQL directo: requiere revisión manual y respaldo antes de ejecutar.
- Validación de imágenes (si se habilitan uploads web): tamaño, MIME real y contenido.

Checklist de hardening WordPress:
- Desactivar XML-RPC y Application Passwords.
- Ocultar metadatos: `wp_generator`, `rsd_link`, `wlwmanifest_link`, `wp_shortlink_wp_head`, oEmbed host JS.
- Reducir feedback de login (mensajes genéricos).
- Bloquear edición de archivos desde el admin: `define('DISALLOW_FILE_EDIT', true);`.
- Mantener núcleo, plugins y tema al día.

Sanitización y validación en el tema:
- Prefijo BEM y slugs: usar limpiadores centralizados para slugs (`get_bem_prefix` y `PrefixManager._clean_slug`).
- Patterns: sanitizar HTML con `wp_kses_post` antes de registrar patrones.
- Contenido: usar `sanitize_title` y `sanitize_text_field`; escapar atributos y HTML en render (`esc_html`, `esc_attr`, `esc_url`).
- Nonces y permisos: exigir `current_user_can('manage_options')` y `check_admin_referer` en acciones administrativas.

Pipeline y assets:
- Validar clases BEM en build y fallar el pipeline si hay clases inválidas.
- Manifest de bloques: mantener rutas bajo `assets/blocks/components/` y usar `filemtime` como versión.
- En editor: encolar todo lo necesario; en frontend: filtrar por bloques usados.

SQL y WP-CLI:
- Preferir WP-CLI para crear contenido (`wp post create`) y importar media (`wp media import`).
- Si se usa el SQL generado, revisarlo, respaldar la base y ejecutar dentro de transacción.

Cabeceras HTTP recomendadas:
```
# Apache (.htaccess)
<IfModule mod_headers.c>
  Header always set X-Frame-Options "SAMEORIGIN"
  Header always set X-Content-Type-Options "nosniff"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set Permissions-Policy "geolocation=(), microphone=(), camera=()"
  Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains" env=HTTPS
</IfModule>

# Nginx (server)
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

Política CSP mínima (ajustar según fuentes reales):
```
Content-Security-Policy:
  default-src 'self';
  script-src 'self' 'unsafe-inline' 'unsafe-eval';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: blob: https:;
  font-src 'self' data: https:;
  connect-src 'self' https:;
  frame-ancestors 'self';
```

Permisos de archivos y rutas:
- `wp-content/uploads`: directorios `0755`, archivos `0644`.
- Tema y plugins: evitar escritura en producción; generar assets en build.
- No almacenar secretos en el repositorio; usarlos vía `wp-config.php`/variables de entorno.

Monitoreo y respuesta:
- Registrar intentos de login y cambios administrativos.
- Copias de seguridad periódicas y pruebas de restauración.
- Revisar logs de servidor/WordPress ante alertas y anomalías.

Acciones ya implementadas en el proyecto:
- Seguridad base en `wp_theme/php/security.php` (desactivaciones y filtros de cabecera de WP).
- Sanitización de patrones antes de registro.
- Validación BEM en el pipeline de build.
- Nonces y permisos en el generador del pipeline de contenido.

Siguientes pasos sugeridos:
- Añadir `DISALLOW_FILE_EDIT` en `wp-config.php` del entorno.
- Ajustar CSP a las fuentes reales del sitio y eliminar `'unsafe-inline'/'unsafe-eval'` cuando sea posible.
- Revisar y aprobar el SQL autogenerado antes de usarlo; preferir WP-CLI.

