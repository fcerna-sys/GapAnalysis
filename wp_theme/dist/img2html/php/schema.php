<?php
function img2html_schema_head(){
  if (is_singular('post')){
    $data = [
      "@context"=>"https://schema.org",
      "@type"=>"BlogPosting",
      "headline"=>get_the_title(),
      "datePublished"=>get_the_date('c'),
      "author"=>["@type"=>"Person","name"=>get_the_author()],
      "image"=>get_the_post_thumbnail_url(get_the_ID(),'full')
    ];
    echo '<script type="application/ld+json">'.wp_json_encode($data).'</script>';
  } else {
    $data = [
      "@context"=>"https://schema.org",
      "@type"=>"Organization",
      "name"=>get_bloginfo('name')
    ];
    echo '<script type="application/ld+json">'.wp_json_encode($data).'</script>';
  }
}
add_action('wp_head','img2html_schema_head');