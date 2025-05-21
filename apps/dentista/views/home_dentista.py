import flet as ft
import httpx
import asyncio
from common import colors
from components.navbar import NavbarDentista


async def HomeDentistaView(page: ft.Page):
    usuario_id = page.session.get("usuario_id")
    usuario_nombre = page.session.get("usuario_nombre") or "Dentista"
    citas = []

    # 🔄 Cargar citas del backend
    async def cargar_citas():
        nonlocal citas
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"http://localhost:8000/api/citas_completas?usuario_id={usuario_id}"
                )
                if response.status_code == 200:
                    citas = response.json()
        except Exception as e:
            print("❌ Error al obtener citas:", e)

    await cargar_citas()

    # ✅ Finalizar cita y actualizar lista
    async def finalizar_cita(cita):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"http://localhost:8000/api/citas/{cita['id']}/finalizar"
                )
                if response.status_code == 200:
                    page.snack_bar = ft.SnackBar(
                        ft.Text("✅ Cita finalizada"), bgcolor=colors.SUCCESS
                    )
                    page.snack_bar.open = True
                    await cargar_citas()
                    page.go("/home_dentista")  # 🔁 recarga
                else:
                    page.snack_bar = ft.SnackBar(
                        ft.Text("❌ No se pudo finalizar la cita"), bgcolor=colors.ERROR
                    )
                    page.snack_bar.open = True
        except Exception as e:
            print("❌ Error al finalizar cita:", e)
            page.snack_bar = ft.SnackBar(
                ft.Text("❌ Error de red"), bgcolor=colors.ERROR
            )
            page.snack_bar.open = True
        page.update()

    # 📝 Placeholder para editar citas
    def editar_cita(cita):
        page.dialog = ft.AlertDialog(
            title=ft.Text("Editar Cita (próximamente)"),
            content=ft.Text(f"Cita de {cita['nombre']}"),
            actions=[ft.TextButton("Cerrar", on_click=lambda _: cerrar_dialog())]
        )
        page.dialog.open = True
        page.update()

    def cerrar_dialog():
        if page.dialog:
            page.dialog.open = False
            page.update()

    # 🖼️ Saludo inicial
    saludo = ft.Text(
        f"👋 Bienvenido, {usuario_nombre}",
        size=20,
        weight=ft.FontWeight.BOLD,
        color=colors.PRIMARY_DARK
    )

    # 📅 Contenedor de citas
    if citas:
        calendario_real = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"🕒 {cita['fecha']} {cita['hora']}", weight=ft.FontWeight.BOLD),
                        ft.Text(f"👤 {cita['nombre']}"),
                        ft.Text(f"🦷 {cita['servicio']}"),
                        ft.Text(f"📝 {cita['notas']}"),
                        ft.Text(f"💳 Pagado: {cita['pago_en_linea']}"),
                        ft.Row([
                            ft.ElevatedButton(
                                "✏️ Editar",
                                on_click=lambda e, c=cita: editar_cita(c)
                            ),
                            ft.ElevatedButton(
                                "✅ Finalizar",
                                on_click=lambda e, c=cita: asyncio.get_event_loop().create_task(finalizar_cita(c)),
                                bgcolor=colors.SUCCESS,
                                color="white"
                            )
                        ], spacing=10)
                    ], spacing=6),
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
                content=ft.Column(
                    controls=[
                        saludo,
                        ft.Text(
                            "Calendario de Citas",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=colors.SECONDARY
                        ),
                        calendario_real,
                        info_consulta
                    ],
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=30
            ),
            NavbarDentista(page=page, ruta_actual="/home_dentista")
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
