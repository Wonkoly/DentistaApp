import flet as ft
from components.navbar import navbar

def ServiciosView(page: ft.Page):
    return ft.View(
        route="/servicios",
        appbar=navbar(page),
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Servicios del consultorio", size=24),
                        ft.Text("Aquí irán los servicios disponibles para agendar.")
                    ]
                )
            )
        ]
    )
