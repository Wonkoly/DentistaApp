import flet as ft
import re
from common import colors

# Vista para recuperación de contraseña del dentista

def RecuperarDentistaView(page: ft.Page):
    email_input = ft.TextField(
        label="Correo electrónico",
        width=300,
        border_color=colors.PRIMARY,
        focused_border_color=colors.PRIMARY_DARK
    )

    telefono_input = ft.TextField(
        label="Número de teléfono",
        width=300,
        border_color=colors.PRIMARY,
        focused_border_color=colors.PRIMARY_DARK
    )

    mensaje = ft.Text(value="", color=colors.ERROR, size=14)

    def validar_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def enviar_codigo(e):
        if not validar_email(email_input.value):
            mensaje.value = "⚠️ Correo inválido"
        elif not telefono_input.value:
            mensaje.value = "⚠️ Número de teléfono requerido"
        else:
            mensaje.value = "📩 Código enviado al correo y teléfono registrado."
            page.go("/confirmar_codigo")
        page.update()

    def volver_login(e):
        page.go("/login_dentista")

    return ft.View(
        "/recuperar_dentista",
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Text("Recuperar contraseña", size=24, weight=ft.FontWeight.BOLD, color=colors.SECONDARY),
                    email_input,
                    telefono_input,
                    ft.ElevatedButton(
                        "Enviar código",
                        on_click=enviar_codigo,
                        bgcolor=colors.PRIMARY,
                        color=colors.TEXT_PRIMARY,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                        width=300
                    ),
                    mensaje,
                    ft.TextButton(
                        "Volver al login",
                        on_click=volver_login,
                        style=ft.ButtonStyle(color=colors.SECONDARY_DARK)
                    )
                ],
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=30,
                bgcolor=colors.PRIMARY_LIGHT,
                border_radius=10
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
