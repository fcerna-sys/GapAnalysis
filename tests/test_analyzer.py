import pytest
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from analyzer import identify_pattern_variant, identify_pattern, extract_design_dna, _is_grayscale

def test_identify_pattern_variant_balanced():
    section = {
        'layout_rows': [
            {
                'columns': ['c1.png', 'c2.png'],
                'ratios_percent': [50, 52]
            }
        ]
    }
    assert identify_pattern_variant(section) == 'balanced'
    assert identify_pattern(section) == 'hero-split-screen-balanced'

def test_identify_pattern_variant_asymmetric():
    section = {
        'layout_rows': [
            {
                'columns': ['c1.png', 'c2.png'],
                'ratios_percent': [70, 30]
            }
        ]
    }
    assert identify_pattern_variant(section) == 'asymmetric'
    assert identify_pattern(section) == 'hero-split-screen-asymmetric'

def test_is_grayscale():
    assert _is_grayscale((100, 105, 100), tolerance=10)
    assert not _is_grayscale((120, 150, 120), tolerance=10)

def test_extract_design_dna_default():
    dna = extract_design_dna([])
    assert isinstance(dna, dict)
    pal = dna.get('palette') or []
    slugs = [p.get('slug') for p in pal]
    assert 'background' in slugs and 'text' in slugs and 'primary' in slugs