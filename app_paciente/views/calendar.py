import flet as ft

def CalandarView(page: ft.Page):
    
    def siguiente(e):
        page.go("/form")

    return ft.View(
        "/calendar",
        [
            ft.Text("Seleccione la fecha y hora de su cita", size=24),
            ft.ElevatedButton("Siguiente", on_click=siguiente)
        ]
    )
