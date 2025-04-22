import flet as ft

def confirm_view(page: ft.Page):
    return ft.View(
        "/confirm",
        [
            ft.Text("¡Cita confirmada!", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("Recibirá un correo con los detalles.")
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
