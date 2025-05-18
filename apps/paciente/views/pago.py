import flet as ft

def PagoView(page: ft.Page) -> ft.View:
    return ft.View(
        route="/pago",
        controls=[
            ft.Text("💳 Pago en línea"),
        ]
    )
