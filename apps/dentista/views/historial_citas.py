import flet as ft
import httpx
from common import colors
from components.navbar import NavbarDentista

async def HistorialCitasView(page: ft.Page):
    usuario_id = page.session.get("usuario_id")
    citas = []

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://localhost:8000/api/citas/finalizadas?usuario_id={usuario_id}")
            if response.status_code == 200:
                citas = response.json()
    except Exception as e:
        print("❌ Error al obtener historial de citas:", e)

    encabezado = ft.Text(
        "📜 Historial de Citas Finalizadas",
        size=24,
        weight=ft.FontWeight.BOLD,
        color=colors.SECONDARY
    )

    if citas:
        lista = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"🕒 {cita['fecha']} {cita['hora']}", weight=ft.FontWeight.BOLD),
                        ft.Text(f"👤 {cita['nombre']}"),
                        ft.Text(f"🦷 {cita['servicio']}"),
                        ft.Text(f"📝 {cita['notas']}"),
                        ft.Text(f"💳 Pagado: {cita['pago_en_linea']}")
                    ], spacing=5),
                    padding=10,
                    bgcolor=colors.PRIMARY_LIGHT,
                    border_radius=10,
                    width=360
                ) for cita in citas
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO
        )
    else:
        lista = ft.Text("No hay citas finalizadas.", size=16, color=colors.SECONDARY)

    return ft.View(
        "/historial_citas",
        controls=[
            ft.Container(
                content=ft.Column([
                    encabezado,
                    lista
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=30
            ),
            NavbarDentista(page=page, ruta_actual="/historial_citas")
        ],
        vertical_alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
