import flet as ft
from common import colors

# Vista para ingresar y validar el código de recuperación de contraseña

def ConfirmarCodigoView(page: ft.Page):
    codigo_input = ft.TextField(
        label="Código de verificación",
        width=300,
        border_color=colors.PRIMARY,
        focused_border_color=colors.PRIMARY_DARK
    )

    nueva_contra_input = ft.TextField(
        label="Nueva contraseña",
        password=True,
        can_reveal_password=True,
        width=300,
        border_color=colors.PRIMARY,
        focused_border_color=colors.PRIMARY_DARK
    )

    confirmar_contra_input = ft.TextField(
        label="Confirmar contraseña",
        password=True,
        can_reveal_password=True,
        width=300,
        border_color=colors.PRIMARY,
        focused_border_color=colors.PRIMARY_DARK
    )

    mensaje = ft.Text(value="", color=colors.ERROR, size=14)

    snackbar = ft.SnackBar(
        content=ft.Text("📨 Código reenviado al correo registrado.", color=colors.TEXT_PRIMARY),
        bgcolor=colors.SECONDARY
    )

    def confirmar_handler(e):
        if not all([codigo_input.value, nueva_contra_input.value, confirmar_contra_input.value]):
            mensaje.value = "⚠️ Todos los campos son obligatorios"
        elif nueva_contra_input.value != confirmar_contra_input.value:
            mensaje.value = "⚠️ Las contraseñas no coinciden"
        elif codigo_input.value != "123456":  # código simulado
            mensaje.value = "❌ Código inválido"
        else:
            mensaje.value = "✅ Contraseña actualizada exitosamente"
            page.go("/login_dentista")
        page.update()

    def reenviar_codigo(e):
        page.snack_bar = snackbar
        snackbar.open = True
        page.update()

    return ft.View(
        "/confirmar_codigo",
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Text("Confirmar Código", size=24, weight=ft.FontWeight.BOLD, color=colors.SECONDARY),
                    codigo_input,
                    nueva_contra_input,
                    confirmar_contra_input,
                    ft.ElevatedButton(
                        "Confirmar",
                        on_click=confirmar_handler,
                        bgcolor=colors.PRIMARY,
                        color=colors.TEXT_PRIMARY
                    ),
                    mensaje,
                    ft.TextButton(
                        "Reenviar código",
                        on_click=reenviar_codigo,
                        style=ft.ButtonStyle(color=colors.SECONDARY)
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
