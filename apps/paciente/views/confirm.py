import flet as ft
import sys, os
import httpx
import asyncio
from common import colors
from common.email import enviar_correo_confirmacion

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

async def registrar_en_base(cita, paciente):
    try:
        async with httpx.AsyncClient() as client:
         response = await client.post("http://localhost:8000/api/citas/", json={
        "nombre": paciente["nombre"],
        "apellido": paciente["apellido"],
        "correo": paciente["correo"],
        "telefono": paciente["telefono"],
        "notas": paciente.get("notas", ""),
        "servicio": int(cita["servicio_id"]),  # 👈 CORREGIDO
        "fecha": cita["fecha"],
        "hora": cita["hora"],
        "sucursal": cita["sucursal"]
    })


        if response.status_code == 200:
                print("[✅] Cita registrada correctamente en la base de datos.")
        else:
                print(f"[❌] Error al registrar cita. Código: {response.status_code}")
    except Exception as e:
        print(f"[❌] Error de conexión al registrar cita: {e}")


def ConfirmView(page: ft.Page):
    cita = page.client_storage.get("cita") or {}
    paciente = page.client_storage.get("paciente") or {}

    def reenviar_correo(_):
        enviar_correo_confirmacion(cita, paciente)
        page.snack_bar = ft.SnackBar(
            content=ft.Text("📧 Correo reenviado correctamente", color="white"),
            bgcolor=colors.SUCCESS,
        )
        page.snack_bar.open = True
        page.update()
        asyncio.run(registrar_en_base(cita, paciente))
 

    # Envío automático al entrar
    reenviar_correo(None)

    pasos = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
        controls=[
            ft.Icon(name="check_circle", color=colors.SUCCESS, size=24),
            ft.Icon(name="check_circle", color=colors.SUCCESS, size=24),
            ft.Icon(name="radio_button_unchecked", color="#CCCCCC", size=24),
        ]
    )

    resumen = ft.Container(
        content=ft.Column([
            ft.Text("🗓 Detalles de la Cita", size=18, weight="bold", color=colors.PRIMARY_DARK),
            ft.Text("Información del paciente:", size=14, weight="bold", color=colors.TEXT_DARK),
            ft.Text(f"👤 {paciente.get('nombre', '')} {paciente.get('apellido', '')}", size=12),
            ft.Text(f"📧 {paciente.get('correo', '')}", size=12),
            ft.Text(f"📱 {paciente.get('telefono', '')}", size=12),

            ft.Divider(),

            ft.Text("Detalles de la cita:", size=14, weight="bold", color=colors.TEXT_DARK),
            ft.Text(f"🦷 Servicio: {cita.get('servicio', '')}", size=12),
            ft.Text(f"📍 Sucursal: {cita.get('sucursal', '')}", size=12),
            ft.Text(f"📅 Fecha: {cita.get('fecha', '')}", size=12),
            ft.Text(f"⏰ Hora: {cita.get('hora', '')}", size=12),
            ft.Text(f"📝 Motivo: {paciente.get('notas', '') or 'No especificado'}", size=12),

            ft.Divider(),

            ft.Row([
                ft.Text("Total:", size=14, weight="bold"),
                ft.Text("$512.00", size=14, weight="bold")
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ],
        spacing=10),
        padding=20,
        bgcolor=colors.PRIMARY_LIGHT,
        border_radius=12,
        width=400,
        shadow=ft.BoxShadow(
            blur_radius=12,
            color="rgba(0,0,0,0.08)",
            offset=ft.Offset(2, 2),
            spread_radius=2
        )
    )

    botones = ft.Row([
        ft.TextButton("← Regresar", on_click=lambda _: page.go("/form")),
        ft.OutlinedButton("🔁 Reenviar", on_click=reenviar_correo),
        ft.ElevatedButton(
            text="💳 Pagar ahora",
            on_click=lambda _: page.go("/pago"),
            bgcolor=colors.SUCCESS,
            style=ft.ButtonStyle(
                color="white",
                text_style=ft.TextStyle(weight="bold", size=14),
                padding=ft.Padding(12, 10, 12, 10)
            )
        )
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    return ft.View(
        route="/confirm",
        controls=[
            pasos,
            ft.Container(height=20),
            ft.Row([resumen], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=20),
            botones
        ],
        padding=30,
        scroll=ft.ScrollMode.AUTO
    )
