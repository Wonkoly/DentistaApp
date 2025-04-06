import flet as ft
from views.login import login_view

def main(page: ft.Page):
    page.title = "Consultorio Dental"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    login_view(page)  # Carga la vista principal (login)

ft.app(target=main)