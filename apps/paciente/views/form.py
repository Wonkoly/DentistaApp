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
    pasos = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Icon(name="check_circle", color=colors.SUCCESS, size=28),
            ft.Icon(name="check_circle", color=colors.TEXT_LIGHT, size=28),
            ft.Icon(name="check_circle", color=colors.TEXT_LIGHT, size=28),
        ]
    )

    # Campos
    nombre = ft.TextField(label="Nombre", width=400)
    apellido = ft.TextField(label="Apellido", width=400)
    correo = ft.TextField(label="Correo electrónico", width=400)
    telefono = ft.TextField(label="Número de Teléfono", width=400)
    notas = ft.TextField(label="Notas (opcional)", multiline=True, width=400, min_lines=3, max_lines=5)

    mensaje_error = ft.Text("", visible=False, color=colors.ERROR)

    def validar_formulario(e):
        nombre_valor = nombre.value.strip()
        apellido_valor = apellido.value.strip()
        correo_valor = correo.value.strip()
        telefono_valor = telefono.value.strip()

        if not nombre_valor or not apellido_valor or not correo_valor or not telefono_valor:
            mensaje_error.value = "⚠️ Todos los campos obligatorios deben estar llenos"
            mensaje_error.visible = True
            page.update()
            return

        if not validar_nombre(nombre_valor) or not validar_nombre(apellido_valor):
            mensaje_error.value = "⚠️ Nombre y apellido solo deben contener letras"
            mensaje_error.visible = True
            page.update()
            return

        if len((nombre_valor + apellido_valor).replace(" ", "")) < 20:
            mensaje_error.value = "⚠️ Nombre completo debe tener al menos 20 letras"
            mensaje_error.visible = True
            page.update()
            return

        if not validar_telefono(telefono_valor):
            mensaje_error.value = "⚠️ El teléfono debe tener 10 dígitos"
            mensaje_error.visible = True
            page.update()
            return

        # Guardar en almacenamiento local
        page.client_storage.set("paciente", {
            "nombre": nombre_valor,
            "apellido": apellido_valor,
            "correo": correo_valor,
            "telefono": telefono_valor,
            "notas": notas.value.strip()
        })

        page.go("/confirm")

    tarjeta_formulario = ft.Container(
        content=ft.Column([
            ft.Text("📝 Ingresa tu información personal", size=22, weight="bold", color=colors.PRIMARY_DARK),
            mensaje_error,
            nombre,
            apellido,
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
            color="rgba(0,0,0,0.12)",
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
            ft.VerticalDivider(opacity=0),
            tarjeta_formulario,
            ft.TextButton("← Regresar al inicio", on_click=lambda _: page.go("/"))
        ],
        scroll=ft.ScrollMode.AUTO,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )