(function(wp){
  const { InspectorControls } = wp.blockEditor || wp.editor;
  const { PanelBody, SelectControl, TextControl, RangeControl, Notice, ToggleControl } = wp.components;
  const el = wp.element.createElement;
  const name = 'img2html/classic-menu';
  const LOCATIONS = (window.IMG2HTML_MENU_LOCATIONS && Array.isArray(window.IMG2HTML_MENU_LOCATIONS))
    ? window.IMG2HTML_MENU_LOCATIONS
    : [
      { label: 'Menú Principal', value: 'primary_menu' },
      { label: 'Menú Secundario', value: 'secondary_menu' },
      { label: 'Menú Footer', value: 'footer_menu' }
    ];
  wp.hooks.addFilter('blocks.registerBlockType','img2html/classic-menu-edit',function(settings, blockName){
    if (blockName !== name) return settings;
    const Edit = function(props){
      const attrs = props.attributes || {};
      const setAttr = (k) => (v) => props.setAttributes({ [k]: v });
      const loc = attrs.location || 'primary_menu';
      const assignedMap = window.IMG2HTML_MENU_ASSIGNED || {};
      const menusList = Array.isArray(window.IMG2HTML_MENUS) ? window.IMG2HTML_MENUS : [];
      const assignedName = assignedMap[loc] || 'Sin asignar';
      const adminUrl = 'nav-menus.php';
      return el(wp.element.Fragment, {},
        el(InspectorControls, {},
          el(PanelBody, { title: 'Menú' },
            el(SelectControl, { label: 'Ubicación', value: loc, options: LOCATIONS, onChange: setAttr('location') }),
            el(TextControl, { label: 'Clase', value: attrs.menuClass || '', onChange: setAttr('menuClass') }),
            el(RangeControl, { label: 'Profundidad', value: attrs.depth || 3, min: 1, max: 6, onChange: setAttr('depth') }),
            el(SelectControl, { label: 'Menú específico (opcional)', value: attrs.menuId || 0, options: [{label:'— ninguno —', value:0}, ...menusList], onChange: setAttr('menuId') }),
            el(SelectControl, { label: 'Estilo', value: attrs.menuStyle || 'default', options: [
              { label: 'Predeterminado', value: 'default' },
              { label: 'Underline', value: 'underline' },
              { label: 'Pill', value: 'pill' },
              { label: 'Ghost', value: 'ghost' },
              { label: 'Compact + Pill', value: 'compact-pill' },
              { label: 'Compact + Ghost', value: 'compact-ghost' },
              { label: 'Compact + Underline', value: 'compact-underline' }
            ], onChange: setAttr('menuStyle') }),
            el(ToggleControl, { label: 'Compacto', checked: !!attrs.compact, onChange: setAttr('compact') }),
            el(Notice, { status: 'warning', isDismissible: false },
              el('span', {}, 'Ubicación: ' + (LOCATIONS.find(o=>o.value===loc)?.label || loc) + ' — '),
              el('strong', {}, 'Asignado: ' + assignedName + ' '),
              el('a', { href: adminUrl, target: '_blank', rel: 'noopener' }, 'Abrir Menús')
            )
          )
        ),
        el('div', {}, 'El menú se renderiza en el front‑end')
      );
    };
    return { ...settings, edit: Edit };
  });
})(window);
