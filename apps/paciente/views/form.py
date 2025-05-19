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
    # Encabezado con pasos marca los puntos de arriba con palomita.
    pasos = ft.Row(
    alignment=ft.MainAxisAlignment.CENTER,
    controls=[
        ft.Icon(name="check_circle", color=colors.SUCCESS, size=28),
        ft.Icon(name="check_circle", color=colors.TEXT_LIGHT, size=28),
        ft.Icon(name="check_circle", color=colors.TEXT_LIGHT, size=28),
    ]
)

    # Campos
    nombre = ft.TextField(label="Nombre completo", width=400)
    correo = ft.TextField(label="Correo electrónico", width=400)
    telefono = ft.TextField(label="Número de Teléfono", width=400)
    notas = ft.TextField(label="Notas (opcional)", multiline=True, width=400, min_lines=3, max_lines=5)

    # Mensaje de error
    mensaje_error = ft.Text("⚠️ Nombre, correo y teléfono son obligatorios", visible=False, color=colors.ERROR)

    # Función de validación
    def validar_formulario(e):
        nombre_valor = nombre.value.strip()
        correo_valor = correo.value.strip()
        telefono_valor = telefono.value.strip()

        if not nombre_valor or not correo_valor or not telefono_valor:
            mensaje_error.value = "⚠️ Todos los campos obligatorios deben estar llenos"
            mensaje_error.visible = True
            page.update()
            return

        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$', nombre_valor):
            mensaje_error.value = "⚠️ El nombre solo puede contener letras y espacios"
            mensaje_error.visible = True
            page.update()
            return

        if not telefono_valor.isdigit() or len(telefono_valor) != 10:
            mensaje_error.value = "⚠️ El teléfono debe contener exactamente 10 dígitos"
            mensaje_error.visible = True
            page.update()
            return

        # Guardar en almacenamiento local
        page.client_storage.set("paciente", {
            "nombre": nombre_valor,
            "correo": correo_valor,
            "telefono": telefono_valor,
            "notas": notas.value.strip()
        })

        page.go("/confirm")

    # Estilo tipo "tarjeta"
    tarjeta_formulario = ft.Container(
        content=ft.Column([
            ft.Text("📝 Ingresa tu información personal", size=22, weight="bold", color=colors.PRIMARY_DARK),
            mensaje_error,
            nombre,
            correo,
            telefono,
            notas,
            ft.ElevatedButton(
    text="Continuar",
    on_click=validar_formulario,
    bgcolor=colors.PRIMARY,
    style=ft.ButtonStyle(
        color="white",
        text_style=ft.TextStyle(weight="bold", size=14),
        padding=ft.Padding(12, 10, 12, 10)
    )
)

        ], spacing=15),
        bgcolor=colors.PRIMARY_LIGHT,
        border_radius=10,
        shadow=ft.BoxShadow(
    blur_radius=12,
    color="rgba(0,0,0,0.12)",  # sombra gris suave
    offset=ft.Offset(2, 2),
    spread_radius=1
),

        padding=30,
        width=450
    )

    return ft.View(
        route="/form",
        controls=[
            pasos,
            ft.VerticalDivider(opacity=0),  # Espacio
            tarjeta_formulario,
            ft.TextButton("← Regresar al inicio", on_click=lambda _: page.go("/"))
        ],
        scroll=ft.ScrollMode.AUTO,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
