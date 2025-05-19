import flet as ft
from common import colors
from components.navbar import NavbarDentista

# Vista para mostrar servicios y registrar citas manualmente

def ServiciosDentistaView(page: ft.Page):
    servicio_dropdown = ft.Dropdown(
        label="Selecciona un servicio",
        options=[
            ft.dropdown.Option("Limpieza Bucal"),
            ft.dropdown.Option("Extracción Dental"),
            ft.dropdown.Option("Obturación"),
            ft.dropdown.Option("Ortodoncia"),
            ft.dropdown.Option("Blanqueamiento"),
            ft.dropdown.Option("Carillas Dentales")
        ],
        width=300,
        border_color=colors.PRIMARY,
        focused_border_color=colors.PRIMARY_DARK
    )

    nombre_input = ft.TextField(label="Nombre del paciente", width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    correo_input = ft.TextField(label="Correo del paciente", width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    fecha_input = ft.TextField(label="Fecha (YYYY-MM-DD)", width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    hora_input = ft.TextField(label="Hora (HH:MM)", width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    mensaje = ft.Text(value="", color=colors.ERROR, size=14)

    def registrar_cita(e):
        if not all([servicio_dropdown.value, nombre_input.value, correo_input.value, fecha_input.value, hora_input.value]):
            mensaje.value = "⚠️ Todos los campos son obligatorios"
        else:
            mensaje.value = f"✅ Cita registrada para {nombre_input.value} el {fecha_input.value} a las {hora_input.value}"
        page.update()

    return ft.View(
        "/servicios_dentista",
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Text("Registro Manual de Cita", size=24, weight=ft.FontWeight.BOLD, color=colors.SECONDARY),
                    servicio_dropdown,
                    nombre_input,
                    correo_input,
                    fecha_input,
                    hora_input,
                    ft.ElevatedButton(
                        "Registrar cita",
                        on_click=registrar_cita,
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
            NavbarDentista(page=page, ruta_actual="servicios")
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
