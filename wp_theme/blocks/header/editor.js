(function(wp){
  const { InnerBlocks, InspectorControls } = wp.blockEditor || wp.editor;
  const { PanelBody, SelectControl, ToggleControl } = wp.components;
  const el = wp.element.createElement;
  const ALLOWED = ['core/site-logo','core/navigation','core/buttons','img2html/classic-menu'];
  const TEMPLATE = [
    ['core/site-logo', { width: 48 }],
    ['core/navigation', { }],
    ['core/buttons', { }]
  ];
  wp.hooks.addFilter(
    'blocks.registerBlockType',
    'img2html/header-edit',
    function(settings, name){
      if (name !== 'img2html/header') return settings;
      return {
        ...settings,
        edit: function(props){
          const attrs = props.attributes || {};
          const setAttr = (k) => (v) => props.setAttributes({ [k]: v });
          return el(wp.element.Fragment, {},
            el(InspectorControls, {},
              el(PanelBody, { title: 'Header' },
                el(SelectControl, { label: 'Alineación', value: attrs.alignment || 'space-between', options: [
                  { label: 'Space Between', value: 'space-between' },
                  { label: 'Izquierda', value: 'left' },
                  { label: 'Derecha', value: 'right' }
                ], onChange: setAttr('alignment') }),
                el(ToggleControl, { label: 'Sticky', checked: !!attrs.sticky, onChange: setAttr('sticky') }),
                el(ToggleControl, { label: 'Transparente', checked: !!attrs.transparent, onChange: setAttr('transparent') }),
                el(ToggleControl, { label: 'Fondo oscuro', checked: !!attrs.darkBackground, onChange: setAttr('darkBackground') }),
                el(ToggleControl, { label: 'Sombra', checked: attrs.shadow !== false, onChange: setAttr('shadow') })
              )
            ),
            el(InnerBlocks, { allowedBlocks: ALLOWED, template: TEMPLATE, templateLock: false })
          );
        }
      };
    }
  );
})(window);
