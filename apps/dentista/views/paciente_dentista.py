import flet as ft
import httpx
from common import colors
from components.navbar import NavbarDentista

API_URL = "http://127.0.0.1:8000/api/pacientes"

async def PacienteDentistaView(page: ft.Page):
    pacientes_completos = []
    tabla = ft.DataTable(
        border=ft.border.all(1, colors.PRIMARY),
        columns=[
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Correo")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Acción"))
        ],
        rows=[]
    )

    busqueda_input = ft.TextField(
        label="Buscar por nombre o correo",
        width=400,
        on_change=lambda e: filtrar_pacientes(e.control.value)
    )

    def ver_citas_paciente(e):
        paciente = e.control.data
        page.dialog = ft.AlertDialog(
            title=ft.Text(f"Citas de {paciente['nombre']}"),
            content=ft.Column(
                controls=[
                    ft.Text(f"Correo: {paciente['correo']}"),
                    ft.Text(f"Teléfono: {paciente['telefono']}"),
                    ft.Text("Citas:"),
                    ft.Column(
                        controls=[
                            ft.Text(f"• {cita}") for cita in paciente.get("citas", ["Sin citas registradas"])
                        ]
                    )
                ],
                tight=True
            ),
            actions=[ft.TextButton("Cerrar", on_click=lambda _: cerrar_dialogo())],
            actions_alignment="end"
        )
        page.dialog.open = True
        page.update()

    def cerrar_dialogo():
        page.dialog.open = False
        page.update()

    def filtrar_pacientes(valor):
        valor = valor.lower()
        pacientes_filtrados = [
            p for p in pacientes_completos
            if valor in p["nombre"].lower() or valor in p["correo"].lower()
        ]
        actualizar_tabla(pacientes_filtrados)

    def actualizar_tabla(pacientes):
        tabla.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(p["nombre"])),
                    ft.DataCell(ft.Text(p["correo"])),
                    ft.DataCell(ft.Text(p["telefono"])),
                    ft.DataCell(ft.IconButton(icon=ft.Icons.VISIBILITY, data=p, on_click=ver_citas_paciente))
                ]
            ) for p in pacientes
        ]
        page.update()

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(API_URL)
            response.raise_for_status()
            pacientes_completos = response.json()
            actualizar_tabla(pacientes_completos)
    except Exception as e:
        print("❌ Error cargando pacientes:", e)
        import traceback
        traceback.print_exc()
        tabla.rows = [ft.DataRow(cells=[ft.DataCell(ft.Text("Error al obtener datos"))])]

    page.views.clear()
    page.views.append(
        ft.View(
            "/pacientes_dentista",
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("👥 Lista de Pacientes", size=24, weight=ft.FontWeight.BOLD, color=colors.PRIMARY_DARK),
                            busqueda_input,
                            tabla
                        ],
                        spacing=20
                    ),
                    padding=20,
                    expand=True
                ),
                NavbarDentista(page, ruta_actual=page.route),
            ],
            vertical_alignment=ft.MainAxisAlignment.START
        )
    )
    page.update()
