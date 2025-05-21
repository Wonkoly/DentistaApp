import flet as ft
import re
import httpx
from common import colors
from typing import Tuple


API_LOGIN_URL = "http://localhost:8000/api/usuarios/login"

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

def LoginDentistaView(page: ft.Page):
    email_input = ft.TextField(
        label="Correo electrónico",
        width=300,
        border_color=colors.PRIMARY,
        focused_border_color=colors.PRIMARY_DARK
    )

    password_input = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=300,
        border_color=colors.PRIMARY,
        focused_border_color=colors.PRIMARY_DARK
    )

    mensaje = ft.Text(value="", color=colors.ERROR, size=14)

    async def login_handler(e):
        # Reiniciar estilos de error
        email_input.error_text = None
        password_input.error_text = None
        email_input.border_color = colors.PRIMARY
        password_input.border_color = colors.PRIMARY

        correo = email_input.value.strip()
        contrasena = password_input.value.strip()

        es_valido, mensaje_error = validar_email(correo)

        if not es_valido:
            mensaje.value = f"⚠️ {mensaje_error}"
            mensaje.color = colors.ERROR
            email_input.error_text = mensaje_error
            email_input.border_color = colors.ERROR

        elif not contrasena:
            mensaje.value = "⚠️ Ingresa la contraseña"
            mensaje.color = colors.ERROR
            password_input.error_text = "Campo requerido"
            password_input.border_color = colors.ERROR

        elif len(contrasena) < 8 or len(contrasena) > 16:
            mensaje.value = "⚠️ La contraseña debe tener entre 8 y 16 caracteres"
            mensaje.color = colors.ERROR
            password_input.error_text = "Longitud inválida (8-16)"
            password_input.border_color = colors.ERROR

        else:
            try:
                async with httpx.AsyncClient() as client:
                    headers = {"Content-Type": "application/json"}
                    response = await client.post(
                        API_LOGIN_URL,
                        json={
                            "email": correo,
                            "password": contrasena
                        },
                        headers=headers
    )



                if response.status_code == 200:
                    datos = response.json()
                    mensaje.value = f"✅ Bienvenido, {datos['nombre']}"
                    mensaje.color = colors.SUCCESS

                    # Guardamos datos del usuario en la sesión (memoria temporal)
                    page.session.set("usuario_id", datos["usuario_id"])
                    page.session.set("usuario_nombre", datos["nombre"])
                    page.go("/home_dentista")
                    return
                else:
                    mensaje.value = "❌ Usuario o contraseña incorrectos"
                    mensaje.color = colors.ERROR
                    email_input.border_color = colors.ERROR
                    password_input.border_color = colors.ERROR

            except Exception as err:
                mensaje.value = f"❌ Error de conexión: {err}"
                mensaje.color = colors.ERROR

        email_input.update()
        password_input.update()
        mensaje.update()

    return ft.View(
        "/login_dentista",
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Iniciar sesión - Dentista",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=colors.SECONDARY
                    ),
                    email_input,
                    password_input,
                    ft.ElevatedButton(
                        "Ingresar",
                        on_click=login_handler,
                        bgcolor=colors.PRIMARY,
                        color=colors.TEXT_PRIMARY
                    ),
                    mensaje,
                    ft.TextButton(
                        "¿Olvidaste tu contraseña?",
                        url="/recuperar_dentista",
                        style=ft.ButtonStyle(color=colors.SECONDARY)
                    ),
                    ft.TextButton(
                        "¿No tienes cuenta? Regístrate",
                        url="/registro_dentista",
                        style=ft.ButtonStyle(color=colors.SECONDARY_DARK)
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
