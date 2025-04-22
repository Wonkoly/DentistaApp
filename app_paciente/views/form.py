import flet as ft

def form_view(page: ft.Page):
    def confirmar(e):
        page.go("/confirm")

    return ft.View(
        "/form",
        [
            ft.Text("Ingrese sus datos personales", size=24),
            ft.TextField(label="Nombre"),
            ft.TextField(label="Correo electrónico"),
            ft.TextField(label="Teléfono"),
            ft.ElevatedButton("Confirmar", on_click=confirmar)
        ]
    )
