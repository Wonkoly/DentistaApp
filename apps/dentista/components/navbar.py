import flet as ft
from common import colors  # 🎯 Tu paleta personalizada

def NavbarDentista(page: ft.Page, ruta_actual: str):
    def navegar(ruta: str):
        if page and page.go and callable(page.go):
            try:
                page.go(ruta)
            except Exception as e:
                print(f"❌ Error al navegar a {ruta}: {e}")

    botones = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        controls=[
            ft.IconButton(
                icon=ft.Icons.CALENDAR_MONTH,
                tooltip="Calendario",
                icon_color=colors.SECONDARY if ruta_actual == "/home_dentista" else None,
                on_click=lambda e: navegar("/home_dentista"),
            ),
            ft.IconButton(
                icon=ft.Icons.MEDICAL_SERVICES,
                tooltip="Servicios",
                icon_color=colors.SECONDARY if ruta_actual == "/servicios_dentista" else None,
                on_click=lambda e: navegar("/servicios_dentista"),
            ),
            ft.IconButton(
                icon=ft.Icons.PEOPLE,
                tooltip="Pacientes",
                icon_color=colors.SECONDARY if ruta_actual == "/pacientes_dentista" else None,
                on_click=lambda e: navegar("/pacientes_dentista"),
            ),
            ft.IconButton(
                icon=ft.Icons.LIST_ALT,
                tooltip="Ver citas con notas",
                icon_color=colors.SECONDARY if ruta_actual == "/ver_citas" else None,
                on_click=lambda e: navegar("/ver_citas"),
            ),
            ft.IconButton(
                icon=ft.Icons.SETTINGS,
                tooltip="Configuración",
                icon_color=colors.SECONDARY if ruta_actual == "/configuracion_dentista" else None,
                on_click=lambda e: navegar("/configuracion_dentista"),
            ),
        ]
    )

    return ft.Container(
        content=botones,
        bgcolor=colors.PRIMARY_LIGHT,
        padding=10
    )
