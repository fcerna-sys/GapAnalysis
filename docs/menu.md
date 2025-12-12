OBJETIVO GENERAL

Implementar un sistema de menú que:

Use el gestor de menús nativo de WordPress (drag & drop, niveles ilimitados)

Permita agregar campos personalizados por cada ítem del menú:

Icono (clase CSS o SVG)

Título alternativo (title)

Descripción corta

Tipografía específica (opcional)

Color de texto (opcional)

Badge (ej: "Nuevo", “Promo”, etc.)

Los guarde como meta en cada ítem del menú

Los imprima en el frontend usando un custom Walker

Sea compatible con cualquier estructura del tema

🧩 1. Registrar los menús en el tema

Archivo: functions.php

function app_register_menus() {
    register_nav_menus([
        'primary_menu' => __('Menú Principal', 'app'),
        'footer_menu'  => __('Menú Footer', 'app'),
    ]);
}
add_action('init', 'app_register_menus');


Con esto WordPress ya habilita:

Crear menús

Ordenar con arrastrar y soltar

Crear submenús

🧩 2. Agregar campos personalizados al editor de ítems del menú

WordPress permite insertar campos personalizados usando el hook:

wp_nav_menu_item_custom_fields


Archivo sugerido:
/inc/menu/custom-fields.php (solo como organización)

add_action('wp_nav_menu_item_custom_fields', function($item_id, $item) {
    
    $icon  = get_post_meta($item_id, '_menu_icon', true);
    $badge = get_post_meta($item_id, '_menu_badge', true);
    $color = get_post_meta($item_id, '_menu_color', true);

    ?>
    
    <p class="description description-wide">
        <label>
            Icono (clase CSS o SVG)
            <input type="text" name="menu_icon[<?php echo $item_id; ?>]" value="<?php echo esc_attr($icon); ?>" />
        </label>
    </p>
    
    <p class="description description-wide">
        <label>
            Badge
            <input type="text" name="menu_badge[<?php echo $item_id; ?>]" value="<?php echo esc_attr($badge); ?>" />
        </label>
    </p>

    <p class="description description-wide">
        <label>
            Color del texto (CSS)
            <input type="text" name="menu_color[<?php echo $item_id; ?>]" value="<?php echo esc_attr($color); ?>" placeholder="#000000" />
        </label>
    </p>

    <?php
}, 10, 2);


Esto hará que aparezcan esos campos debajo de cada ítem del menú.

🧩 3. Guardar los valores personalizados

WordPress guarda los meta de los ítems del menú con:

update_post_meta


Archivo: mismo archivo de arriba.

add_action('wp_update_nav_menu_item', function($menu_id, $menu_item_db_id) {

    if (isset($_POST['menu_icon'][$menu_item_db_id])) {
        update_post_meta($menu_item_db_id, '_menu_icon', sanitize_text_field($_POST['menu_icon'][$menu_item_db_id]));
    }

    if (isset($_POST['menu_badge'][$menu_item_db_id])) {
        update_post_meta($menu_item_db_id, '_menu_badge', sanitize_text_field($_POST['menu_badge'][$menu_item_db_id]));
    }

    if (isset($_POST['menu_color'][$menu_item_db_id])) {
        update_post_meta($menu_item_db_id, '_menu_color', sanitize_hex_color($_POST['menu_color'][$menu_item_db_id]));
    }

}, 10, 2);

🧩 4. Crear el Custom Walker para imprimir todo

Archivo sugerido:
/inc/menu/class-app-walker.php

class App_Walker_Nav_Menu extends Walker_Nav_Menu {

    public function start_el(&$output, $item, $depth = 0, $args = [], $id = 0) {

        $icon  = get_post_meta($item->ID, '_menu_icon', true);
        $badge = get_post_meta($item->ID, '_menu_badge', true);
        $color = get_post_meta($item->ID, '_menu_color', true);

        $color_style = $color ? 'style="color:' . esc_attr($color) . ';"' : '';

        $output .= '<li class="menu-item">';

        $output .= '<a href="' . esc_attr($item->url) . '" ' . $color_style . '>';

        // ICON
        if ($icon) {
            $output .= '<span class="menu-icon ' . esc_attr($icon) . '"></span> ';
        }

        // LABEL
        $output .= '<span class="menu-text">' . esc_html($item->title) . '</span>';

        // BADGE
        if ($badge) {
            $output .= '<span class="menu-badge">' . esc_html($badge) . '</span>';
        }

        $output .= '</a>';
    }

    public function end_el(&$output, $item, $depth = 0, $args = []) {
        $output .= '</li>';
    }
}

🧩 5. Implementar el menú en el tema

En tu template (por ejemplo header.php):

wp_nav_menu([
    'theme_location' => 'primary_menu',
    'menu_class' => 'menu-principal',
    'walker' => new App_Walker_Nav_Menu()
]);

🧩 6. CSS recomendado

Cada tema puede personalizarlo, pero al menos:

.menu-icon {
    margin-right: 6px;
    display: inline-block;
}

.menu-badge {
    background: #ff4747;
    color: #fff;
    padding: 2px 6px;
    font-size: 12px;
    border-radius: 4px;
    margin-left: 6px;
}

🧩 7. (Opcional) Extender tipografía

Si quieres agregar tipografía por menú o por ítem:

Campos adicionales:

font-size

font-weight

font-family

padding custom

Y en el walker agregas inline styles o clases dinámicas.

🧩 8. (Opcional) Mega Menú

Se agrega otro checkbox:

¿Activar Mega Menú?


Guardado como:

_menu_megamenu = true


Y en el Walker, si es un item padre con ese meta:

output mega-menu markup

🎁 LISTA DE ARCHIVOS que se DEBE CREAR

Muy importante para que no se pierda:

/inc/menu/
    custom-fields.php           (campos extra en admin)
    save-fields.php             (guardar meta)
    class-app-walker.php        (walker custom)

functions.php
    include_once '/inc/menu/custom-fields.php';
    include_once '/inc/menu/save-fields.php';
    include_once '/inc/menu/class-app-walker.php';
    register_nav_menus();

💯 Con esto tu tema tiene:

✔ Menú multinivel
✔ Drag & drop nativo
✔ Iconos por item
✔ Badges
✔ Colores personalizados
✔ Listo para que tu app los genere automáticamente
 