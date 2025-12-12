(function(){
  try{
    var iframes = document.querySelectorAll('.wp-block-embed iframe');
    iframes.forEach(function(f){
      f.setAttribute('loading','lazy');
    });
  }catch(err){}
})();