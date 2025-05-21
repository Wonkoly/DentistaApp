import os
import sys

# Modificar el sys.path para que detecte backend/
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, ROOT_DIR)
print("🧭 Ruta base añadida:", ROOT_DIR)

# 🟢 IMPORTS DE LIBRERÍAS EXTERNAS (instaladas con pip)
import flet as ft
from fastapi import FastAPI

# 🟢 IMPORTS DE MÓDULOS DEL PROYECTO (que dependen de sys.path)
from backend.routes import auth, citas

# API FastAPI
app = FastAPI()
app.include_router(auth.router, prefix="/api")
app.include_router(citas.router, prefix="/api")

# 🟢 IMPORT VISTAS FLET
from apps.dentista.views.login_dentista import LoginDentistaView
from apps.dentista.views.registro_dentista import RegistroDentistaView
from apps.dentista.views.recuperar_dentista import RecuperarDentistaView
from apps.dentista.views.home_dentista import HomeDentistaView
from apps.dentista.views.servicios_dentista import ServiciosDentistaView
from apps.dentista.views.configuracion_dentista import ConfiguracionDentistaView
from apps.dentista.views.confirmar_codigo import ConfirmarCodigoView
from apps.dentista.views.paciente_dentista import PacienteDentistaView
from apps.dentista.views.ver_citas import VerCitasView
from apps.dentista.views.historial_citas import HistorialCitasView  # ✅ NUEVA IMPORTACIÓN

def main(page: ft.Page):
    page.title = "Clinica Choyo - Dentista"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 420
    page.window_height = 850
    page.scroll = ft.ScrollMode.HIDDEN
    page.update()

    async def route_change(e):
        page.views.clear()
        match page.route:
            case "/":
                page.views.append(LoginDentistaView(page))
            case "/login_dentista":
                page.views.append(LoginDentistaView(page))
            case "/registro_dentista":
                page.views.append(RegistroDentistaView(page))
            case "/recuperar_dentista":
                page.views.append(RecuperarDentistaView(page))
            case "/confirmar_codigo":
                page.views.append(ConfirmarCodigoView(page))
            case "/home_dentista":
                view = await HomeDentistaView(page)
                page.views.append(view)
            case "/servicios_dentista":
                page.views.append(ServiciosDentistaView(page))
            case "/configuracion_dentista":
                page.views.append(ConfiguracionDentistaView(page))
            case "/pacientes_dentista":
                view = await PacienteDentistaView(page)
                page.views.append(view)
            case "/ver_citas":
                view = VerCitasView(page)
                print("✅ VerCitasView cargado:", type(view))
                page.views.append(view)
            case "/historial_citas":  # ✅ NUEVA RUTA
                view = await HistorialCitasView(page)
                page.views.append(view)

        page.update()

    page.on_route_change = route_change
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=8081, assets_dir="assets")
