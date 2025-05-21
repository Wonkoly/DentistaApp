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

    def ver_citas_paciente(e):
        paciente = e.control.data or {}
        citas = paciente.get("citas") or []

        cita_items = []
        for cita in citas:
            if not isinstance(cita, dict):
                continue
            fecha = str(cita.get("fecha") or "¿Sin fecha?")
            hora = str(cita.get("hora") or "¿Sin hora?")
            servicio = str(cita.get("servicio") or "¿Sin servicio?")
            pagado = "Sí" if cita.get("pago_en_linea") else "No"
            detalle = f"{fecha} - {hora} - {servicio} - Pagado en línea: {pagado}"
            cita_items.append(ft.Text(f"• {detalle}"))

        if not cita_items:
            cita_items = [ft.Text("• Sin citas registradas")]

        def cerrar(e=None):
            if page.dialog:
                page.dialog.open = False
                page.update()

        dialogo = ft.AlertDialog(
            title=ft.Text(f"Citas de {paciente.get('nombre', 'Paciente')}"),
            content=ft.Column(
                controls=[
                    ft.Text(f"Correo: {paciente.get('correo', 'Desconocido')}"),
                    ft.Text(f"Teléfono: {paciente.get('telefono', 'Desconocido')}"),
                    ft.Text("Citas:"),
                    ft.Column(controls=cita_items or [ft.Text("• Sin información disponible")])
                ],
                tight=True
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=cerrar)
            ],
            actions_alignment="end"
        )

        page.dialog = dialogo
        page.dialog.open = True
        page.update()

    def actualizar_tabla(pacientes):
        tabla.rows = []

        for p in pacientes:
            nombre = p.get("nombre", "Desconocido")
            correo = p.get("correo", "Sin correo")
            telefono = p.get("telefono", "Sin teléfono")

            if not all([nombre, correo, telefono]):
                continue

            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(nombre))),
                        ft.DataCell(ft.Text(str(correo))),
                        ft.DataCell(ft.Text(str(telefono))),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.VISIBILITY,
                                data=p,
                                on_click=ver_citas_paciente
                            )
                        )
                    ]
                )
            )

    def filtrar_pacientes(valor):
        valor = valor.lower()
        pacientes_filtrados = [
            p for p in pacientes_completos
            if valor in p.get("nombre", "").lower() or valor in p.get("correo", "").lower()
        ]
        actualizar_tabla(pacientes_filtrados)

    busqueda_input = ft.TextField(
        label="Buscar por nombre o correo",
        width=400,
        on_change=lambda e: filtrar_pacientes(e.control.value)
    )

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

    controles_vista = [
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
        )
    ]

    navbar = NavbarDentista(page, ruta_actual=page.route)
    if navbar:
        controles_vista.append(navbar)

    return ft.View(
        "/pacientes_dentista",
        controls=controles_vista,
        vertical_alignment=ft.MainAxisAlignment.START
    )
