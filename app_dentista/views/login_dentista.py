import flet as ft
import json
import os

def LoginDentistaView(page: ft.Page):
    email_input = ft.TextField(label="Correo electrónico", prefix_icon=ft.Icons.EMAIL, width=350)
    password_input = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, prefix_icon=ft.Icons.LOCK, width=350)

    dialog = ft.AlertDialog(title=ft.Text("Aviso"), content=ft.Text(""), actions=[
        ft.TextButton("Cerrar", on_click=lambda e: page.dialog.close())
    ])

    def mostrar_mensaje(texto, color):
        dialog.content = ft.Text(texto, color=color)
        dialog.open = True
        page.dialog = dialog
        page.update()

    def verificar_credenciales(e):
        print("Botón presionado")  # Confirmación en terminal

        errores = False

        # Validación visual de campos
        if not email_input.value.strip():
            email_input.error_text = "Campo obligatorio"
            errores = True
        else:
            email_input.error_text = None

        if not password_input.value.strip():
            password_input.error_text = "Campo obligatorio"
            errores = True
        else:
            password_input.error_text = None

        page.update()

        if errores:
            return

        ruta = os.path.join("database", "usuarios.json")
        if not os.path.exists(ruta):
            mostrar_mensaje("No hay usuarios registrados aún", ft.Colors.RED)
            return

        try:
            with open(ruta, "r") as f:
                data = json.load(f)

            for user in data.get("usuarios", []):
                if user["email"].strip() == email_input.value.strip() and user["password"] == password_input.value:
                    print("Login exitoso")
                    mostrar_mensaje("Inicio de sesión exitoso", ft.Colors.GREEN)
                    page.client_storage.set("usuario_logueado", user["email"])
                    page.go("/calendario_dentista")
                    page.update()
                    return

            password_input.value = ""
            mostrar_mensaje("Usuario o contraseña incorrectos", ft.Colors.RED)

        except Exception as ex:
            mostrar_mensaje(f"Error: {ex}", ft.Colors.RED)

    return ft.View(
        route="/login_dentista",
        controls=[
            ft.Container(
                expand=True,
                bgcolor="#9ca3af",
                alignment=ft.alignment.center,
                content=ft.Column(
                    horizontal_alignment="center",
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=30,
                    controls=[
                        ft.Text("CLÍNICA CHOYO", size=26, weight="bold", color="white"),
                        ft.Text("INICIAR SESIÓN COMO DENTISTA", size=18, color="white"),
                        email_input,
                        password_input,
                        ft.ElevatedButton(
                            "Iniciar sesión",
                            icon=ft.Icons.LOGIN,
                            bgcolor="#3b82f6",
                            color="white",
                            width=200,
                            height=45,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=verificar_credenciales
                        ),
                        ft.Row([
                            ft.TextButton("¿Olvidaste tu contraseña?", on_click=lambda e: page.go("/recuperar_contrasena")),
                            ft.Text(" | ", color="white"),
                            ft.TextButton("Crear cuenta", on_click=lambda e: page.go("/registro_dentista"))
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Text("© 2025 Clínica Choyo - Puerto Vallarta", size=12, color="white")
                    ]
                )
            )
        ]
    )
