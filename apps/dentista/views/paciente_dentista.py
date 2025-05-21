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
        citas = paciente.get("citas")

        if not citas or not isinstance(citas, list) or len(citas) == 0:
            citas = [{"detalle": "Sin citas registradas"}]

        cita_items = []
        for cita in citas:
            if isinstance(cita, dict):
                fecha = cita.get("fecha", "¿Sin fecha?")
                hora = cita.get("hora", "¿Sin hora?")
                servicio = cita.get("servicio", "¿Sin servicio?")
                pagado = "Sí" if cita.get("pago_en_linea") else "No"
                detalle = f"{fecha} - {hora} - {servicio} - Pagado en línea: {pagado}"
            else:
                detalle = str(cita)

            cita_items.append(ft.Text(f"• {detalle}"))

        def cerrar_dialogo_accion(e=None):
            page.dialog.open = False
            page.update()

        def ver_historial_completo(e):
            print(f"🔎 Ver historial completo de {paciente['nombre']} (ID: {paciente['paciente_id']})")
            # Aquí puedes implementar navegación si tienes otra vista para historial completo
            page.snack_bar = ft.SnackBar(ft.Text("🔧 Función de historial aún no implementada"))
            page.snack_bar.open = True
            cerrar_dialogo_accion()

        def reenviar_confirmacion(e):
            print(f"✉️ Reenviando confirmación de citas a {paciente['correo']}")
            # Aquí podrías usar httpx para hacer el POST a /api/reenviar_correo
            page.snack_bar = ft.SnackBar(ft.Text("✅ Correo reenviado correctamente"))
            page.snack_bar.open = True
            cerrar_dialogo_accion()

        page.dialog = ft.AlertDialog(
            title=ft.Text(f"Citas de {paciente['nombre']}"),
            content=ft.Column(
                controls=[
                    ft.Text(f"Correo: {paciente['correo']}"),
                    ft.Text(f"Teléfono: {paciente['telefono']}"),
                    ft.Text("Citas registradas:"),
                    ft.Column(controls=cita_items, tight=True),
                ],
                tight=True
            ),
            actions=[
                ft.TextButton("Ver historial completo", on_click=ver_historial_completo),
                ft.TextButton("Reenviar confirmación", on_click=reenviar_confirmacion),
                ft.TextButton("Cerrar", on_click=cerrar_dialogo_accion)
            ],
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
