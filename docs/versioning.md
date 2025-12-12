# Sistema de Gestión de Versiones y Despliegue

Este documento explica cómo usar el sistema de versiones y despliegue del tema.

## Archivos del Sistema

- `version.json`: Información de versión actual del tema
- `CHANGELOG.json`: Registro de cambios en formato JSON
- `CHANGELOG.md`: Changelog legible generado automáticamente
- `deploy.py`: Script principal de deployment
- `deploy.sh` / `deploy.bat`: Scripts de conveniencia

## Comandos Disponibles

### Build del Tema

Construye el tema para producción con todas las optimizaciones:

```bash
# Usando Python directamente
python deploy.py build

# Usando script de conveniencia
./deploy.sh build
# o en Windows
deploy.bat build
```

**Opciones:**
- `--no-minify`: No minificar assets
- `--no-purge`: No purgar CSS no usado

**Resultado:**
- Crea directorio `dist/` con el tema optimizado
- Genera ZIP en `dist/` con nombre `{theme-slug}-{version}-build-{build}.zip`
- Actualiza `version.json` con nuevo build number

### Despliegue del Tema

Despliega el tema a un directorio de WordPress:

```bash
# Usando Python directamente
python deploy.py deploy --target=/path/to/wp-content/themes

# Usando script de conveniencia
./deploy.sh deploy /path/to/wp-content/themes
# o en Windows
deploy.bat deploy C:\path\to\wp-content\themes
```

**Opciones:**
- `--no-backup`: No crear backup antes de desplegar

**Resultado:**
- Copia el tema desde `dist/` al directorio especificado
- Crea backup automático si existe versión anterior
- Actualiza permisos de archivos

### Build + Deploy Completo

Ejecuta build y deploy en un solo comando:

```bash
python deploy.py full --target=/path/to/wp-content/themes
./deploy.sh full /path/to/wp-content/themes
```

## Gestión de Versiones

### Incrementar Versión

```bash
# Incrementar patch (1.0.0 -> 1.0.1)
python deploy.py build --bump=patch

# Incrementar minor (1.0.0 -> 1.1.0)
python deploy.py build --bump=minor

# Incrementar major (1.0.0 -> 2.0.0)
python deploy.py build --bump=major

# Incrementar solo build number
python deploy.py build --bump=build
```

### Agregar Entrada al Changelog

```python
from version_manager import VersionManager

vm = VersionManager('wp_theme', 'mi-tema')
vm.add_changelog_entry(
    version='1.0.1',
    changes=[
        'Corregido bug en slider',
        'Mejorado rendimiento de galería',
        'Agregado soporte para WebP'
    ],
    change_type='patch'
)
```

### Ver Changelog

```python
from version_manager import VersionManager

vm = VersionManager('wp_theme', 'mi-tema')
changelog = vm.get_changelog()
print(vm.generate_changelog_md())
```

## Estructura de version.json

```json
{
  "version": "1.0.0",
  "build": 42,
  "created": "2025-01-15T10:30:00",
  "updated": "2025-01-20T14:45:00",
  "previous_version": "0.9.9"
}
```

## Estructura de CHANGELOG.json

```json
[
  {
    "version": "1.0.1",
    "date": "2025-01-20T14:45:00",
    "type": "patch",
    "changes": [
      "Corregido bug en slider",
      "Mejorado rendimiento"
    ]
  },
  {
    "version": "1.0.0",
    "date": "2025-01-15T10:30:00",
    "type": "major",
    "changes": [
      "Versión inicial del tema"
    ]
  }
]
```

## Tipos de Cambios

- **major**: Cambios incompatibles con versiones anteriores
- **minor**: Nuevas funcionalidades compatibles
- **patch**: Correcciones de bugs compatibles
- **hotfix**: Correcciones urgentes

## Workflow Recomendado

### Desarrollo

1. Hacer cambios en el tema
2. Probar localmente
3. Agregar entrada al changelog si es necesario

### Preparar Release

```bash
# 1. Incrementar versión
python deploy.py build --bump=minor

# 2. Agregar changelog manualmente si es necesario
# (o se genera automáticamente)

# 3. Build del tema
python deploy.py build
```

### Desplegar a Producción

```bash
# Desplegar a servidor
python deploy.py deploy --target=/var/www/html/wp-content/themes

# O build + deploy en uno
python deploy.py full --target=/var/www/html/wp-content/themes
```

## Integración con CI/CD

### GitHub Actions

```yaml
name: Build and Deploy Theme

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build theme
        run: python deploy.py build
      - name: Upload artifact
        uses: actions/upload-artifact@v2
        with:
          name: theme-build
          path: dist/*.zip
```

### GitLab CI

```yaml
build:
  script:
    - python deploy.py build
  artifacts:
    paths:
      - dist/*.zip
```

## Mejores Prácticas

1. **Siempre hacer build antes de deploy**: Asegura que el tema esté optimizado
2. **Usar backups**: El sistema crea backups automáticos, pero puedes desactivarlos con `--no-backup`
3. **Documentar cambios**: Agrega entradas al changelog para cambios significativos
4. **Versionar correctamente**: Usa semantic versioning (major.minor.patch)
5. **Probar en staging**: Despliega primero a un entorno de pruebas

## Troubleshooting

### Error: "No existe build"
**Solución**: Ejecuta `python deploy.py build` primero

### Error: "Permisos denegados"
**Solución**: Asegúrate de tener permisos de escritura en el directorio de destino

### Error: "npm no encontrado"
**Solución**: Las optimizaciones (minify/purge) requieren Node.js. Instala Node.js o usa `--no-minify --no-purge`


