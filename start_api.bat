@echo off
chcp 65001 >nul
echo 🚀 Iniciando API de Validación de Textos para Redes Sociales
echo ==========================================================

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado. Por favor instala Python 3.8+
    pause
    exit /b 1
)

REM Verificar si el entorno virtual existe
if not exist "venv" (
    echo 📦 Creando entorno virtual...
    python -m venv venv
)

REM Activar entorno virtual
echo 🔧 Activando entorno virtual...
call venv\Scripts\activate.bat

REM Verificar si las dependencias están instaladas
if not exist "venv\Lib\site-packages\fastapi" (
    echo 📥 Instalando dependencias...
    pip install -r requirements.txt
)

REM Verificar si los modelos están descargados
echo 🧠 Verificando modelos de IA...
python -c "from transformers import pipeline; from spanlp.palabrotas import Palabrotas; print('✅ Modelos verificados correctamente')" 2>nul
if errorlevel 1 (
    echo 📥 Descargando modelos de IA (esto puede tomar unos minutos)...
    python -c "from transformers import pipeline; from spanlp.palabrotas import Palabrotas; print('✅ Modelos descargados correctamente')"
)

echo.
echo 🌟 Todo listo! Iniciando la API...
echo 📖 Documentación disponible en: http://localhost:8000/docs
echo 🔍 Health check en: http://localhost:8000/health
echo.
echo Presiona Ctrl+C para detener la API
echo ==========================================================

REM Iniciar la API
python main.py

pause 