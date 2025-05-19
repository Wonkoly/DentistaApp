import os, sys

# Añadir la ruta base del proyecto ANTES que cualquier import local
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, ROOT_DIR)
print("🧭 Ruta base añadida:", ROOT_DIR)

from fastapi import FastAPI
from backend.routes import auth, citas  # si tienes más routers

app = FastAPI()

# Incluir rutas
app.include_router(auth.router, prefix="/api")
app.include_router(citas.router, prefix="/api")  # si lo tienes

import flet as ft

from apps.dentista.views.login_dentista import LoginDentistaView
from apps.dentista.views.registro_dentista import RegistroDentistaView
from apps.dentista.views.recuperar_dentista import RecuperarDentistaView
from apps.dentista.views.home_dentista import HomeDentistaView
from apps.dentista.views.servicios_dentista import ServiciosDentistaView
from apps.dentista.views.configuracion_dentista import ConfiguracionDentistaView
from apps.dentista.views.confirmar_codigo import ConfirmarCodigoView
from backend.routes import auth
app.include_router(auth.router, prefix="/api")


def main(page: ft.Page):
    page.title = "Clinica Choyo - Dentista"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 420
    page.window_height = 850
    page.scroll = ft.ScrollMode.HIDDEN
    page.update()

    def route_change(e):
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
                page.views.append(HomeDentistaView(page))
            case "/servicios_dentista":
                page.views.append(ServiciosDentistaView(page))
            case "/configuracion_dentista":
                page.views.append(ConfiguracionDentistaView(page))

        page.update()

    page.on_route_change = route_change
    page.go(page.route)

if __name__ == "__main__":

    ft.app(target=main, view=ft.WEB_BROWSER, port=8081, assets_dir="assets")
