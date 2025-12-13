(function(wp){
  const { InspectorControls } = wp.blockEditor || wp.editor;
  const { PanelBody, SelectControl, TextControl, ToggleControl } = wp.components;
  const el = wp.element.createElement;
  const NAME = 'img2html/doc-viewer';
  const DOCS = Array.isArray(window.IMG2HTML_DOCS) ? window.IMG2HTML_DOCS : [
    { label: 'THEME_GUIDE.md', value: 'THEME_GUIDE.md' },
    { label: 'PATTERNS_GUIDE.md', value: 'PATTERNS_GUIDE.md' },
    { label: 'EXTEND.md', value: 'EXTEND.md' },
    { label: 'COMPOSE.md', value: 'COMPOSE.md' },
    { label: 'STYLE.md', value: 'STYLE.md' },
    { label: 'app-overview.html', value: 'app-overview.html' }
  ];
  wp.hooks.addFilter('blocks.registerBlockType','img2html/doc-viewer-edit',function(settings, blockName){
    if (blockName !== NAME) return settings;
    const Edit = function(props){
      const a = props.attributes || {};
      const setAttr = (k) => (v) => props.setAttributes({ [k]: v });
      return el(wp.element.Fragment, {},
        el(InspectorControls, {},
          el(PanelBody, { title: 'Doc Viewer' },
            el(SelectControl, { label: 'Archivo', value: a.file || 'THEME_GUIDE.md', options: DOCS, onChange: setAttr('file') }),
            el(TextControl, { label: 'Sección (opcional)', value: a.section || '', onChange: setAttr('section') }),
            el(ToggleControl, { label: 'Mostrar título', checked: !!a.showTitle, onChange: setAttr('showTitle') }),
            el(ToggleControl, { label: 'Habilitar búsqueda', checked: a.searchEnabled !== false, onChange: setAttr('searchEnabled') })
          )
        ),
        el('div', {}, 'Se renderiza en el front‑end')
      );
    };
    return { ...settings, edit: Edit };
  });
})(window);
