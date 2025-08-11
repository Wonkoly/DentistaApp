import flet as ft
import httpx
from common import colors
from common.validators import validar_email

API_LOGIN_URL = "http://localhost:8000/api/usuarios/login"

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
        # Reset estilos
        mensaje.value = ""
        email_input.error_text = None
        password_input.error_text = None
        email_input.border_color = colors.PRIMARY
        password_input.border_color = colors.PRIMARY

        correo = email_input.value.strip()
        contrasena = password_input.value.strip()

        # Validación de correo
        es_valido, mensaje_error = validar_email(correo)
        if not es_valido:
            mensaje.value = f"⚠️ {mensaje_error}"
            email_input.error_text = mensaje_error
            email_input.border_color = colors.ERROR
        elif not contrasena:
            mensaje.value = "⚠️ Ingresa la contraseña"
            password_input.error_text = "Campo requerido"
            password_input.border_color = colors.ERROR
        elif len(contrasena) < 8 or len(contrasena) > 16:
            mensaje.value = "⚠️ La contraseña debe tener entre 8 y 16 caracteres"
            password_input.error_text = "Longitud inválida (8-16)"
            password_input.border_color = colors.ERROR
        else:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        API_LOGIN_URL,
                        json={"email": correo, "password": contrasena},
                        headers={"Content-Type": "application/json"}
                    )

                if response.status_code == 200:
                    datos = response.json()
                    mensaje.value = f"✅ Bienvenido, {datos['nombre']}"
                    mensaje.color = colors.SUCCESS

                    # Guardar sesión
                    page.session.set("usuario_id", datos["usuario_id"])
                    page.session.set("usuario_nombre", datos["nombre"])

                    page.go("/home_dentista")
                    return
                else:
                    mensaje.value = "❌ Usuario o contraseña incorrectos"
                    email_input.border_color = colors.ERROR
                    password_input.border_color = colors.ERROR

            except Exception as err:
                mensaje.value = f"❌ Error de conexión: {err}"

        # Actualizar interfaz
        email_input.update()
        password_input.update()
        mensaje.update()

    return ft.View(
        "/login_dentista",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
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
                            on_click=lambda _: page.go("/recuperar_dentista"),
                            style=ft.ButtonStyle(color=colors.SECONDARY)
                        ),
                        ft.TextButton(
                            "¿No tienes cuenta? Regístrate",
                            on_click=lambda _: page.go("/registro_dentista"),
                            style=ft.ButtonStyle(color=colors.SECONDARY_DARK)
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15
                ),
                padding=30,
                bgcolor=colors.PRIMARY_LIGHT,
                border_radius=10
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
