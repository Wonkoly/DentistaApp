import flet as ft
from components.navbar import navbar

def ConfiguracionView(page: ft.Page):
    return ft.View(
        route="/configuracion",
        appbar=navbar(page),
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Configuración del perfil", size=24),
                        ft.Text("Aquí puedes editar tu información personal.")
                    ]
                )
            )
        ]
    )
