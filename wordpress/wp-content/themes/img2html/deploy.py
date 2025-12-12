#!/usr/bin/env python3
"""
Script de deployment del tema img2html
Uso: python deploy.py [build|deploy|full] [--target=/path/to/wp-content/themes]
"""
import sys
import os
import argparse
from version_manager import VersionManager

def main():
    parser = argparse.ArgumentParser(description='Deploy tema img2html')
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
    
    vm = VersionManager('c:\\laragon\\www\\img2html\\wp_theme', 'img2html')
    
    if args.bump:
        new_version = vm.bump_version(args.bump)
        print(f"📌 Nueva versión: {new_version}")
    
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
