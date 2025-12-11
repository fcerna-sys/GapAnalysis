#!/usr/bin/env python3
"""Verificar que el código migrado está completo"""
import os

files_to_check = {
    'renders.py': ['_generate_slider_render_php', '_render_hero', '_render_section', '_render_cards'],
    'editors.py': ['_generate_slider_editor_js', '_editor_sidebar', '_editor_search'],
    'styles.py': ['_generate_slider_style_css', '_generate_slider_editor_css'],
    'organisms.py': ['create_slider_block', 'create_hero_block', 'create_section_block'],
}

print("=" * 70)
print("VERIFICACION DE MIGRACION COMPLETA")
print("=" * 70)

for filename, functions in files_to_check.items():
    filepath = f'blocks_builder/{filename}'
    if not os.path.exists(filepath):
        print(f"\n[ERROR] {filename} no existe")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.splitlines()
    
    print(f"\n{filename}:")
    print(f"  Total lineas: {len(lines)}")
    print(f"  Total caracteres: {len(content)}")
    
    all_found = True
    for func_name in functions:
        found = f'def {func_name}' in content
        status = "[OK]" if found else "[FALTA]"
        print(f"  {status} {func_name}")
        if not found:
            all_found = False
    
    if all_found:
        print(f"  [OK] Todas las funciones encontradas")
    else:
        print(f"  [ERROR] Faltan funciones")

print("\n" + "=" * 70)
print("VERIFICACION COMPLETA")
print("=" * 70)

