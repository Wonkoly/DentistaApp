import flet as ft
import sys, os
import re
from datetime import datetime

# 🔧 Agrega dinámicamente el path raíz del proyecto (DentistaApp)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# 🔎 Debug visual
print("\U0001F9ED Ruta base añadida:", ROOT_DIR)
print("\U0001F5C2 sys.path:", sys.path)
print("\U0001F4C1 Contenido del ROOT_DIR:", os.listdir(ROOT_DIR))

# ✅ Verificación de existencia
assert os.path.exists(os.path.join(ROOT_DIR, "common")), "❌ common folder no existe en ROOT_DIR"
assert os.path.exists(os.path.join(ROOT_DIR, "common/colors.py")), "❌ colors.py no encontrado"

# 📦 Importaciones del proyecto
from common import colors
from views.home import HomeView
from views.calendar_view import CalendarView
from views.form import FormView
from views.confirm import ConfirmView
from views.opiniones import OpinionesView
from views.tratamientos import TratamientosView
from views.clinica import ClinicaView
from views.pago import PagoView, PagoExitosoView

def main(page: ft.Page):
    page.title = "Clínica Choyo - Dentista"
    page.window_width = 420
    page.window_height = 850
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=colors.PRIMARY)
    page.scroll = ft.ScrollMode.HIDDEN
    page.update()

    def route_change(e):
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
            case "/pago_exitoso":
                page.views.append(PagoExitosoView(page))

        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main, view=ft.WEB_BROWSER, port=8080, assets_dir="assets")
