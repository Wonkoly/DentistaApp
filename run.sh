#!/bin/bash

echo "🐍 Activando entorno virtual..."
. .venv/bin/activate

echo "🚀 Iniciando API FastAPI..."
uvicorn backend.main:app --reload &

echo "🦷 Iniciando app Dentista en Flet..."
python apps/dentista/main.py

