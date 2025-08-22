#!/bin/bash

echo "🚀 Iniciando API de Validación de Textos para Redes Sociales"
echo "=========================================================="

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado. Por favor instala Python 3.8+"
    exit 1
fi

# Verificar si el entorno virtual existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Verificar si las dependencias están instaladas
if [ ! -f "venv/lib/python*/site-packages/fastapi" ]; then
    echo "📥 Instalando dependencias..."
    pip install -r requirements.txt
fi

# Verificar si los modelos están descargados
echo "🧠 Verificando modelos de IA..."
python3 -c "
from transformers import pipeline
from spanlp.palabrotas import Palabrotas
print('✅ Modelos verificados correctamente')
" 2>/dev/null || {
    echo "📥 Descargando modelos de IA (esto puede tomar unos minutos)..."
    python3 -c "
from transformers import pipeline
from spanlp.palabrotas import Palabrotas
print('✅ Modelos descargados correctamente')
"
}

echo ""
echo "🌟 Todo listo! Iniciando la API..."
echo "📖 Documentación disponible en: http://localhost:8000/docs"
echo "🔍 Health check en: http://localhost:8000/health"
echo ""
echo "Presiona Ctrl+C para detener la API"
echo "=========================================================="

# Iniciar la API
python3 main.py 