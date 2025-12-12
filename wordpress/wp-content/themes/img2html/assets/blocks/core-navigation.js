(function(){
  try{
    document.addEventListener('keydown', function(e){
      if (e.key === 'Escape'){
        var dialog = document.querySelector('.wp-block-navigation__responsive-container.is-menu-open');
        if (dialog){
          var btn = dialog.querySelector('button');
          if (btn){ btn.click(); }
        }
      }
    });
  }catch(err){}
})();