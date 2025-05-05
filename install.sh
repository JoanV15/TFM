#!/bin/bash

echo "🚀 Instalador completo del sistema TFM (Backend + Frontend)"
echo "🔍 Verificando entorno..."

# Backend
echo ""
echo "🔧 [1/4] Configurando entorno virtual para el backend..."
cd backend
python3 -m venv venv
source venv/bin/activate

echo "📦 Instalando dependencias del backend..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Backend instalado correctamente."
deactivate
cd ..

# Frontend
echo ""
echo "🎨 [2/4] Instalando dependencias del frontend (SvelteKit)..."
cd frontend

if ! command -v npm &> /dev/null
then
    echo "❌ npm no está instalado. Por favor, instala Node.js y npm antes de continuar."
    exit 1
fi

npm install

echo "✅ Frontend instalado correctamente."
cd ..

# Instrucciones finales
echo ""
echo "🎉 Instalación completada con éxito."
echo ""
echo "👉 Para lanzar el backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload"
echo ""
echo "👉 Para lanzar el frontend:"
echo "   cd frontend"
echo "   npm run dev"
echo ""

