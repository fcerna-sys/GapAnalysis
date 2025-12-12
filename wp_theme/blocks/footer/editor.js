(function(wp){
  const { InnerBlocks } = wp.blockEditor || wp.editor;
  const el = wp.element.createElement;
  const ALLOWED = ['core/columns','core/site-logo','core/heading','core/paragraph','core/navigation','core/buttons','core/column','img2html/social-links'];
  const TEMPLATE = [
    ['core/columns']
  ];
  wp.hooks.addFilter(
    'blocks.registerBlockType',
    'img2html/footer-edit',
    function(settings, name){
      if (name !== 'img2html/footer') return settings;
      return {
        ...settings,
        edit: function(){
          return el(InnerBlocks, { allowedBlocks: ALLOWED, template: TEMPLATE, templateLock: false });
        }
      };
    }
  );
})(window);
