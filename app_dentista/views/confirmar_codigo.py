# views/confirmar_codigo.py
import flet as ft

def ConfirmarCodigoView(page: ft.Page):
    codigo = ft.TextField(label="Código de verificación", prefix_icon=ft.icons.LOCK, width=350)
    nueva_password = ft.TextField(label="Nueva contraseña", password=True, can_reveal_password=True, prefix_icon=ft.icons.LOCK, width=350)
    confirmar_password = ft.TextField(label="Confirmar contraseña", password=True, can_reveal_password=True, prefix_icon=ft.icons.LOCK, width=350)

    dialogo = ft.AlertDialog(title=ft.Text("Cambio de contraseña"), content=ft.Text(""), actions=[
        ft.TextButton("Cerrar", on_click=lambda e: page.dialog.close())
    ])

    def mostrar_mensaje(mensaje, color):
        dialogo.content = ft.Text(mensaje, color=color)
        dialogo.open = True
        page.dialog = dialogo
        page.update()

    def cambiar_contrasena(e):
        if not codigo.value or not nueva_password.value or not confirmar_password.value:
            mostrar_mensaje("Todos los campos son obligatorios", ft.colors.RED)
            return
        if nueva_password.value != confirmar_password.value:
            mostrar_mensaje("Las contraseñas no coinciden", ft.colors.RED)
            return
        
        # Simular código correcto
        if codigo.value != "123456":
            mostrar_mensaje("Código incorrecto", ft.colors.RED)
            return

        # Aquí deberías actualizar el usuario en usuarios.json (omito por simplicidad)
        mostrar_mensaje("Contraseña actualizada exitosamente", ft.colors.GREEN)

    return ft.View(
        route="/confirmar_codigo",
        controls=[
            ft.Container(
                expand=True,
                bgcolor="#9ca3af",
                alignment=ft.alignment.center,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.Text("Confirmar código de verificación", size=24, weight="bold", color="white"),
                        codigo,
                        nueva_password,
                        confirmar_password,
                        ft.ElevatedButton(
                            "Confirmar",
                            icon=ft.icons.CHECK_CIRCLE,
                            bgcolor=ft.colors.BLUE,
                            color="white",
                            on_click=cambiar_contrasena
                        ),
                        ft.TextButton("Volver al login", on_click=lambda e: page.go("/login_dentista"))
                    ]
                )
            )
        ]
    )
