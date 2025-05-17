
import flet as ft

def RegistroView(page: ft.Page):
    def registrar(e):
        if not correo.value or not contrasena.value:
            mensaje.value = "⚠️ Por favor completa todos los campos."
            mensaje.color = ft.Colors.RED
            mensaje.visible = True
            page.update()
        else:
            mensaje.value = "✅ Registro exitoso."
            mensaje.color = ft.Colors.GREEN
            mensaje.visible = True
            page.update()

    correo = ft.TextField(label="Correo electrónico", width=300)
    contrasena = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    mensaje = ft.Text("", size=14, visible=False, text_align="center")

    return ft.View(
        "/registro_dentista",
        bgcolor="#1e293b",  # fondo oscuro
        controls=[
            ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Text("CREAR CUENTA DENTISTA", size=24, weight="bold", color=ft.Colors.WHITE),
                    correo,
                    contrasena,
                    mensaje,
                    ft.ElevatedButton("Registrarme", icon=ft.Icons.PERSON_ADD, bgcolor="#3b82f6", on_click=registrar),
                    ft.TextButton("← Volver al login", on_click=lambda e: page.go("/"))
                ]
            )
        ]
    )
