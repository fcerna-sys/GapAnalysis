#!/bin/bash
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
