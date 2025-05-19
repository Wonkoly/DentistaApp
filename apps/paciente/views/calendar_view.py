import flet as ft
import datetime
import sys, os

# Importar colores LUNA
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from common import colors

def CalendarView(page: ft.Page):
    page.title = "Seleccione Fecha y Hora"

    header = ft.Row([
        ft.CircleAvatar(content=ft.Text("C"), radius=25),
        ft.Column([
            ft.Text("CONSULTORIO DENTAL CHOYO", size=22, weight=ft.FontWeight.BOLD, color=colors.PRIMARY_DARK),
            ft.Text("DENTISTA: RODOLFO CASTELLÓN", size=14, italic=True, color=colors.TEXT_DARK),
        ], spacing=2)
    ], alignment=ft.MainAxisAlignment.START, spacing=15)

    date_display = ft.Text("--/--/----", size=16, weight=ft.FontWeight.W_600)

    def _on_date_change(e):
        date_display.value = e.control.value.strftime('%d/%m/%Y')
        page.update()

    date_picker = ft.DatePicker(
        first_date=datetime.date(2025, 6, 1),
        last_date=datetime.date(2025, 6, 30),
        on_change=_on_date_change,
    )
    page.overlay.append(date_picker)

    date_button = ft.ElevatedButton(
        text="Seleccionar Fecha",
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda e: page.open(date_picker),
        bgcolor=colors.PRIMARY,
        color=colors.TEXT_PRIMARY
    )

    times = [f"{h}:00 PM" for h in range(2, 9)]
    time_dropdown = ft.Dropdown(
        width=200,
        label="Hora",
        options=[ft.dropdown.Option(t) for t in times],
        value=None
    )

    service_dropdown = ft.Dropdown(
        width=250,
        label="Seleccione un servicio",
        options=[
            ft.dropdown.Option("Limpieza dental - $350 MXN"),
            ft.dropdown.Option("Extracción dental - $700 MXN"),
            ft.dropdown.Option("Ortodoncia - $1500 MXN"),
            ft.dropdown.Option("Blanqueamiento - 350 MXN"),
            ft.dropdown.Option("Carillas dentales 1200 MXN")
        ]
    )

    location_dropdown = ft.Dropdown(
        width=250,
        label="Elige la sucursal más cerca de ti",
        options=[
            ft.dropdown.Option("Puerto Vallarta"),
            ft.dropdown.Option("Centro")
        ]
    )

    error_text = ft.Text("", color=colors.ERROR, visible=False)

    def siguiente(e):
        if not service_dropdown.value or not location_dropdown.value or not time_dropdown.value or date_display.value == "--/--/----":
            error_text.value = "⚠️ Todos los campos son obligatorios para continuar."
            error_text.visible = True
            page.update()
            return

        page.client_storage.set("cita", {
            "servicio": service_dropdown.value,
            "sucursal": location_dropdown.value,
            "hora": time_dropdown.value,
            "fecha": date_display.value
        })
        page.go("/form")

    nav_buttons = ft.Row([
        ft.ElevatedButton("Regresar", on_click=lambda e: page.go("/")),
        ft.ElevatedButton("Siguiente", on_click=siguiente, bgcolor=colors.PRIMARY, color=colors.TEXT_PRIMARY)
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

    layout = ft.Column([
        header,
        ft.Divider(),

        ft.Container(
            content=ft.Row(
                [
                    ft.Column([
                        ft.Text("🦷 Servicio", size=16, weight=ft.FontWeight.W_600, color=colors.SECONDARY),
                        service_dropdown,
                        ft.Text("📍 Sucursal", size=16, weight=ft.FontWeight.W_600, color=colors.SECONDARY),
                        location_dropdown
                    ], spacing=15),

                    ft.Column([
                        ft.Text("📅 Fecha", size=16, weight=ft.FontWeight.W_600, color=colors.SECONDARY),
                        date_button,
                        date_display
                    ], spacing=15),

                    ft.Column([
                        ft.Text("⏰ Hora", size=16, weight=ft.FontWeight.W_600, color=colors.SECONDARY),
                        time_dropdown
                    ], spacing=15)
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND
            ),
            padding=20,
            bgcolor=colors.PRIMARY_LIGHT,
            border_radius=10
        ),

        ft.VerticalDivider(opacity=0),
        error_text,
        nav_buttons
    ],
    spacing=30,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    scroll=ft.ScrollMode.AUTO
    )

    return ft.View(
        route="/calendar",
        controls=[layout],
        appbar=ft.AppBar(title=ft.Text("Seleccionar Fecha y Hora", color=colors.TEXT_PRIMARY), bgcolor=colors.PRIMARY),
        scroll=ft.ScrollMode.AUTO
    )