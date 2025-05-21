import flet as ft
import httpx
from common import colors
from components.navbar import NavbarDentista

async def HomeDentistaView(page: ft.Page):
    usuario_id = page.session.get("usuario_id")
    usuario_nombre = page.session.get("usuario_nombre") or "Dentista"
    citas = []

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://localhost:8000/api/citas_completas?usuario_id={usuario_id}")
            if response.status_code == 200:
                citas = response.json()
    except Exception as e:
        print("❌ Error al obtener citas:", e)

    saludo = ft.Text(
        f"👋 Bienvenido, {usuario_nombre}",
        size=20,
        weight=ft.FontWeight.BOLD,
        color=colors.PRIMARY_DARK
    )

    if citas:
        calendario_real = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"🕒 {cita['fecha']} {cita['hora']}", weight=ft.FontWeight.BOLD),
                        ft.Text(f"👤 {cita['nombre']}"),
                        ft.Text(f"🦷 {cita['servicio']}"),
                        ft.Text(f"📝 {cita['notas']}"),
                        ft.Text(f"💳 Pagado: {cita['pago_en_linea']}")
                    ],
                    spacing=4),
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
        calendario_real = ft.Text(
            "No hay citas registradas aún.",
            size=16,
            color=colors.SECONDARY
        )

    info_consulta = ft.Text(
        "Selecciona una cita para ver detalles como nombre del paciente, correo, horario y motivo.",
        size=14,
        color=colors.SECONDARY
    )

    return ft.View(
        route="/home_dentista",
        controls=[
            ft.Container(
                content=ft.Column([
                    saludo,
                    ft.Text("Calendario de Citas", size=24, weight=ft.FontWeight.BOLD, color=colors.SECONDARY),
                    calendario_real,
                    info_consulta
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=30
            ),
            NavbarDentista(page=page, ruta_actual="/home_dentista")
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
