import flet as ft
import re
import requests
from common import colors

API_REGISTER_URL = "http://localhost:8000/api/usuarios/registrar"

def validar_email(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def RegistroDentistaView(page: ft.Page):
    nombre_input = ft.TextField(label="Nombre", width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    apellido_input = ft.TextField(label="Apellido", width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    email_input = ft.TextField(label="Correo electrónico", width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    password_input = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    confirm_password_input = ft.TextField(label="Confirmar contraseña", password=True, can_reveal_password=True, width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    mensaje = ft.Text(value="", size=14)

    def registrar_handler(e):
        mensaje.color = colors.ERROR

        if not all([nombre_input.value, apellido_input.value, email_input.value, password_input.value, confirm_password_input.value]):
            mensaje.value = "⚠️ Todos los campos son obligatorios"
        elif not validar_email(email_input.value):
            mensaje.value = "⚠️ Correo electrónico no válido"
        elif password_input.value != confirm_password_input.value:
            mensaje.value = "⚠️ Las contraseñas no coinciden"
        else:
            try:
                response = requests.post(API_REGISTER_URL, params={
                    "nombre": nombre_input.value,
                    "apellido": apellido_input.value,
                    "email": email_input.value,
                    "password": password_input.value
                })

                if response.status_code == 200:
                    mensaje.value = "✅ Usuario registrado exitosamente"
                    mensaje.color = colors.SUCCESS
                    page.update()
                    page.go("/login_dentista")
                    return
                else:
                    mensaje.value = "❌ Error al registrar: " + response.text
            except Exception as ex:
                mensaje.value = f"❌ Error de conexión: {ex}"

        page.update()

    def ir_a_login(e):
        page.go("/login_dentista")

    return ft.View(
        "/registro_dentista",
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Text("Registro - Dentista", size=24, weight=ft.FontWeight.BOLD, color=colors.SECONDARY),
                    nombre_input,
                    apellido_input,
                    email_input,
                    password_input,
                    confirm_password_input,
                    ft.ElevatedButton(
                        "Registrarse",
                        on_click=registrar_handler,
                        bgcolor=colors.PRIMARY,
                        color=colors.TEXT_PRIMARY,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                        width=300
                    ),
                    mensaje,
                    ft.TextButton(
                        "¿Ya tienes cuenta? Inicia sesión",
                        on_click=ir_a_login,
                        style=ft.ButtonStyle(color=colors.SECONDARY)
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15),
                padding=30,
                bgcolor=colors.PRIMARY_LIGHT,
                border_radius=10
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
