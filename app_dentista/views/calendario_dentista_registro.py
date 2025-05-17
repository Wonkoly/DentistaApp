import flet as ft

def RegistroView(page: ft.Page):
    mensaje = ft.Text("", size=12, color=ft.Colors.RED_300, visible=False, text_align="center")

    correo = ft.TextField(label="Correo electrónico", width=300)
    contrasena = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    confirmar_contrasena = ft.TextField(label="Confirmar contraseña", password=True, can_reveal_password=True, width=300)

    def registrar(e):
        if not correo.value or not contrasena.value or not confirmar_contrasena.value:
            mensaje.value = "⚠️ Todos los campos son obligatorios."
            mensaje.color = ft.Colors.RED_300
            mensaje.visible = True
            page.update()
            return
        if contrasena.value != confirmar_contrasena.value:
            mensaje.value = "⚠️ Las contraseñas no coinciden."
            mensaje.color = ft.Colors.RED_300
            mensaje.visible = True
            page.update()
            return

        mensaje.value = "✅ Cuenta registrada correctamente."
        mensaje.color = ft.Colors.GREEN_300
        mensaje.visible = True
        page.update()

    return ft.View(
        route="/registro",
        controls=[
            ft.Container(
                bgcolor=ft.Colors.SURFACE,
                alignment=ft.alignment.center,
                expand=True,
                content=ft.Column(
                    horizontal_alignment="center",
                    alignment="center",
                    spacing=20,
                    controls=[
                        ft.Text("REGISTRO DE DENTISTA", size=26, weight="bold", color=ft.Colors.WHITE),
                        correo,
                        contrasena,
                        confirmar_contrasena,
                        mensaje,
                        ft.ElevatedButton("Registrar cuenta", bgcolor=ft.Colors.BLUE_500, color="white", on_click=registrar),
                        ft.TextButton("← Volver al inicio", on_click=lambda e: page.go("/"))
                    ]
                )
            )
        ]
    )