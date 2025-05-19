import flet as ft
from common import colors
from components.navbar import NavbarDentista

def HomeDentistaView(page: ft.Page):
    # Obtener nombre del dentista desde la sesión
    nombre_dentista = page.session.get("usuario_nombre") or "Dentista"

    saludo = ft.Text(
        f"👋 Bienvenido, {nombre_dentista}",
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

    return ft.View(
        "/home_dentista",
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
        ]
    )
