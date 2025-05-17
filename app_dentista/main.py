import flet as ft
from views.login_dentista import LoginDentistaView

def main(page: ft.Page):
    page.title = "Clínica Choyo - Dentista"

    def route_change(route):
        page.views.clear()
        page.views.append(LoginDentistaView(page))
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main, view=ft.WEB_BROWSER, port=8081, assets_dir="assets")
