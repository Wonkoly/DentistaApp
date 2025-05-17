import flet as ft

def navbar(page: ft.Page):
    return ft.AppBar(
        title=ft.Text("Clínica Choyo"),
        center_title=False,
        bgcolor=ft.colors.BLUE_GREY_800,
        actions=[
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Calendario", on_click=lambda e: page.go("/calendario_dentista")),
                    ft.PopupMenuItem(text="Pacientes", on_click=lambda e: page.go("/pacientes")),
                    ft.PopupMenuItem(text="Servicios", on_click=lambda e: page.go("/servicios")),
                    ft.PopupMenuItem(text="Configuración", on_click=lambda e: page.go("/configuracion")),
                    ft.PopupMenuItem(),  # Separador
                    ft.PopupMenuItem(text="Cerrar sesión", on_click=lambda e: page.go("/"))
                ]
            )
        ]
    )
