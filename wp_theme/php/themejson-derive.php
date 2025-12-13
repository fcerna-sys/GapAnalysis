<?php
if (!defined('ABSPATH')) { exit; }

function img2html_parse_px($s){ if (preg_match('/([0-9\.]+)/',$s,$m)) return floatval($m[1]); return 720; }
function img2html_type_ratio($px){ if ($px<=640) return 1.25; if ($px<=860) return 1.333; return 1.414; }
function img2html_baseline_step($px){ if ($px<=640) return 6; if ($px<=860) return 8; return 10; }
function img2html_modular_size($base, $ratio, $steps){ return $base * pow($ratio, $steps); }

add_filter('wp_theme_json_data_theme', function($data){
  $path = get_theme_file_path('theme.json');
  $json = file_exists($path) ? json_decode(file_get_contents($path), true) : [];
  $contentSize = isset($json['settings']['layout']['contentSize']) ? $json['settings']['layout']['contentSize'] : '720px';
  $px = img2html_parse_px($contentSize);
  $ratio = img2html_type_ratio($px);
  $profile = get_option('img2html_theme_profile','medium');
  if ($profile === 'compact') $ratio = max(1.2, $ratio - 0.05);
  if ($profile === 'ample') $ratio = min(1.6, $ratio + 0.05);
  $baseRem = 1.0;
  $sizes = [
    'h1' => img2html_modular_size($baseRem, $ratio, 4),
    'h2' => img2html_modular_size($baseRem, $ratio, 3),
    'h3' => img2html_modular_size($baseRem, $ratio, 2),
    'h4' => img2html_modular_size($baseRem, $ratio, 1),
    'h5' => img2html_modular_size($baseRem, $ratio, 0),
    'h6' => 0.75
  ];
  $leadMax = img2html_modular_size($baseRem, $ratio, 1.5);
  $titleMax = img2html_modular_size($baseRem, $ratio, 3);
  $displayMax = img2html_modular_size($baseRem, $ratio, 4);
  $spacing = img2html_baseline_step($px);
  if ($profile === 'compact') $spacing = max(4, $spacing - 2);
  if ($profile === 'ample') $spacing = min(14, $spacing + 2);
  $sp = [
    ['slug'=>'0','name'=>'None','size'=>'0'],
    ['slug'=>'xxs','name'=>'XX Small','size'=>round($spacing*0.5,2).'px'],
    ['slug'=>'xs','name'=>'Extra Small','size'=>round($spacing*0.75,2).'px'],
    ['slug'=>'sm','name'=>'Small','size'=>round($spacing*1.0,2).'px'],
    ['slug'=>'md','name'=>'Medium','size'=>round($spacing*2.0,2).'px'],
    ['slug'=>'lg','name'=>'Large','size'=>round($spacing*3.0,2).'px'],
    ['slug'=>'xl','name'=>'Extra Large','size'=>round($spacing*4.0,2).'px'],
    ['slug'=>'2xl','name'=>'2X Large','size'=>round($spacing*6.0,2).'px']
  ];
  $new = [
    'settings' => [
      'typography' => [
        'fontSizes' => [
          [ 'slug'=>'display','name'=>'Display','size'=> 'clamp('.round($displayMax*0.6,3).'rem, 6vw, '.round($displayMax,3).'rem)' ],
          [ 'slug'=>'title','name'=>'Title','size'=> 'clamp('.round($titleMax*0.66,3).'rem, 4vw, '.round($titleMax,3).'rem)' ],
          [ 'slug'=>'lead','name'=>'Lead','size'=> 'clamp('.round($leadMax*0.75,3).'rem, 2.5vw, '.round($leadMax,3).'rem)' ],
          [ 'slug'=>'body','name'=>'Body','size'=> '1rem' ],
          [ 'slug'=>'caption','name'=>'Caption','size'=> '0.875rem' ],
          [ 'slug'=>'overline','name'=>'Overline','size'=> '0.75rem' ]
        ]
      ],
      'spacing' => [
        'spacingScale' => [ 'steps' => 0 ],
        'spacingSizes' => $sp
      ]
    ],
    'styles' => [
      'spacing' => [ 'blockGap' => round($spacing*2.0).'px' ],
      'elements' => (function() use ($sizes, $profile){
        $lh_delta = $profile === 'compact' ? -0.05 : ($profile === 'ample' ? 0.05 : 0);
        $lh = function($base) use ($lh_delta){ $val = $base + $lh_delta; return (string)round($val,2); };
        return [
          'h1' => [ 'typography' => [ 'fontSize' => round($sizes['h1'],3).'rem', 'lineHeight' => $lh(1.2) ] ],
          'h2' => [ 'typography' => [ 'fontSize' => round($sizes['h2'],3).'rem', 'lineHeight' => $lh(1.25) ] ],
          'h3' => [ 'typography' => [ 'fontSize' => round($sizes['h3'],3).'rem', 'lineHeight' => $lh(1.3) ] ],
          'h4' => [ 'typography' => [ 'fontSize' => round($sizes['h4'],3).'rem', 'lineHeight' => $lh(1.35) ] ],
          'h5' => [ 'typography' => [ 'fontSize' => round($sizes['h5'],3).'rem', 'lineHeight' => $lh(1.4) ] ],
          'h6' => [ 'typography' => [ 'fontSize' => 'var(--wp--preset--font-size--overline)', 'textTransform'=>'uppercase', 'letterSpacing'=>'.08em' ] ]
        ];
      })(),
      'blocks' => [
        'core/paragraph' => [ 'typography' => [ 'lineHeight' => '1.6' ], 'spacing' => [ 'margin' => [ 'bottom' => 'var(--wp--preset--spacing--md)' ] ] ],
        'core/heading' => [ 'spacing' => [ 'margin' => [ 'bottom' => 'var(--wp--preset--spacing--md)' ] ] ],
        'core/list' => [ 'spacing' => [ 'margin' => [ 'bottom' => 'var(--wp--preset--spacing--md)' ] ] ],
        'core/image' => [ 'border' => [ 'radius' => '8px' ], 'spacing' => [ 'margin' => [ 'bottom' => 'var(--wp--preset--spacing--md)' ] ] ]
      ]
    ]
  ];
  if (method_exists($data,'update_with')){ $data->update_with($new); }
  return $data;
});
