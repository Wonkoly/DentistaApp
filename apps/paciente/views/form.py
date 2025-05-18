import flet as ft
import sys, os
import re

# Validaciones
def validar_nombre(nombre):
    return re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$', nombre)

def validar_telefono(telefono):
    return re.match(r'^\d{10}$', telefono)

# Ruta para importar colores globales
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from common import colors


def FormView(page: ft.Page) -> ft.View:
    # Controles del formulario
    nombre = ft.TextField(label="Nombre completo", autofocus=True)
    correo = ft.TextField(label="Correo electrónico")
    telefono = ft.TextField(label="Número de Teléfono")
    notas = ft.TextField(label="Notas (opcional)", multiline=True, min_lines=3, max_lines=5)

    alerta = ft.Text("", color=colors.ERROR)

    def continuar(e):
        nombre_valor = nombre.value.strip()
        correo_valor = correo.value.strip()
        telefono_valor = telefono.value.strip()

        if not nombre_valor or not correo_valor or not telefono_valor:
            alerta.value = "⚠️ Nombre, correo y teléfono son obligatorios."
            alerta.visible = True
            page.update()
            return

        if not validar_nombre(nombre_valor):
            alerta.value = "⚠️ El nombre solo debe contener letras y espacios."
            alerta.visible = True
            page.update()
            return

        if not validar_telefono(telefono_valor):
            alerta.value = "⚠️ El teléfono debe contener exactamente 10 números."
            alerta.visible = True
            page.update()
            return

        # Almacenar los datos
        page.client_storage.set("paciente", {
            "nombre": nombre_valor,
            "correo": correo_valor,
            "telefono": telefono_valor,
            "notas": notas.value.strip()
        })

        alerta.visible = False
        page.go("/confirm")

    return ft.View(
        route="/form",
        controls=[
            ft.Text("📝 Ingresa tu información personal", size=24, weight="bold", color=colors.SECONDARY),
            alerta,
            nombre,
            correo,
            telefono,
            notas,
            ft.ElevatedButton(
                text="Continuar",
                bgcolor=colors.PRIMARY,
                color=colors.TEXT_PRIMARY,
                on_click=continuar
            ),
            ft.TextButton("← Regresar al inicio", on_click=lambda _: page.go("/"))
        ],
        padding=20,
        vertical_alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
