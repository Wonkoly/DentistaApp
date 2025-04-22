import flet as ft

def home_view(page: ft.Page):
    def continuar(e):
        page.go("/calendar")

    return ft.View(
        "/",
        [
            ft.Text("Bienvenido a Clínica Dental", size=30, weight=ft.FontWeight.BOLD),
            ft.Text("Seleccione un servicio para continuar."),
            ft.ElevatedButton("Continuar", on_click=continuar)
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
