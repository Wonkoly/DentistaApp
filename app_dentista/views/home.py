import flet as ft

def login_view(page: ft.Page):
    def acceder(e):
        # En el futuro se conectará con el backend
        page.go("/")  # Por ahora no hace nada más

    return ft.View(
        route="/",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Bienvenido, Doctor", size=32, weight=ft.FontWeight.BOLD, text_align="center"),
                        ft.Text("Inicia sesión para acceder al sistema", size=18, text_align="center"),
                        ft.TextField(label="Correo electrónico", width=300),
                        ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300),
                        ft.ElevatedButton("Acceder", on_click=acceder)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                padding=40
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
