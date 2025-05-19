@echo off
cd /d %~dp0

echo Activando entorno virtual...
call .venv\Scripts\activate.bat

echo Iniciando API FastAPI...
start cmd /k uvicorn backend.main:app --reload

echo Iniciando app Dentista en Flet...
python apps\dentista\main.py

