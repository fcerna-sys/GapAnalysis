@echo off
echo 🚀 Iniciando build del tema...

REM Instalar dependencias si no existen
if not exist "node_modules" (
    echo 📦 Instalando dependencias...
    call npm install
)

REM Minificar CSS y JS
echo 🔨 Minificando assets...
call npm run minify

REM Purga de CSS no usado
echo 🧹 Purgando CSS no usado...
call npm run purge

echo ✅ Build completado!
pause
