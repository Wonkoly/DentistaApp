import flet as ft
from views.home import HomeView 

def main(page: ft.Page):

    def route_change(e):
        page.views.clear()
        if page.route == "/":
            page.views.append(HomeView(page))
        elif page.route == "":
            pass
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)
