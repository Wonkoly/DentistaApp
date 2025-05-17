import flet as ft
import json
import os

def LoginView(page: ft.Page):
    email_input = ft.TextField(label="Correo electrónico", width=300)
    password_input = ft.TextField(label="Contraseña", password=True, width=300)
    message = ft.Text("", color="red", size=12)

    def verificar(e):
        ruta = os.path.join("database", "usuarios.json")
        try:
            with open(ruta, "r") as f:
                data = json.load(f)

            for user in data["usuarios"]:
                if user["email"] == email_input.value and user["password"] == password_input.value:
                    message.value = f"Bienvenido, {user['nombre']}!"
                    message.color = "green"
                    page.update()
                    return
            message.value = "Usuario o contraseña incorrectos"
            message.color = "red"
        except Exception as ex:
            message.value = f"Error: {ex}"
            message.color = "red"
        page.update()

    page.add(
        ft.Column([
            ft.Text("Login simple", size=24, weight="bold"),
            email_input,
            password_input,
            ft.ElevatedButton("Iniciar sesión", on_click=verificar),
            message
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )