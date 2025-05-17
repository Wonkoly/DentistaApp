
import flet as ft

def HomeView(page: ft.Page):
    page.bgcolor = ft.Colors.BLUE_GREY_900
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    email = ft.TextField(label="Correo electrónico", width=300)
    password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    mensaje_error = ft.Text("", color=ft.Colors.RED_300, size=12, visible=False, text_align="center")

    def iniciar_sesion(e):
        if not email.value or not password.value:
            mensaje_error.value = "Por favor completa todos los campos."
            mensaje_error.visible = True
        else:
            mensaje_error.visible = False
            # Aquí puedes agregar la lógica real de autenticación

        page.update()

    def ir_a_recuperar(e):
        page.go("/recuperar")

    def ir_a_registro(e):
        page.go("/registro")

    return ft.View(
        route="/",
        controls=[
            ft.Container(
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.CircleAvatar(content=ft.Text("RC"), bgcolor=ft.Colors.GREY_700, radius=30),
                        ft.Text("CLÍNICA CHOYO", size=24, weight="bold", color=ft.Colors.WHITE),
                        ft.Text("INICIAR SESIÓN COMO DENTISTA", size=14, color=ft.Colors.WHITE54),
                        email,
                        password,
                        mensaje_error,
                        ft.ElevatedButton("Iniciar sesión", icon=ft.Icons.LOGIN, bgcolor=ft.Colors.BLUE_500, on_click=iniciar_sesion),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            width=300,
                            controls=[
                                ft.TextButton("¿Olvidaste tu contraseña?", on_click=ir_a_recuperar),
                                ft.TextButton("Registrarse", on_click=ir_a_registro),
                            ]
                        ),
                        ft.Text("© 2025 Clínica Choyo - Puerto Vallarta", size=10, color=ft.Colors.WHITE24)
                    ]
                ),
                padding=40,
                bgcolor=ft.Colors.BLUE_GREY_800,
                border_radius=10,
            )
        ]
    )
