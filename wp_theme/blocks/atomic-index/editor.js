(function(wp){
  const { InspectorControls } = wp.blockEditor || wp.editor;
  const { PanelBody, ToggleControl, TextControl, RangeControl } = wp.components;
  const el = wp.element.createElement;
  const name = 'img2html/atomic-index';
  wp.hooks.addFilter('blocks.registerBlockType','img2html/atomic-index-edit',function(settings, blockName){
    if (blockName !== name) return settings;
    const Edit = function(props){
      const attrs = props.attributes || {};
      const setAttr = (k) => (v) => props.setAttributes({ [k]: v });
      return el(wp.element.Fragment, {},
        el(InspectorControls, {},
          el(PanelBody, { title: 'Atomic Index' },
            el(ToggleControl, { label: 'Mostrar Átomos', checked: !!attrs.showAtoms, onChange: setAttr('showAtoms') }),
            el(ToggleControl, { label: 'Mostrar Moléculas', checked: !!attrs.showMolecules, onChange: setAttr('showMolecules') }),
            el(ToggleControl, { label: 'Mostrar Organismos', checked: !!attrs.showOrganisms, onChange: setAttr('showOrganisms') }),
            el(TextControl, { label: 'Buscar por nombre', value: attrs.query || '', onChange: setAttr('query'), placeholder: 'ej: card, hero' }),
            el(RangeControl, { label: 'Límite por grupo (0 = sin límite)', value: attrs.limitPerGroup || 0, min: 0, max: 12, onChange: setAttr('limitPerGroup') }),
            el(ToggleControl, { label: 'Solo bloques completos (render + style)', checked: !!attrs.onlyComplete, onChange: setAttr('onlyComplete') }),
            el(wp.components.SelectControl, { label: 'Orden', value: attrs.order || 'alpha', onChange: setAttr('order'), options: [
              { label: 'Alfabético', value: 'alpha' },
              { label: 'Fecha de modificación', value: 'mtime' }
            ] })
          ),
          el(PanelBody, { title: 'Plantilla de tarjeta' },
            el(wp.components.SelectControl, { label: 'Plantilla', value: attrs.cardTemplate || 'compact', onChange: setAttr('cardTemplate'), options: [
              { label: 'Compacta', value: 'compact' },
              { label: 'Detallada', value: 'detailed' },
              { label: 'Minimal', value: 'minimal' }
            ] }),
            el(ToggleControl, { label: 'Mostrar título del bloque', checked: attrs.showTitle !== false, onChange: setAttr('showTitle') })
            ,
            el(wp.components.SelectControl, { label: 'Fuente de título', value: attrs.titleSource || 'title', onChange: setAttr('titleSource'), options: [
              { label: 'Título (legible)', value: 'title' },
              { label: 'Slug técnico', value: 'slug' },
              { label: 'Nombre de bloque (name)', value: 'name' }
            ] }),
            el(ToggleControl, { label: 'Mostrar subtítulo técnico (slug)', checked: !!attrs.showSubtitleTechnical, onChange: setAttr('showSubtitleTechnical') })
          )
        ),
        el('div', {}, 'Atomic Index: ver previsualización en el front‑end')
      );
    };
    return { ...settings, edit: Edit };
  });
})(window);
