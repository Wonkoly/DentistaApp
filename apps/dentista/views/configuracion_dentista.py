import flet as ft
from common import colors
from components.navbar import NavbarDentista

# Vista para actualizar datos del dentista, incluida su contraseña y foto

def ConfiguracionDentistaView(page: ft.Page):
    nombre_input = ft.TextField(label="Nombre", width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    apellido_input = ft.TextField(label="Apellido", width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    correo_input = ft.TextField(label="Correo", width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    nueva_contra_input = ft.TextField(label="Nueva contraseña", password=True, can_reveal_password=True, width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    foto_input = ft.TextField(label="Ruta de la fotografía (opcional)", width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)

    mensaje = ft.Text(value="", color=colors.SUCCESS, size=14)

    def guardar_configuracion(e):
        # En proyecto real, guardar los datos modificados en la base
        mensaje.value = "✅ Cambios guardados correctamente"
        page.update()

    return ft.View(
        "/configuracion_dentista",
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Text("Configuración del Perfil", size=24, weight=ft.FontWeight.BOLD, color=colors.SECONDARY),
                    nombre_input,
                    apellido_input,
                    correo_input,
                    nueva_contra_input,
                    foto_input,
                    ft.ElevatedButton(
                        "Guardar cambios",
                        on_click=guardar_configuracion,
                        bgcolor=colors.PRIMARY,
                        color=colors.TEXT_PRIMARY
                    ),
                    mensaje
                ],
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=30,
                bgcolor=colors.PRIMARY_LIGHT,
                border_radius=10
            ),
            NavbarDentista(page=page, ruta_actual="configuracion")
        ]
    )
