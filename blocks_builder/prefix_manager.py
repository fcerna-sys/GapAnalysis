"""
Sistema centralizado de gestión de prefijos dinámicos.
Asegura que el prefijo del tema se aplique consistentemente en:
- block.json (name, category, textdomain)
- Clases CSS BEM
- Nombres de patrones
- Funciones PHP
- Slug del theme
- Text-domain
- Folder structure
"""
import os
import re
from typing import Optional, Dict


class PrefixManager:
    """Gestiona prefijos dinámicos del tema de forma centralizada."""
    
    def __init__(self, theme_slug: Optional[str] = None, theme_textdomain: Optional[str] = None):
        """
        Inicializa el gestor de prefijos.
        
        Args:
            theme_slug: Slug del tema (ej: 'mi-tema')
            theme_textdomain: Text domain del tema (opcional, se genera desde slug si no se proporciona)
        """
        self.theme_slug = self._clean_slug(theme_slug) if theme_slug else 'img2html'
        self.bem_prefix = self._clean_slug(theme_slug) if theme_slug else 'img2html'
        self.textdomain = theme_textdomain or self.bem_prefix
        self.folder_name = self.theme_slug
    
    def _clean_slug(self, slug: str) -> str:
        """Limpia y normaliza un slug."""
        if not slug:
            return 'img2html'
        # Solo letras, números y guiones; minúsculas
        clean = re.sub(r'[^a-z0-9-]', '', slug.lower())
        # Remover guiones múltiples
        clean = re.sub(r'-+', '-', clean)
        # Remover guiones al inicio/final
        clean = clean.strip('-')
        if not clean or len(clean) < 2:
            return 'img2html'
        return clean
    
    # ========================================
    # PREFIJOS PARA BLOCK.JSON
    # ========================================
    
    def get_block_name(self, block_type: str, block_name: str) -> str:
        """Obtiene el nombre completo del bloque para block.json."""
        return f"{self.bem_prefix}/{block_type}-{block_name}"
    
    def get_block_category(self, category_type: str = 'blocks') -> str:
        """Obtiene la categoría del bloque."""
        # category_type puede ser: 'atoms', 'molecules', 'organisms', 'blocks'
        return f"{self.bem_prefix}-{category_type}"
    
    def get_block_textdomain(self) -> str:
        """Obtiene el textdomain para block.json."""
        return self.textdomain
    
    # ========================================
    # PREFIJOS PARA CLASES CSS BEM
    # ========================================
    
    def get_bem_class(self, block_type: str, block_name: str, element: Optional[str] = None, 
                     modifier: Optional[str] = None) -> str:
        """
        Genera una clase CSS BEM completa.
        
        Ejemplos:
            get_bem_class('atom', 'button') -> 'mitema-atom-button'
            get_bem_class('atom', 'button', 'text') -> 'mitema-atom-button__text'
            get_bem_class('atom', 'button', 'text', 'large') -> 'mitema-atom-button__text--large'
        """
        base = f"{self.bem_prefix}-{block_type}-{block_name}"
        if element:
            base = f"{base}__{element}"
        if modifier:
            base = f"{base}--{modifier}"
        return base
    
    def get_bem_base_class(self, block_type: str, block_name: str) -> str:
        """Obtiene solo la clase base BEM."""
        return f"{self.bem_prefix}-{block_type}-{block_name}"
    
    # ========================================
    # PREFIJOS PARA PATRONES
    # ========================================
    
    def get_pattern_slug(self, pattern_name: str) -> str:
        """Obtiene el slug completo del pattern."""
        return f"{self.bem_prefix}/{pattern_name}"
    
    def get_pattern_category(self, category: str) -> str:
        """Obtiene la categoría del pattern con prefijo."""
        return f"{self.bem_prefix}-{category}"
    
    # ========================================
    # PREFIJOS PARA FUNCIONES PHP
    # ========================================
    
    def get_php_function_name(self, function_name: str) -> str:
        """
        Obtiene el nombre de una función PHP con prefijo.
        
        Ejemplo:
            get_php_function_name('register_blocks') -> 'mitema_register_blocks'
        """
        # Convertir guiones a guiones bajos y asegurar prefijo
        clean_name = function_name.replace('-', '_')
        if not clean_name.startswith(self.bem_prefix.replace('-', '_')):
            return f"{self.bem_prefix.replace('-', '_')}_{clean_name}"
        return clean_name
    
    def get_php_hook_name(self, hook_name: str) -> str:
        """Obtiene el nombre de un hook de WordPress con prefijo."""
        return f"{self.bem_prefix.replace('-', '_')}_{hook_name}"
    
    # ========================================
    # PREFIJOS PARA VARIABLES Y CONSTANTES
    # ========================================
    
    def get_php_constant_name(self, constant_name: str) -> str:
        """Obtiene el nombre de una constante PHP con prefijo en mayúsculas."""
        prefix_upper = self.bem_prefix.replace('-', '_').upper()
        const_upper = constant_name.upper()
        return f"{prefix_upper}_{const_upper}"
    
    def get_js_variable_name(self, var_name: str) -> str:
        """Obtiene el nombre de una variable JavaScript con prefijo (camelCase)."""
        # Convertir prefijo a camelCase
        parts = self.bem_prefix.split('-')
        prefix_camel = parts[0] + ''.join(word.capitalize() for word in parts[1:])
        # Convertir var_name a camelCase si tiene guiones
        var_parts = var_name.split('-')
        var_camel = var_parts[0] + ''.join(word.capitalize() for word in var_parts[1:])
        return f"{prefix_camel}{var_camel.capitalize()}"
    
    # ========================================
    # ESTRUCTURA DE CARPETAS
    # ========================================
    
    def get_theme_folder_name(self) -> str:
        """Obtiene el nombre de la carpeta del tema."""
        return self.folder_name
    
    def get_blocks_folder_path(self, theme_dir: str) -> str:
        """Obtiene la ruta completa de la carpeta de bloques."""
        return os.path.join(theme_dir, 'blocks')
    
    def get_patterns_folder_path(self, theme_dir: str) -> str:
        """Obtiene la ruta completa de la carpeta de patterns."""
        return os.path.join(theme_dir, 'patterns')
    
    # ========================================
    # MÉTODOS DE VALIDACIÓN
    # ========================================
    
    def validate_prefix(self) -> Dict[str, bool]:
        """Valida que todos los prefijos sean consistentes."""
        return {
            'theme_slug': bool(self.theme_slug and len(self.theme_slug) >= 2),
            'bem_prefix': bool(self.bem_prefix and len(self.bem_prefix) >= 2),
            'textdomain': bool(self.textdomain and len(self.textdomain) >= 2),
            'folder_name': bool(self.folder_name and len(self.folder_name) >= 2),
            'consistent': self.bem_prefix == self._clean_slug(self.theme_slug)
        }
    
    def get_all_prefixes(self) -> Dict[str, str]:
        """Obtiene todos los prefijos en un diccionario."""
        return {
            'theme_slug': self.theme_slug,
            'bem_prefix': self.bem_prefix,
            'textdomain': self.textdomain,
            'folder_name': self.folder_name,
            'php_prefix': self.bem_prefix.replace('-', '_'),
            'js_prefix': self._to_camel_case(self.bem_prefix)
        }
    
    def _to_camel_case(self, text: str) -> str:
        """Convierte un texto a camelCase."""
        parts = text.split('-')
        return parts[0] + ''.join(word.capitalize() for word in parts[1:])


# Instancia global (se inicializa cuando se crea el tema)
_global_prefix_manager: Optional[PrefixManager] = None


def get_prefix_manager(theme_slug: Optional[str] = None, 
                      theme_textdomain: Optional[str] = None) -> PrefixManager:
    """Obtiene o crea la instancia global del PrefixManager."""
    global _global_prefix_manager
    if _global_prefix_manager is None or theme_slug:
        _global_prefix_manager = PrefixManager(theme_slug, theme_textdomain)
    return _global_prefix_manager


def initialize_prefix_manager(theme_slug: Optional[str] = None, 
                             theme_textdomain: Optional[str] = None):
    """Inicializa el PrefixManager global."""
    global _global_prefix_manager
    _global_prefix_manager = PrefixManager(theme_slug, theme_textdomain)

