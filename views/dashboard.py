import flet as ft
from controllers.reservas import get_reservas_por_dentista

def dashboard_view(page: ft.Page, usuario):
    # Create reusable snackbars
    dev_snack = ft.SnackBar(ft.Text("Función en desarrollo"))
    nav_snack = ft.SnackBar(ft.Text("Sección aún no implementada"))
    error_snack = ft.SnackBar(ft.Text("Error al cargar citas"))

    def confirm_logout(e):
        confirm_dialog = ft.AlertDialog(
            title=ft.Text("Confirmar"),
            content=ft.Text("¿Está seguro que desea cerrar sesión?"),
            actions=[
                ft.TextButton("Sí", on_click=lambda e: page.go("/")),
                ft.TextButton("No", on_click=lambda e: confirm_dialog.open == False)
            ]
        )
        page.dialog = confirm_dialog
        confirm_dialog.open = True
        page.update()

    page.appbar = ft.AppBar(
        title=ft.Text(f"Bienvenido, Dr. {usuario['email']}"),
        actions=[
            ft.IconButton(
                icon=ft.icons.SETTINGS,
                tooltip="Configuración",
                on_click=lambda e: dev_snack.open
            ),
            ft.IconButton(
                icon=ft.icons.LOGOUT,
                tooltip="Cerrar sesión",
                on_click=confirm_logout
            )
        ]
    )

    calendario = ft.ListView(expand=True, spacing=12, padding=10, auto_scroll=True)

    def cargar_citas():
        try:
            citas = get_reservas_por_dentista(usuario['email'])
            calendario.controls.clear()

            if not citas:
                calendario.controls.append(ft.Text("No hay citas registradas aún.", italic=True))
            else:
                for c in citas:
                    calendario.controls.append(
                        ft.Card(
                            content=ft.Container(
                                padding=10,
                                content=ft.Column([
                                    ft.Text(f"Paciente: {c['nombre']}", size=18, weight=ft.FontWeight.BOLD),
                                    ft.Text(f"Servicio: {c['servicio']}"),
                                    ft.Text(f"Fecha: {c['fecha']}"),
                                    ft.Text(f"Hora: {c['hora']}"),
                                    ft.Text(f"Correo: {c['email']}"),
                                    ft.Text(f"Estado: {c['estado']}")
                                ])
                            )
                        )
                    )
        except Exception as e:
            print(f"Error loading appointments: {e}")
            error_snack.open = True
        finally:
            page.update()

    cargar_citas()

    menu_lateral = ft.NavigationRail(
        selected_index=0,
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.CALENDAR_MONTH, label="Calendario"),
            ft.NavigationRailDestination(icon=ft.icons.MEDICAL_SERVICES, label="Servicios"),
            ft.NavigationRailDestination(icon=ft.icons.PEOPLE, label="Pacientes"),
            ft.NavigationRailDestination(icon=ft.icons.SETTINGS, label="Configuración"),
        ],
        on_change=lambda e: nav_snack.open
    )

    page.add(
        ft.Row([
            menu_lateral,
            ft.VerticalDivider(width=1),
            ft.Column([
                ft.Text("Citas programadas", size=22, weight=ft.FontWeight.BOLD),
                calendario
            ], expand=True)
        ], expand=True)
    )
