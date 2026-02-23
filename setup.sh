#!/bin/bash

# Script de setup para desarrollo

echo "🚀 Configurando entorno DevOps Banco Pichincha..."

# Crear entorno virtual
echo "📦 Creando entorno virtual Python..."
python -m venv venv || virtualenv venv

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
fi

# Instalar dependencias
echo "📚 Instalando dependencias Python..."
pip install --upgrade pip
pip install -r src/requirements.txt

# Instalar pre-commit hooks
echo "🔍 Configurando pre-commit..."
pip install pre-commit
pre-commit install

# Copiar archivo de entorno
echo "⚙️ Configurando variables de entorno..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "⚠️  Por favor, edita el archivo .env con tus valores"
fi

echo "✅ Setup completado!"
echo "📝 Para iniciar el servicio en desarrollo: python src/app.py"
echo "🐳 Para construir con Docker: docker build -t devops-microservice ."
echo "🧪 Para ejecutar tests: pytest src/tests/"