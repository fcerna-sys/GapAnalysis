"""
Sistema de validación y normalización de nomenclatura BEM.
Asegura que todas las clases CSS sigan el formato: {prefijo}-{bloque}__{elemento}--{modificador}
"""
import re
from typing import Optional, List, Tuple


def validate_bem_class(class_name: str, bem_prefix: str) -> bool:
    """
    Valida que una clase CSS siga la nomenclatura BEM.
    
    Formato esperado:
    - Bloque: {prefijo}-{bloque}
    - Elemento: {prefijo}-{bloque}__{elemento}
    - Modificador: {prefijo}-{bloque}--{modificador} o {prefijo}-{bloque}__{elemento}--{modificador}
    
    Args:
        class_name: Nombre de la clase a validar
        bem_prefix: Prefijo BEM del tema
    
    Returns:
        True si la clase sigue BEM, False en caso contrario
    """
    if not class_name or not bem_prefix:
        return False
    
    # Patrón BEM: prefijo-bloque, prefijo-bloque__elemento, prefijo-bloque--modificador, etc.
    bem_pattern = rf'^{re.escape(bem_prefix)}-[a-z0-9-]+(__[a-z0-9-]+)?(--[a-z0-9-]+)?$'
    
    return bool(re.match(bem_pattern, class_name))


def generate_bem_class(
    bem_prefix: str,
    block: str,
    element: Optional[str] = None,
    modifier: Optional[str] = None
) -> str:
    """
    Genera una clase CSS siguiendo metodología BEM.
    
    Args:
        bem_prefix: Prefijo del tema (ej: 'mitema')
        block: Nombre del bloque (ej: 'hero', 'card', 'button')
        element: Nombre del elemento opcional (ej: 'title', 'content')
        modifier: Nombre del modificador opcional (ej: 'primary', 'destacada')
    
    Returns:
        Clase CSS en formato BEM (ej: 'mitema-hero__titulo--destacada')
    
    Examples:
        generate_bem_class('mitema', 'hero') -> 'mitema-hero'
        generate_bem_class('mitema', 'hero', 'titulo') -> 'mitema-hero__titulo'
        generate_bem_class('mitema', 'card', 'titulo', 'destacada') -> 'mitema-card__titulo--destacada'
        generate_bem_class('mitema', 'button', None, 'primary') -> 'mitema-button--primary'
    """
    # Normalizar nombres (solo minúsculas, guiones, números)
    def normalize(name: str) -> str:
        return re.sub(r'[^a-z0-9-]', '', name.lower().replace('_', '-').replace(' ', '-'))
    
    bem_prefix = normalize(bem_prefix)
    block = normalize(block)
    
    # Construir clase base
    class_parts = [bem_prefix, block]
    
    # Agregar elemento si existe
    if element:
        element = normalize(element)
        class_parts.append(f"__{element}")
    
    # Agregar modificador si existe
    if modifier:
        modifier = normalize(modifier)
        class_parts.append(f"--{modifier}")
    
    return ''.join(class_parts)


def extract_bem_parts(class_name: str, bem_prefix: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Extrae las partes de una clase BEM (bloque, elemento, modificador).
    
    Args:
        class_name: Clase CSS en formato BEM
        bem_prefix: Prefijo BEM del tema
    
    Returns:
        Tupla (bloque, elemento, modificador) o (None, None, None) si no es BEM válido
    """
    if not validate_bem_class(class_name, bem_prefix):
        return (None, None, None)
    
    # Remover prefijo
    without_prefix = class_name[len(bem_prefix) + 1:]  # +1 para el guión
    
    # Separar elemento y modificador
    parts = without_prefix.split('__')
    block = parts[0]
    
    element = None
    modifier = None
    
    if len(parts) > 1:
        element_and_mod = parts[1].split('--')
        element = element_and_mod[0]
        if len(element_and_mod) > 1:
            modifier = element_and_mod[1]
    else:
        # Modificador directo en el bloque
        block_parts = block.split('--')
        if len(block_parts) > 1:
            block = block_parts[0]
            modifier = block_parts[1]
    
    return (block, element, modifier)


def normalize_block_name(block_name: str) -> str:
    """
    Normaliza el nombre de un bloque para usar en BEM.
    Convierte a minúsculas, reemplaza espacios/guiones bajos por guiones.
    
    Args:
        block_name: Nombre del bloque (ej: 'Hero Section', 'text_image')
    
    Returns:
        Nombre normalizado (ej: 'hero-section', 'text-image')
    """
    normalized = re.sub(r'[^a-z0-9-]', '-', block_name.lower())
    normalized = re.sub(r'-+', '-', normalized)  # Múltiples guiones a uno solo
    return normalized.strip('-')


def ensure_bem_naming(
    class_name: str,
    bem_prefix: str,
    block: str,
    element: Optional[str] = None,
    modifier: Optional[str] = None
) -> str:
    """
    Asegura que una clase siga BEM. Si no lo hace, la genera correctamente.
    
    Args:
        class_name: Clase actual (puede no seguir BEM)
        bem_prefix: Prefijo BEM
        block: Nombre del bloque
        element: Elemento opcional
        modifier: Modificador opcional
    
    Returns:
        Clase CSS en formato BEM correcto
    """
    if validate_bem_class(class_name, bem_prefix):
        return class_name
    
    # Generar clase BEM correcta
    return generate_bem_class(bem_prefix, block, element, modifier)


__all__ = [
    'validate_bem_class',
    'generate_bem_class',
    'extract_bem_parts',
    'normalize_block_name',
    'ensure_bem_naming',
]

