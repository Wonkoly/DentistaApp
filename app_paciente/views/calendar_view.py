
import flet as ft
import datetime

def CalendarView(page: ft.Page):
    page.title = "Seleccione Fecha y Hora"

    header = ft.Row([
        ft.CircleAvatar(content=ft.Text("C"), radius=25),
        ft.Column([
            ft.Text("CONSULTORIO DENTAL CHOYO", size=22, weight=ft.FontWeight.BOLD, color="black"),
            ft.Text("DENTISTA: RODOLFO CASTELLÓN", size=14, italic=True),
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
        on_click=lambda e: page.open(date_picker)
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
            ft.dropdown.Option("Limpieza"),
            ft.dropdown.Option("Extracción"),
            ft.dropdown.Option("Ortodoncia"),
            ft.dropdown.Option("Blanqueamiento"),
            ft.dropdown.Option("Carillas dentales")
        ]
    )

    location_dropdown = ft.Dropdown(
        width=250,
        label="Elige la sucursal más cerca de ti",
        options=[
            ft.dropdown.Option("Puerto Vallarta"),
            ft.dropdown.Option("Bahía de Banderas")
        ]
    )

    error_text = ft.Text("", color=ft.Colors.RED_600, visible=False)

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
        ft.ElevatedButton("Siguiente", on_click=siguiente)
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

    layout = ft.Column([
        header,
        ft.Divider(),

        ft.Container(
            content=ft.Row(
                [
                    ft.Column([
                        ft.Text("🦷 Servicio", size=16, weight=ft.FontWeight.W_600),
                        service_dropdown,
                        ft.Text("📍 Sucursal", size=16, weight=ft.FontWeight.W_600),
                        location_dropdown
                    ], spacing=15),

                    ft.Column([
                        ft.Text("📅 Fecha", size=16, weight=ft.FontWeight.W_600),
                        date_button,
                        date_display
                    ], spacing=15),

                    ft.Column([
                        ft.Text("⏰ Hora", size=16, weight=ft.FontWeight.W_600),
                        time_dropdown
                    ], spacing=15)
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND
            ),
            padding=20,
            bgcolor=ft.Colors.BLUE_50,
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
        appbar=ft.AppBar(title=ft.Text("Seleccionar Fecha y Hora")),
        scroll=ft.ScrollMode.AUTO
    )
