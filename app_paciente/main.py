import flet as ft
from views.home import HomeView 
from views.calendar import CalendarView

def main(page: ft.Page):

    # Forzamos el tema claro
    page.theme_mode = ft.ThemeMode.LIGHT

    # (Opcional) Personalizamos el tema
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="#1565C0",   # Azul dental
            background="#FFFFFF",
            surface="#FFFFFF",
            on_surface="#000000"
        )
    )

    def route_change(e):
        page.views.clear()
        if page.route == "/":
            page.views.append(HomeView(page))
        elif page.route == "/calendar":
            page.views.append(CalendarView(page))
        elif page.route == "/form":
            pass
        elif page.route == "/comfirm":
            pass
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main, view=ft.WEB_BROWSER, port=8080, assets_dir="assets")