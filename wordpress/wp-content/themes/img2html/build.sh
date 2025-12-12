#!/bin/bash
echo "🚀 Iniciando build del tema..."

# Instalar dependencias si no existen
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependencias..."
    npm install
fi

# Minificar CSS y JS
echo "🔨 Minificando assets..."
npm run minify

# Purga de CSS no usado
echo "🧹 Purgando CSS no usado..."
npm run purge

# Optimizar imágenes (requiere imagemin-cli)
if command -v imagemin &> /dev/null; then
    echo "🖼️  Optimizando imágenes..."
    imagemin assets/img/**/*.{jpg,png} --out-dir=assets/img-optimized
fi

echo "✅ Build completado!"
