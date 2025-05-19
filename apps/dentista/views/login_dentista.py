import flet as ft
import re
import httpx
from common import colors

API_LOGIN_URL = "http://localhost:8000/api/usuarios/login"

def validar_email(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

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
        if not validar_email(email_input.value):
            mensaje.value = "⚠️ Correo inválido"
            mensaje.color = colors.ERROR
        elif not password_input.value:
            mensaje.value = "⚠️ Ingresa la contraseña"
            mensaje.color = colors.ERROR
        else:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(API_LOGIN_URL, params={
                        "email": email_input.value,
                        "password": password_input.value
                    })

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

            except Exception as err:
                mensaje.value = f"❌ Error de conexión: {err}"
                mensaje.color = colors.ERROR

        page.update()


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
