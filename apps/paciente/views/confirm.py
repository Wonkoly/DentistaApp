import flet as ft

def ConfirmView(page: ft.Page) -> ft.View:
    return ft.View(
        route="/confirm",
        controls=[
            ft.Text("✅ Confirmación de cita"),
        ]
    )
