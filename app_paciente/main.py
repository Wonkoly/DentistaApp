import flet as ft
from views.home import HomeView 

def main(page: ft.Page):

    def route_change(e):
        page.views.clear()
        if page.route == "/":
            page.views.append(HomeView(page))
        elif page.route == "/calendar":
            pass
        elif page.route == "/form":
            pass
        elif page.route == "/comfirm":
            pass
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main, view=ft.WEB_BROWSER, port=8080, assets_dir="assets")