#!/usr/bin/env fish

# Navegar al directorio raíz del proyecto
cd (dirname (status --current-filename))

echo "🦷 Iniciando app Dentista en Flet..."
python apps/dentista/main.py &

#echo "🦷 Iniciando app Dentista en Flet..."
#python apps/paciente/main.py


