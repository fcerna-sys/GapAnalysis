(function(){
  try{
    document.addEventListener('keydown', function(e){
      if (e.key === 'Escape'){
        var input = document.querySelector('.wp-block-search input[type="search"]');
        if (input){ input.blur(); }
      }
    });
  }catch(err){}
})();