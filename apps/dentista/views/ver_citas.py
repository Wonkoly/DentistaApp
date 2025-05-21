import flet as ft
import httpx
from common import colors
from components.navbar import NavbarDentista



async def obtener_citas():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/api/citas_completas")
        if response.status_code == 200:
            return response.json()
        return []

def VerCitasView(page: ft.Page):
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID Paciente")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Hora")),
            ft.DataColumn(ft.Text("Servicio")),
            ft.DataColumn(ft.Text("Notas")),
            ft.DataColumn(ft.Text("Pago en línea")),
        ],
        rows=[]
    )

    async def cargar_tabla():
        citas = await obtener_citas()
        tabla.rows.clear()

        for cita in citas:
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(cita["paciente_id"]))),
                        ft.DataCell(ft.Text(cita["nombre"])),
                        ft.DataCell(ft.Text(cita["fecha"])),
                        ft.DataCell(ft.Text(cita["hora"])),
                        ft.DataCell(ft.Text(cita["servicio"])),
                        ft.DataCell(ft.Text(cita["notas"])),
                        ft.DataCell(ft.Text(cita["pago_en_linea"])),
                    ]
                )
            )
        page.update()

    page.on_view_push = lambda e: page.run_async(cargar_tabla)

    return ft.View(
        "/ver_citas",
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Text("📋 Historial de Citas", size=24, weight=ft.FontWeight.BOLD, color=colors.SECONDARY),
                    tabla
                ], spacing=20),
                padding=20
            ),
            NavbarDentista(page=page, ruta_actual="ver_citas")
        ],
        scroll=ft.ScrollMode.AUTO
    )
