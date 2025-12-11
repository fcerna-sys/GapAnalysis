# Blocks Builder - Estructura Modular

Este módulo está organizado por propósito para facilitar el mantenimiento y evitar problemas de recuperación.

## Estructura

```
blocks_builder/
├── __init__.py          # Exporta funciones principales
├── helpers.py           # ✅ Funciones auxiliares completas (BEM, CSS frameworks)
├── atoms.py             # ✅ Componentes atómicos completos (button, heading, input, etc.)
├── molecules.py         # ✅ Componentes moleculares completos (card, form-field, etc.)
├── organisms.py         # ⚠️ Importa funciones del backup + inyecta auxiliares
├── renders.py           # ⚠️ Importa funciones del backup (13 funciones de render)
├── editors.py           # ⚠️ Importa funciones del backup (8 funciones de editor)
├── styles.py            # ⚠️ Importa funciones del backup (2 funciones de estilos)
└── registration.py      # ✅ Funciones de registro completas
```

## Estado del Código

**✅ Código completo disponible:**
- Todos los módulos importan funciones desde `blocks_builder_backup.py`
- El código completo (2847 líneas) está preservado en el backup
- Los módulos actúan como "vistas organizadas" del código original
- **100% del código funcional está disponible**

**Módulos completos (código migrado):**
- `helpers.py`: Funciones auxiliares (get_bem_prefix, setup_css_framework, generate_bem_css)
- `atoms.py`: 6 átomos completos con implementación propia
- `molecules.py`: 5 moléculas completas con implementación propia
- `registration.py`: Funciones de registro completas

**Módulos que importan del backup (código preservado):**
- `renders.py`: 13 funciones de renderizado PHP
- `editors.py`: 8 funciones de editor JavaScript
- `styles.py`: 2 funciones de generación de CSS
- `organisms.py`: 13 funciones de creación de bloques complejos

## Uso

```python
from blocks_builder import create_custom_blocks, setup_css_framework

# Configurar framework CSS
setup_css_framework(theme_dir, 'tailwind')

# Crear todos los bloques
create_custom_blocks(theme_dir, 'tailwind', plan, theme_slug)
```

## Migración Gradual

El archivo `blocks_builder.py` en la raíz ahora es un wrapper que importa desde esta estructura modular, manteniendo compatibilidad hacia atrás.

**Próximos pasos (opcional):**
1. Migrar funciones de `renders.py` desde el backup
2. Migrar funciones de `editors.py` desde el backup
3. Migrar funciones de `styles.py` desde el backup
4. Migrar funciones de `organisms.py` desde el backup

Mientras tanto, todo el código funciona correctamente importando desde el backup.

