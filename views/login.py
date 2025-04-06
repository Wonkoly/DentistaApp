import flet as ft
from controllers.auth import login_user

def login_view(page: ft.Page):
    email = ft.TextField(label="Correo")
    password = ft.TextField(label="Contraseña", password=True)

    def handle_login(e):
        user = login_user(email.value, password.value)
        if user:
            if user["role"] == "admin":
                from views.admin_panel import admin_panel_view
                page.clean()
                admin_panel_view(page)
            else:
                from views.dashboard import dashboard_view
                page.clean()
                dashboard_view(page, user)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Usuario o contraseña inválidos"))
            page.snack_bar.open = True
            page.update()

    login_btn = ft.ElevatedButton(text="Iniciar sesión", on_click=handle_login)

    page.add(
        ft.Column([
            ft.Image(src="assets/images/logo_sutudeg.png", width=150),
            email, password, login_btn
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
