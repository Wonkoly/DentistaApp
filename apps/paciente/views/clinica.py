import flet as ft
import sys, os

# Permite importar desde common/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from common import colors


def ClinicaView(page: ft.Page) -> ft.View:
    return ft.View(
        route="/clinica",
        controls=[
            ft.Text("🏥 Clínica Dental 'Rodolfo Castellón'", size=24, weight="bold", color=colors.PRIMARY_DARK),
            ft.Divider(),
            ft.Text("🕒 Horarios de atención", size=20, weight="w600", color=colors.SECONDARY),
            ft.Text("Lunes a Viernes: 2:00 PM – 8:00 PM\nDescanso: 4:30 PM – 5:00 PM"),

            ft.Text("📍 Dirección", size=20, weight="w600", color=colors.SECONDARY),
            ft.Text("Av. Principal #123, Colonia Centro, Puerto Vallarta, Jalisco"),

            ft.Text("📞 Contacto", size=20, weight="w600", color=colors.SECONDARY),
            ft.Text("Teléfono: 322-123-4567\nCorreo: rodolfo.dental@gmail.com"),

            ft.Text("🧑‍⚕️ Mensaje del doctor", size=20, weight="w600", color=colors.SECONDARY),
            ft.Text("Mi compromiso es brindarte atención dental de calidad, en un ambiente profesional y seguro. Gracias por confiar en nuestra clínica."),

            ft.ElevatedButton(
                text="Agendar una cita",
                bgcolor=colors.PRIMARY,
                color=colors.TEXT_PRIMARY,
                on_click=lambda _: page.go("/tratamientos")
            ),
            ft.TextButton("← Regresar al inicio", on_click=lambda _: page.go("/"))
        ],
        padding=30,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.START
    )
