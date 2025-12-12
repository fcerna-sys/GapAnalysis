@echo off
REM Script de deployment del tema

set ACTION=%1
set TARGET=%2

if "%ACTION%"=="build" (
    echo 🔨 Construyendo tema...
    python deploy.py build
) else if "%ACTION%"=="deploy" (
    if "%TARGET%"=="" (
        echo ❌ Error: Especifica la ruta de destino
        echo Uso: deploy.bat deploy C:\path	o\wp-content	hemes
        exit /b 1
    )
    echo 🚀 Desplegando tema...
    python deploy.py deploy --target="%TARGET%"
) else if "%ACTION%"=="full" (
    if "%TARGET%"=="" (
        echo ❌ Error: Especifica la ruta de destino
        echo Uso: deploy.bat full C:\path	o\wp-content	hemes
        exit /b 1
    )
    echo 🔨 Construyendo y desplegando tema...
    python deploy.py full --target="%TARGET%"
) else (
    echo Uso: deploy.bat [build^|deploy^|full] [target_path]
    exit /b 1
)
