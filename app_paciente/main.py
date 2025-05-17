import flet as ft
import os
import sys



# Añadir el path absoluto de la carpeta actual
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv()

from views.home import HomeView
from views.calendar_view import CalendarView
from views.form import FormView
from views.confirm import ConfirmView
from views.opiniones import OpinionesView
from views.tratamientos import TratamientosView
from views.clinica import ClinicaView
from views.pago import PagoView


def main(page: ft.Page):
    print("✅ APP INICIADA")

    page.title = "App Dentista"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.TEAL,
            background=ft.Colors.WHITE,
            surface=ft.Colors.WHITE,
            on_surface=ft.Colors.BLACK
        )
    )

    def route_change(e):
        print(f"🔀 Ruta actual: {page.route}")
        page.views.clear()
        match page.route:
            case "/":
                page.views.append(HomeView(page))
            case "/calendar":
                page.views.append(CalendarView(page))
            case "/form":
                page.views.append(FormView(page))
            case "/confirm":
                page.views.append(ConfirmView(page))
            case "/opiniones":
                page.views.append(OpinionesView(page))
            case "/tratamientos":
                page.views.append(TratamientosView(page))
            case "/clinica":
                page.views.append(ClinicaView(page))
            case "/pago":
                page.views.append(PagoView(page))

        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main, view=ft.WEB_BROWSER, port=8080, assets_dir="assets")