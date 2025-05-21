import flet as ft
from common import colors
from components.navbar import NavbarDentista

class HomeDentista(ft.View):
    def __init__(self, page: ft.Page):
        self.page = page
        usuario_nombre = page.session.get("usuario_nombre") or "Dentista"

        saludo = ft.Text(
            f"👋 Bienvenido, {usuario_nombre}",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=colors.PRIMARY_DARK
        )

        calendario_placeholder = ft.Container(
            content=ft.Text(
                "Aquí se mostrará el calendario con las citas del día.",
                size=18,
                text_align=ft.TextAlign.CENTER,
                color=colors.TEXT_DARK
            ),
            alignment=ft.alignment.center,
            padding=20,
            bgcolor=colors.PRIMARY_LIGHT,
            border_radius=10,
            width=360,
            height=300
        )

        info_consulta = ft.Text(
            "Selecciona una cita para ver detalles como nombre del paciente, correo, horario y motivo.",
            size=14,
            color=colors.SECONDARY
        )

        super().__init__(
            route="/home_dentista",
            controls=[
                ft.Container(
                    content=ft.Column([
                        saludo,
                        ft.Text("Calendario de Citas", size=24, weight=ft.FontWeight.BOLD, color=colors.SECONDARY),
                        calendario_placeholder,
                        info_consulta
                    ],
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=30
                ),
                NavbarDentista(page=page, ruta_actual="home")
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

async def HomeDentistaView(page: ft.Page):
    return HomeDentista(page)
