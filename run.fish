#!/usr/bin/env fish

# Navegar al directorio raíz del proyecto
cd (dirname (status --current-filename))

echo "🐍 Activando entorno virtual (.venv)..."
source .venv/bin/activate.fish

echo "🚀 Iniciando API FastAPI..."
uvicorn backend.main:app --reload &

#echo "🦷 Iniciando app Dentista en Flet..."
#python apps/dentista/main.py &

#echo "🦷 Iniciando app Dentista en Flet..."
#python apps/paciente/main.py


