import flet as ft
from controllers.reservas import get_all_reservas, actualizar_estado_reserva

def admin_panel_view(page: ft.Page):
    page.appbar = ft.AppBar(
        title=ft.Text("Panel de Administración"),
        actions=[
            ft.IconButton(icon=ft.icons.LOGOUT, tooltip="Cerrar sesión", on_click=lambda e: page.go("/"))
        ]
    )

    # Lista de reservas
    reservas_listview = ft.ListView(expand=True, spacing=10, padding=10)

    def cargar_reservas():
        reservas = get_all_reservas()
        reservas_listview.controls.clear()

        for r in reservas:
            estado_color = {
                "pendiente": ft.colors.ORANGE_300,
                "aprobada": ft.colors.GREEN_400,
                "cancelada": ft.colors.RED_300
            }[r["estado"]]

            reserva_card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(f"Paciente: {r['nombre']} ({r['email']})"),
                        ft.Text(f"Servicio: {r['servicio']}"),
                        ft.Text(f"Fecha: {r['fecha']} - Hora: {r['hora']}"),
                        ft.Text(f"Estado: {r['estado']}", color=estado_color),
                        ft.Row([
                            ft.ElevatedButton("Aprobar", on_click=lambda e, id=r["id"]: cambiar_estado(id, "aprobada")),
                            ft.ElevatedButton("Cancelar", on_click=lambda e, id=r["id"]: cambiar_estado(id, "cancelada")),
                        ], spacing=10)
                    ])
                )
            )
            reservas_listview.controls.append(reserva_card)

        page.update()

    def cambiar_estado(reserva_id, nuevo_estado):
        actualizar_estado_reserva(reserva_id, nuevo_estado)
        cargar_reservas()

    cargar_reservas()

    page.add(
        ft.Column([
            ft.Text("Reservas registradas", size=22, weight=ft.FontWeight.BOLD),
            reservas_listview
        ], expand=True, scroll=ft.ScrollMode.AUTO)
    )
