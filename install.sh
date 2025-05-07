#!/bin/bash

echo "🚀 Proceso de instalación comenzado."
echo "🔍 Verificando entorno..."

# Backend
echo ""
echo "🔧 [1/5] Configurando entorno virtual para el backend..."
cd backend
python3 -m venv venv
source venv/bin/activate

echo "📦 Instalando dependencias del backend..."
pip install --upgrade pip
pip install -r requirements.txt
deactivate
cd ..

echo "✅ Backend instalado correctamente."

# Copiar webui.db desde contenedor Docker
echo ""
echo "📥 [2/5] Intentando copiar webui.db desde contenedor Docker..."
CONTAINER_ID=$(docker ps -aqf "name=openwebui")

if [ -n "$CONTAINER_ID" ]; then
    docker cp "$CONTAINER_ID":/app/backend/data/webui.db ./backend/webui.db && \
    echo "✅ webui.db copiado correctamente a ./backend/webui.db"
else
    echo "⚠️  No se encontró contenedor de OpenWebUI. Este paso se omitió."
fi

# Frontend
echo ""
echo "🎨 [3/5] Preparando frontend (SvelteKit)..."
cd frontend

if ! command -v npm &> /dev/null
then
    echo "❌ npm no está instalado. Por favor, instala Node.js y npm antes de continuar."
    exit 1
fi

echo "🧹 Limpiando posibles conflictos previos de npm/Vite..."
rm -rf node_modules .vite .svelte-kit dist package-lock.json
npm cache clean --force

echo "📦 Instalando dependencias del frontend..."
npm install

cd ..
echo "✅ Frontend instalado correctamente."

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