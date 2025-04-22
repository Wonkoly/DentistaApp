import flet as ft
from views.home import home_view
from views.calendar import calendar_view
from views.form import form_view
from views.confirm import confirm_view

def main(page: ft.Page):
    page.title = "Reserva de Citas - Clínica Dental"
    page.theme_mode = ft.ThemeMode.LIGHT

    page.routes = {
        "/": home_view,
        "/calendar": calendar_view,
        "/form": form_view,
        "/confirm": confirm_view,
    }

    page.go("/")

if __name__ == "__main__":
    ft.app(target=main)
