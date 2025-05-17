
import flet as ft
import re

def RecuperarContrasenaView(page: ft.Page):
    email = ft.TextField(label="Correo electrónico", prefix_icon=ft.icons.EMAIL)
    confirmar_email = ft.TextField(label="Confirma tu correo", prefix_icon=ft.icons.EMAIL)
    telefono = ft.TextField(label="Número de teléfono", prefix_icon=ft.icons.PHONE)

    dialogo = ft.AlertDialog(title=ft.Text("Recuperación"), content=ft.Text(""), actions=[
        ft.TextButton("Cerrar", on_click=lambda e: page.dialog.close())
    ])

    def mostrar_mensaje(mensaje, color):
        dialogo.content = ft.Text(mensaje, color=color)
        dialogo.open = True
        page.dialog = dialogo
        page.update()

    def validar_email_telefono(e):
        errores = False

        # Limpiar errores anteriores
        for campo in [email, confirmar_email, telefono]:
            campo.error_text = None

        # Campos vacíos
        if not email.value.strip():
            email.error_text = "Campo obligatorio"
            errores = True
        if not confirmar_email.value.strip():
            confirmar_email.error_text = "Campo obligatorio"
            errores = True
        if not telefono.value.strip():
            telefono.error_text = "Campo obligatorio"
            errores = True

        # Correo electrónico debe coincidir
        if email.value.strip() and confirmar_email.value.strip() and email.value.strip() != confirmar_email.value.strip():
            confirmar_email.error_text = "El correo electrónico no coincide"
            errores = True

        # Validación de teléfono: solo números y 10 dígitos exactos
        if telefono.value.strip() and not re.fullmatch(r"\d{10}", telefono.value.strip()):
            telefono.error_text = "Solo se aceptan 10 dígitos numéricos sin letras ni símbolos"
            errores = True

        page.update()

        if errores:
            return

        mostrar_mensaje("Datos confirmados. Te enviamos un código (simulado)", ft.colors.GREEN)

    return ft.View(
        route="/recuperar_contrasena",
        controls=[
            ft.Container(
                expand=True,
                bgcolor="#1e293b",
                alignment=ft.alignment.center,
                content=ft.Container(
                    width=400,
                    padding=30,
                    border_radius=15,
                    bgcolor=ft.colors.WHITE,
                    content=ft.Column(
                        spacing=20,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("¿Olvidaste tu contraseña?", size=22, weight="bold", text_align="center"),
                            email,
                            confirmar_email,
                            telefono,
                            ft.ElevatedButton(
                                "Confirmar",
                                icon=ft.icons.CHECK,
                                bgcolor="#10b981",
                                color="white",
                                on_click=validar_email_telefono
                            ),
                            ft.TextButton("Volver al login", on_click=lambda e: page.go("/login_dentista"))
                        ]
                    )
                )
            )
        ]
    )
