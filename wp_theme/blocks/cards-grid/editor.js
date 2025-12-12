(function(wp){
  const { InnerBlocks } = wp.blockEditor || wp.editor;
  const el = wp.element.createElement;
  const ALLOWED = ['img2html/card'];
  const TEMPLATE = [
    ['img2html/card'],
    ['img2html/card'],
    ['img2html/card']
  ];
  wp.hooks.addFilter(
    'blocks.registerBlockType',
    'img2html/cards-grid-edit',
    function(settings, name){
      if (name !== 'img2html/cards-grid') return settings;
      return {
        ...settings,
        edit: function(){
          return el(InnerBlocks, { allowedBlocks: ALLOWED, template: TEMPLATE, templateLock: false });
        }
      };
    }
  );
})(window);
