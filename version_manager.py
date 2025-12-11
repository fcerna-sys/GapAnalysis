"""
Sistema de gestión de versiones y despliegue para temas WordPress.
Incluye: versionado automático, changelog, build, deploy.
"""
import os
import json
import shutil
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class VersionManager:
    """Gestiona versiones del tema y despliegue."""
    
    def __init__(self, theme_dir: str, theme_slug: Optional[str] = None):
        self.theme_dir = theme_dir
        self.theme_slug = theme_slug or 'img2html'
        self.version_file = os.path.join(theme_dir, 'version.json')
        self.changelog_file = os.path.join(theme_dir, 'CHANGELOG.json')
        self.build_dir = os.path.join(theme_dir, 'build')
        self.dist_dir = os.path.join(theme_dir, 'dist')
        
    def get_current_version(self) -> Dict:
        """Obtiene la versión actual del tema."""
        if os.path.isfile(self.version_file):
            with open(self.version_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'version': '1.0.0',
            'build': 1,
            'created': datetime.now().isoformat(),
            'updated': datetime.now().isoformat()
        }
    
    def bump_version(self, bump_type: str = 'patch') -> str:
        """
        Incrementa la versión del tema.
        bump_type: 'major', 'minor', 'patch', 'build'
        """
        current = self.get_current_version()
        version = current['version']
        build = current.get('build', 1)
        
        parts = version.split('.')
        major = int(parts[0])
        minor = int(parts[1]) if len(parts) > 1 else 0
        patch = int(parts[2]) if len(parts) > 2 else 0
        
        if bump_type == 'major':
            major += 1
            minor = 0
            patch = 0
        elif bump_type == 'minor':
            minor += 1
            patch = 0
        elif bump_type == 'patch':
            patch += 1
        elif bump_type == 'build':
            build += 1
        else:
            patch += 1
        
        new_version = f"{major}.{minor}.{patch}"
        
        version_data = {
            'version': new_version,
            'build': build,
            'created': current.get('created', datetime.now().isoformat()),
            'updated': datetime.now().isoformat(),
            'previous_version': version
        }
        
        with open(self.version_file, 'w', encoding='utf-8') as f:
            json.dump(version_data, f, indent=2)
        
        return new_version
    
    def add_changelog_entry(self, version: str, changes: List[str], change_type: str = 'patch'):
        """
        Agrega una entrada al changelog.
        change_type: 'major', 'minor', 'patch', 'hotfix'
        """
        changelog = self.get_changelog()
        
        entry = {
            'version': version,
            'date': datetime.now().isoformat(),
            'type': change_type,
            'changes': changes
        }
        
        changelog.insert(0, entry)
        
        # Mantener solo las últimas 50 entradas
        changelog = changelog[:50]
        
        with open(self.changelog_file, 'w', encoding='utf-8') as f:
            json.dump(changelog, f, indent=2)
    
    def get_changelog(self) -> List[Dict]:
        """Obtiene el changelog completo."""
        if os.path.isfile(self.changelog_file):
            with open(self.changelog_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def generate_changelog_md(self) -> str:
        """Genera un CHANGELOG.md legible desde el JSON."""
        changelog = self.get_changelog()
        
        md = f"# Changelog - {self.theme_slug}\n\n"
        md += "Todas las actualizaciones notables de este tema se documentarán en este archivo.\n\n"
        md += "El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).\n\n"
        
        for entry in changelog:
            version = entry.get('version', 'Unknown')
            date = entry.get('date', '')
            change_type = entry.get('type', 'patch')
            changes = entry.get('changes', [])
            
            # Formatear fecha
            try:
                dt = datetime.fromisoformat(date)
                date_str = dt.strftime('%Y-%m-%d')
            except:
                date_str = date
            
            # Emoji según tipo
            emoji = {
                'major': '🚀',
                'minor': '✨',
                'patch': '🐛',
                'hotfix': '🔧'
            }.get(change_type, '📝')
            
            md += f"## {emoji} [{version}] - {date_str}\n\n"
            
            if changes:
                for change in changes:
                    md += f"- {change}\n"
            else:
                md += "- Sin cambios documentados\n"
            
            md += "\n"
        
        return md
    
    def build_theme(self, minify: bool = True, purge: bool = True) -> str:
        """
        Construye el tema para producción.
        Retorna la ruta del archivo ZIP generado.
        """
        import subprocess
        
        print("🔨 Construyendo tema...")
        
        # 1. Incrementar build number
        current = self.get_current_version()
        build = current.get('build', 1) + 1
        version = current['version']
        
        # 2. Ejecutar optimizaciones si están disponibles
        if minify:
            try:
                print("  📦 Minificando assets...")
                subprocess.run(['npm', 'run', 'minify'], cwd=self.theme_dir, check=False, capture_output=True)
            except Exception as e:
                print(f"  ⚠️  Advertencia: No se pudo minificar: {e}")
        
        if purge:
            try:
                print("  🧹 Purgando CSS...")
                subprocess.run(['npm', 'run', 'purge'], cwd=self.theme_dir, check=False, capture_output=True)
            except Exception as e:
                print(f"  ⚠️  Advertencia: No se pudo purgar CSS: {e}")
        
        # 3. Crear directorio dist
        os.makedirs(self.dist_dir, exist_ok=True)
        
        # 4. Copiar archivos del tema (excluyendo build, node_modules, etc.)
        dist_theme_dir = os.path.join(self.dist_dir, self.theme_slug)
        if os.path.isdir(dist_theme_dir):
            shutil.rmtree(dist_theme_dir)
        
        shutil.copytree(
            self.theme_dir,
            dist_theme_dir,
            ignore=shutil.ignore_patterns(
                'node_modules',
                '.git',
                'build',
                'dist',
                '*.zip',
                '.env',
                '__pycache__',
                '*.pyc',
                '.DS_Store'
            )
        )
        
        # 5. Actualizar version.json en dist
        version_data = {
            'version': version,
            'build': build,
            'created': current.get('created', datetime.now().isoformat()),
            'updated': datetime.now().isoformat(),
            'build_date': datetime.now().isoformat()
        }
        
        dist_version_file = os.path.join(dist_theme_dir, 'version.json')
        with open(dist_version_file, 'w', encoding='utf-8') as f:
            json.dump(version_data, f, indent=2)
        
        # 6. Generar CHANGELOG.md
        changelog_md = self.generate_changelog_md()
        changelog_md_path = os.path.join(dist_theme_dir, 'CHANGELOG.md')
        with open(changelog_md_path, 'w', encoding='utf-8') as f:
            f.write(changelog_md)
        
        # 7. Crear ZIP
        zip_filename = f"{self.theme_slug}-{version}-build-{build}.zip"
        zip_path = os.path.join(self.dist_dir, zip_filename)
        
        print(f"  📦 Creando ZIP: {zip_filename}...")
        shutil.make_archive(
            zip_path.replace('.zip', ''),
            'zip',
            self.dist_dir,
            self.theme_slug
        )
        
        # 8. Actualizar build number
        current['build'] = build
        current['updated'] = datetime.now().isoformat()
        with open(self.version_file, 'w', encoding='utf-8') as f:
            json.dump(current, f, indent=2)
        
        print(f"✅ Build completado: {zip_filename}")
        return zip_path
    
    def deploy_theme(self, target_path: str, backup: bool = True) -> bool:
        """
        Despliega el tema a un directorio de WordPress.
        target_path: Ruta a wp-content/themes/
        """
        try:
            target_theme_dir = os.path.join(target_path, self.theme_slug)
            
            # 1. Backup si existe
            if backup and os.path.isdir(target_theme_dir):
                backup_dir = f"{target_theme_dir}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                print(f"📦 Creando backup: {os.path.basename(backup_dir)}...")
                shutil.copytree(target_theme_dir, backup_dir)
            
            # 2. Copiar desde dist
            dist_theme_dir = os.path.join(self.dist_dir, self.theme_slug)
            if not os.path.isdir(dist_theme_dir):
                print("❌ Error: No existe build. Ejecuta 'theme build' primero.")
                return False
            
            if os.path.isdir(target_theme_dir):
                shutil.rmtree(target_theme_dir)
            
            print(f"🚀 Desplegando a {target_path}...")
            shutil.copytree(dist_theme_dir, target_theme_dir)
            
            # 3. Actualizar permisos (Unix)
            try:
                os.chmod(target_theme_dir, 0o755)
                for root, dirs, files in os.walk(target_theme_dir):
                    for d in dirs:
                        os.chmod(os.path.join(root, d), 0o755)
                    for f in files:
                        os.chmod(os.path.join(root, f), 0o644)
            except Exception:
                pass  # Windows no necesita esto
            
            print("✅ Despliegue completado")
            return True
            
        except Exception as e:
            print(f"❌ Error en despliegue: {e}")
            return False
    
    def create_deployment_scripts(self):
        """Crea scripts de deployment automatizados."""
        # Script Python para build y deploy
        deploy_script = os.path.join(self.theme_dir, 'deploy.py')
        deploy_content = f"""#!/usr/bin/env python3
\"\"\"
Script de deployment del tema {self.theme_slug}
Uso: python deploy.py [build|deploy|full] [--target=/path/to/wp-content/themes]
\"\"\"
import sys
import os
import argparse
from version_manager import VersionManager

def main():
    parser = argparse.ArgumentParser(description='Deploy tema {self.theme_slug}')
    parser.add_argument('action', choices=['build', 'deploy', 'full'], 
                       help='Acción a ejecutar')
    parser.add_argument('--target', default=None,
                       help='Ruta de destino para deploy (wp-content/themes)')
    parser.add_argument('--no-minify', action='store_true',
                       help='No minificar assets')
    parser.add_argument('--no-purge', action='store_true',
                       help='No purgar CSS')
    parser.add_argument('--no-backup', action='store_true',
                       help='No crear backup al desplegar')
    parser.add_argument('--bump', choices=['major', 'minor', 'patch', 'build'],
                       help='Tipo de bump de versión')
    
    args = parser.parse_args()
    
    vm = VersionManager('{self.theme_dir}', '{self.theme_slug}')
    
    if args.bump:
        new_version = vm.bump_version(args.bump)
        print(f"📌 Nueva versión: {{new_version}}")
    
    if args.action in ['build', 'full']:
        vm.build_theme(minify=not args.no_minify, purge=not args.no_purge)
    
    if args.action in ['deploy', 'full']:
        if not args.target:
            print("❌ Error: --target es requerido para deploy")
            sys.exit(1)
        vm.deploy_theme(args.target, backup=not args.no_backup)
    
    print("✅ Completado")

if __name__ == '__main__':
    main()
"""
        
        with open(deploy_script, 'w', encoding='utf-8') as f:
            f.write(deploy_content)
        
        # Script bash
        deploy_sh = os.path.join(self.theme_dir, 'deploy.sh')
        deploy_sh_content = """#!/bin/bash
# Script de deployment del tema

ACTION=${1:-full}
TARGET=${2:-}

case $ACTION in
    build)
        echo "🔨 Construyendo tema..."
        python deploy.py build
        ;;
    deploy)
        if [ -z "$TARGET" ]; then
            echo "❌ Error: Especifica la ruta de destino"
            echo "Uso: ./deploy.sh deploy /path/to/wp-content/themes"
            exit 1
        fi
        echo "🚀 Desplegando tema..."
        python deploy.py deploy --target="$TARGET"
        ;;
    full)
        if [ -z "$TARGET" ]; then
            echo "❌ Error: Especifica la ruta de destino"
            echo "Uso: ./deploy.sh full /path/to/wp-content/themes"
            exit 1
        fi
        echo "🔨 Construyendo y desplegando tema..."
        python deploy.py full --target="$TARGET"
        ;;
    *)
        echo "Uso: ./deploy.sh [build|deploy|full] [target_path]"
        exit 1
        ;;
esac
"""
        
        with open(deploy_sh, 'w', encoding='utf-8') as f:
            f.write(deploy_sh_content)
        
        try:
            os.chmod(deploy_sh, 0o755)
        except Exception:
            pass
        
        # Script batch para Windows
        deploy_bat = os.path.join(self.theme_dir, 'deploy.bat')
        deploy_bat_content = """@echo off
REM Script de deployment del tema

set ACTION=%1
set TARGET=%2

if "%ACTION%"=="build" (
    echo 🔨 Construyendo tema...
    python deploy.py build
) else if "%ACTION%"=="deploy" (
    if "%TARGET%"=="" (
        echo ❌ Error: Especifica la ruta de destino
        echo Uso: deploy.bat deploy C:\path\to\wp-content\themes
        exit /b 1
    )
    echo 🚀 Desplegando tema...
    python deploy.py deploy --target="%TARGET%"
) else if "%ACTION%"=="full" (
    if "%TARGET%"=="" (
        echo ❌ Error: Especifica la ruta de destino
        echo Uso: deploy.bat full C:\path\to\wp-content\themes
        exit /b 1
    )
    echo 🔨 Construyendo y desplegando tema...
    python deploy.py full --target="%TARGET%"
) else (
    echo Uso: deploy.bat [build^|deploy^|full] [target_path]
    exit /b 1
)
"""
        
        with open(deploy_bat, 'w', encoding='utf-8') as f:
            f.write(deploy_bat_content)
        
        print("✓ Scripts de deployment creados")


def setup_version_management(theme_dir: str, theme_slug: Optional[str] = None, initial_changes: Optional[List[str]] = None):
    """
    Configura el sistema de gestión de versiones para un tema.
    """
    try:
        vm = VersionManager(theme_dir, theme_slug)
        
        # Inicializar version.json si no existe
        if not os.path.isfile(vm.version_file):
            version_data = {
                'version': '1.0.0',
                'build': 1,
                'created': datetime.now().isoformat(),
                'updated': datetime.now().isoformat()
            }
            with open(vm.version_file, 'w', encoding='utf-8') as f:
                json.dump(version_data, f, indent=2)
        
        # Inicializar changelog si no existe
        if not os.path.isfile(vm.changelog_file):
            changelog = []
            if initial_changes:
                changelog.append({
                    'version': '1.0.0',
                    'date': datetime.now().isoformat(),
                    'type': 'major',
                    'changes': initial_changes or ['Versión inicial del tema']
                })
            with open(vm.changelog_file, 'w', encoding='utf-8') as f:
                json.dump(changelog, f, indent=2)
        
        # Crear scripts de deployment
        vm.create_deployment_scripts()
        
        # Actualizar style.css con versión
        style_css_path = os.path.join(theme_dir, 'style.css')
        if os.path.isfile(style_css_path):
            try:
                with open(style_css_path, 'r', encoding='utf-8') as f:
                    style_content = f.read()
                
                version = vm.get_current_version()['version']
                
                # Actualizar o agregar versión en el header
                if 'Version:' in style_content:
                    style_content = re.sub(r'Version:\s*[\d.]+', f'Version: {version}', style_content)
                else:
                    # Agregar después de Theme Name
                    style_content = re.sub(
                        r'(Theme Name:.*\n)',
                        f'\\1Version: {version}\n',
                        style_content
                    )
                
                with open(style_css_path, 'w', encoding='utf-8') as f:
                    f.write(style_content)
            except Exception:
                pass  # Si no se puede actualizar, continuar
        
        print(f"✓ Sistema de versiones configurado (v{vm.get_current_version()['version']})")
        
    except Exception as e:
        print(f"Error al configurar versiones: {e}")
        import traceback
        traceback.print_exc()

