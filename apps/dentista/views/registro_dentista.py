import flet as ft
import re
import requests
from typing import Tuple
from common import colors

API_REGISTER_URL = "http://localhost:8000/api/usuarios/registrar"

def validar_email(email: str) -> Tuple[bool, str]:
    pattern = r'^[\w\.-]+@([\w\.-]+\.\w+)$'
    match = re.match(pattern, email)
    if not match:
        return False, "Correo electrónico no válido"

    dominio = email.split('@')[1].lower()
    dominios_prohibidos = {
        "gmai.com": "¿Quisiste decir gmail.com?",
        "hotmial.com": "¿Quisiste decir hotmail.com?",
        "yaho.com": "¿Quisiste decir yahoo.com?",
        "outlok.com": "¿Quisiste decir outlook.com?",
        "gmal.com": "¿Quisiste decir gmail.com?"
    }

    if dominio in dominios_prohibidos:
        return False, dominios_prohibidos[dominio]

    return True, ""

def RegistroDentistaView(page: ft.Page):
    nombre_input = ft.TextField(label="Nombre", width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    apellido_input = ft.TextField(label="Apellido", width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    email_input = ft.TextField(label="Correo electrónico", width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    password_input = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    confirm_password_input = ft.TextField(label="Confirmar contraseña", password=True, can_reveal_password=True, width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    mensaje = ft.Text(value="", size=14)

    def registrar_handler(e):
        mensaje.color = colors.ERROR
        mensaje.value = ""

        nombre = nombre_input.value.strip()
        apellido = apellido_input.value.strip()
        correo = email_input.value.strip()
        contra = password_input.value.strip()
        contra2 = confirm_password_input.value.strip()

        # Validaciones
        if not all([nombre, apellido, correo, contra, contra2]):
            mensaje.value = "⚠️ Todos los campos son obligatorios"

        else:
            es_valido, mensaje_error = validar_email(correo)
            if not es_valido:
                mensaje.value = f"⚠️ {mensaje_error}"

            elif contra != contra2:
                mensaje.value = "⚠️ Las contraseñas no coinciden"

            elif len(contra) < 8 or len(contra) > 16:
                mensaje.value = "⚠️ La contraseña debe tener entre 8 y 16 caracteres"

            else:
                try:
                    response = requests.post(API_REGISTER_URL, json={
                        "nombre": nombre,
                        "apellido": apellido,
                        "email": correo,
                        "password": contra
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
