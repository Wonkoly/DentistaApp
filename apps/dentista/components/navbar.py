import flet as ft
from common import colors  # paleta personalizada

def NavbarDentista(page: ft.Page, ruta_actual: str):
    try:
        def navegar(ruta):
            if page and page.go:
                page.go(ruta)

        botones = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.IconButton(
                    icon=ft.Icons.CALENDAR_MONTH,
                    tooltip="Calendario",
                    on_click=lambda e: navegar("/home_dentista")
                ),
                ft.IconButton(
                    icon=ft.Icons.MEDICAL_SERVICES,
                    tooltip="Servicios",
                    on_click=lambda e: navegar("/servicios_dentista")
                ),
                ft.IconButton(
                    icon=ft.Icons.PEOPLE,
                    tooltip="Pacientes",
                    on_click=lambda e: navegar("/pacientes_dentista")
                ),
                ft.IconButton(
                    icon=ft.Icons.LIST_ALT,
                    tooltip="Ver citas con notas",
                    on_click=lambda e: navegar("/ver_citas")
                ),
                ft.IconButton(
                    icon=ft.Icons.HISTORY,  # ✅ NUEVO BOTÓN
                    tooltip="Historial de citas",
                    on_click=lambda e: navegar("/historial_citas")
                ),
                ft.IconButton(
                    icon=ft.Icons.SETTINGS,
                    tooltip="Configuración",
                    on_click=lambda e: navegar("/configuracion_dentista")
                )
            ]
        )

        return ft.Container(
            content=botones,
            bgcolor=colors.PRIMARY_LIGHT,
            padding=10
        )
    except Exception as err:
        print("❌ Error en NavbarDentista:", err)
        return ft.Container(
            content=ft.Text("Error en la navegación"),
            bgcolor=ft.colors.RED_100,
            padding=10
        )

