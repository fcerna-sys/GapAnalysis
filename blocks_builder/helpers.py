"""
Funciones auxiliares para bloques de Gutenberg.
Incluye: prefijo BEM, configuración de frameworks CSS, generación de CSS con BEM.
"""
import os
import json
import re
from typing import Dict, List, Optional, Tuple


def get_bem_prefix(theme_slug: Optional[str] = None) -> str:
    """
    Obtiene el prefijo BEM desde theme_slug.
    Convierte a formato válido (solo letras, números, guiones) y usa como prefijo.
    Si no hay theme_slug, usa 'img2html' como fallback.
    """
    if not theme_slug:
        return 'img2html'
    # Limpiar slug: solo letras, números, guiones; convertir a minúsculas
    clean = re.sub(r'[^a-z0-9-]', '', theme_slug.lower())
    # Si queda vacío o muy corto, usar fallback
    if not clean or len(clean) < 2:
        return 'img2html'
    return clean


def setup_css_framework(theme_dir: str, framework: str):
    """
    Configura el framework CSS seleccionado (Tailwind, Bootstrap o ninguno).
    """
    if framework == 'tailwind':
        _setup_tailwind(theme_dir)
    elif framework == 'bootstrap':
        _setup_bootstrap(theme_dir)
    else:
        # CSS propio - no hacer nada especial
        pass


def _setup_tailwind(theme_dir: str):
    """Configura Tailwind CSS con compilación automática."""
    try:
        # Crear tailwind.config.js
        tailwind_config = """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './**/*.php',
    './blocks/**/*.js',
    './templates/**/*.html',
    './parts/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        // Colores del tema se agregarán automáticamente
      },
    },
  },
  plugins: [],
  corePlugins: {
    preflight: false, // Evitar conflictos con WordPress
  },
}
"""
        config_path = os.path.join(theme_dir, 'tailwind.config.js')
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(tailwind_config)
        
        # Crear package.json para compilar Tailwind
        package_json = {
            "name": "img2html-theme",
            "version": "1.0.0",
            "scripts": {
                "build:css": "tailwindcss -i ./src/input.css -o ./assets/css/tailwind.css --minify",
                "watch:css": "tailwindcss -i ./src/input.css -o ./assets/css/tailwind.css --watch"
            },
            "devDependencies": {
                "tailwindcss": "^3.4.0"
            }
        }
        package_path = os.path.join(theme_dir, 'package.json')
        with open(package_path, 'w', encoding='utf-8') as f:
            json.dump(package_json, f, indent=2)
        
        # Crear directorio src y archivo input.css
        src_dir = os.path.join(theme_dir, 'src')
        os.makedirs(src_dir, exist_ok=True)
        input_css = """@tailwind base;
@tailwind components;
@tailwind utilities;

/* Estilos personalizados del tema */
"""
        input_css_path = os.path.join(src_dir, 'input.css')
        with open(input_css_path, 'w', encoding='utf-8') as f:
            f.write(input_css)
        
        # Crear assets/css si no existe
        assets_css_dir = os.path.join(theme_dir, 'assets', 'css')
        os.makedirs(assets_css_dir, exist_ok=True)
        
        # Crear tailwind.css compilado básico (se recompilará después)
        tailwind_css = """/* Tailwind CSS compilado */
/* Este archivo se regenera con: npm run build:css */
"""
        tailwind_css_path = os.path.join(assets_css_dir, 'tailwind.css')
        with open(tailwind_css_path, 'w', encoding='utf-8') as f:
            f.write(tailwind_css)
        
        print("Tailwind CSS configurado. Ejecuta 'npm install && npm run build:css' para compilar.")
        
    except Exception as e:
        print(f"Error al configurar Tailwind: {e}")


def _setup_bootstrap(theme_dir: str):
    """Configura Bootstrap 5 con archivos locales."""
    try:
        # Crear directorio assets
        assets_dir = os.path.join(theme_dir, 'assets')
        os.makedirs(assets_dir, exist_ok=True)
        css_dir = os.path.join(assets_dir, 'css')
        js_dir = os.path.join(assets_dir, 'js')
        os.makedirs(css_dir, exist_ok=True)
        os.makedirs(js_dir, exist_ok=True)
        
        # Crear bootstrap.custom.css
        bootstrap_custom = """/* Bootstrap 5 Custom Styles */
/* Solo incluye lo necesario para evitar conflictos con Gutenberg */

/* Importar Bootstrap desde node_modules o CDN local */
@import url('bootstrap.min.css');

/* Scope local para evitar conflictos */
.img2html-theme {
  /* Estilos del tema aquí */
}

/* Evitar conflictos con editor */
.block-editor-page .img2html-theme {
  /* Estilos específicos del editor */
}
"""
        bootstrap_custom_path = os.path.join(css_dir, 'bootstrap.custom.css')
        with open(bootstrap_custom_path, 'w', encoding='utf-8') as f:
            f.write(bootstrap_custom)
        
        # Crear README para Bootstrap
        bootstrap_readme = """# Bootstrap 5 Setup

Para usar Bootstrap 5 en este tema:

1. Descarga Bootstrap desde https://getbootstrap.com/
2. Copia bootstrap.min.css a assets/css/
3. Copia bootstrap.bundle.min.js a assets/js/
4. O usa npm: npm install bootstrap@5

El tema usará bootstrap.custom.css para estilos personalizados.
"""
        readme_path = os.path.join(assets_dir, 'BOOTSTRAP_README.md')
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(bootstrap_readme)
        
        print("Bootstrap 5 configurado. Descarga los archivos desde getbootstrap.com")
        
    except Exception as e:
        print(f"Error al configurar Bootstrap: {e}")


def generate_bem_css(
    block_name: str,
    bem_prefix: str,
    css_framework: str,
    elements: List[Tuple[str, str]],
    modifiers: Optional[Dict[str, List[str]]] = None,
    base_styles: Optional[str] = None
) -> str:
    """
    Genera CSS siguiendo metodología BEM (Block__Element--Modifier).
    
    Args:
        block_name: Nombre del bloque (ej: 'atom-button')
        bem_prefix: Prefijo BEM (ej: 'img2html')
        css_framework: 'tailwind', 'bootstrap' o 'none'
        elements: Lista de tuplas (nombre_elemento, estilos_css)
        modifiers: Dict con modificadores {elemento: [mod1, mod2, ...]}
        base_styles: Estilos CSS base para el bloque
    
    Returns:
        CSS completo con metodología BEM
    """
    # Asegurar que el prefijo se use correctamente en clases CSS
    base_class = f".{bem_prefix}-{block_name}"
    
    css_lines = []
    css_lines.append(f"/* {block_name.upper()} - Estilos con BEM */")
    css_lines.append(f"/* Bloque: {base_class} */")
    css_lines.append("")
    
    # Estilos base del bloque
    if base_styles:
        css_lines.append(f"{base_class} {{")
        css_lines.append(base_styles)
        css_lines.append("}")
        css_lines.append("")
    
    # Elementos (Block__Element)
    for element_name, element_styles in elements:
        element_class = f"{base_class}__{element_name}"
        css_lines.append(f"/* Elemento: {element_class} */")
        css_lines.append(f"{element_class} {{")
        css_lines.append(element_styles)
        css_lines.append("}")
        css_lines.append("")
    
    # Modificadores (Block--Modifier o Block__Element--Modifier)
    if modifiers:
        for element_or_block, mod_list in modifiers.items():
            if element_or_block == block_name or element_or_block in ['button', 'heading', 'badge', 'pricing-item']:
                # Modificador del bloque
                for mod in mod_list:
                    mod_class = f"{base_class}--{mod}"
                    css_lines.append(f"/* Modificador: {mod_class} */")
                    css_lines.append(f"{mod_class} {{")
                    css_lines.append("    /* Estilos del modificador */")
                    css_lines.append("}")
                    css_lines.append("")
            else:
                # Modificador de un elemento
                element_class = f"{base_class}__{element_or_block}"
                for mod in mod_list:
                    mod_class = f"{element_class}--{mod}"
                    css_lines.append(f"/* Modificador: {mod_class} */")
                    css_lines.append(f"{mod_class} {{")
                    css_lines.append("    /* Estilos del modificador */")
                    css_lines.append("}")
                    css_lines.append("")
    
    # Framework-specific styles
    if css_framework == 'tailwind':
        css_lines.append("/* Tailwind: Usar clases de utilidad cuando sea posible */")
    elif css_framework == 'bootstrap':
        css_lines.append("/* Bootstrap: Usar clases de Bootstrap cuando sea posible */")
    
    return "\n".join(css_lines)

