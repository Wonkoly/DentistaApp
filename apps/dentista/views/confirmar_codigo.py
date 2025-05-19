import flet as ft
from common import colors

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
            mensaje.color = colors.ERROR
        elif nueva_contra_input.value != confirmar_contra_input.value:
            mensaje.value = "⚠️ Las contraseñas no coinciden"
            mensaje.color = colors.ERROR
        elif codigo_input.value != "123456":  # código simulado
            mensaje.value = "❌ Código inválido"
            mensaje.color = colors.ERROR
        else:
            mensaje.value = "✅ Contraseña actualizada exitosamente"
            mensaje.color = colors.SUCCESS
            page.update()
            page.go("/login_dentista")
            return

        page.update()

    def reenviar_codigo(e):
        page.snack_bar = snackbar
        snackbar.open = True
        page.update()

    def volver(e):
        page.go("/recuperar_dentista")

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
                        color=colors.TEXT_PRIMARY,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                        width=300
                    ),
                    mensaje,
                    ft.Row(
                        [
                            ft.TextButton(
                                "Reenviar código",
                                on_click=reenviar_codigo,
                                style=ft.ButtonStyle(color=colors.SECONDARY)
                            ),
                            ft.TextButton(
                                "Volver",
                                on_click=volver,
                                style=ft.ButtonStyle(color=colors.SECONDARY_DARK)
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
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
