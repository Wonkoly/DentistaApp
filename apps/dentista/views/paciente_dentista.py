import flet as ft
from common import colors
from components.navbar import NavbarDentista

# Vista donde el dentista puede consultar pacientes registrados

def PacientesDentistaView(page: ft.Page):
    # Datos simulados (normalmente vendrían de la base de datos)
    pacientes = [
        {"nombre": "Carlos López", "correo": "carlos@example.com", "cita": "2025-05-20 17:00"},
        {"nombre": "Ana Torres", "correo": "ana@example.com", "cita": "2025-05-22 15:30"},
        {"nombre": "Luis Méndez", "correo": "luis@example.com", "cita": "2025-05-23 14:00"}
    ]

    items = []
    for paciente in pacientes:
        items.append(
            ft.Container(
                content=ft.Column([
                    ft.Text(paciente["nombre"], size=18, weight=ft.FontWeight.BOLD, color=colors.SECONDARY),
                    ft.Text(f"Correo: {paciente['correo']}", size=14, color=colors.TEXT_DARK),
                    ft.Text(f"Próxima cita: {paciente['cita']}", size=14, color=colors.TEXT_DARK)
                ]),
                padding=15,
                bgcolor=colors.PRIMARY_LIGHT,
                border_radius=10,
                margin=ft.margin.only(bottom=10)
            )
        )

    return ft.View(
        "/pacientes_dentista",
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Text("Listado de Pacientes", size=24, weight=ft.FontWeight.BOLD, color=colors.SECONDARY),
                    *items
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=30
            ),
            NavbarDentista(page=page, ruta_actual="pacientes")
        ]
    )
