import flet as ft
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from common import colors


def HomeView(page: ft.Page) -> ft.View:
    def ir_a_seccion(e):
        destino = e.control.value
        if destino == "Tratamientos":
            page.go("/tratamientos")
        elif destino == "Clínica":
            page.go("/clinica")
        elif destino == "Opiniones":
            page.go("/opiniones")

    return ft.View(
        route="/",
        padding=30,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Text("Bienvenido a Clínica Dental 'CHOYO'", size=26, weight="bold", color=colors.PRIMARY_DARK),
            ft.Text("Selecciona una opción para continuar", size=18, color=colors.SECONDARY),
            ft.Divider(height=20, color="transparent"),

            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.ElevatedButton(
                        text="📅 Agendar Cita",
                        icon=ft.Icons.EVENT_AVAILABLE,
                        on_click=lambda _: page.go("/calendar"),
                        bgcolor=colors.PRIMARY,
                        color=colors.TEXT_PRIMARY
                    ),
                    ft.Dropdown(
                        label="Más opciones",
                        width=200,
                        options=[
                            ft.dropdown.Option("Tratamientos"),
                            ft.dropdown.Option("Clínica"),
                            ft.dropdown.Option("Opiniones")
                        ],
                        on_change=ir_a_seccion
                    ),
                ]
            ),

            ft.Divider(height=30, color="transparent"),

        ]
    )
