(function(){
  try{
    document.addEventListener('keydown', function(e){
      if (e.key === 'Escape'){
        var overlay = document.querySelector('.wp-lightbox-overlay');
        if (overlay){ overlay.click(); }
      }
    });
  }catch(err){ /* no-op */ }
})();