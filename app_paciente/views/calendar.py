import flet as ft
import datetime


def CalendarView(page: ft.Page):
    # Título de la vista
    page.title = "Seleccione Fecha y Hora"

    # Encabezado
    header = ft.Text(
        "Seleccione Fecha y Hora", 
        size=24, 
        weight=ft.FontWeight.BOLD
    )

    # Texto para mostrar la fecha seleccionada
    date_display = ft.Text("--/--/----")

    # Manejador de cambio de fecha
    def _on_date_change(e):
        date_display.value = e.control.value.strftime('%d/%m/%Y')
        page.update()

    # DatePicker nativo en modal
    date_picker = ft.DatePicker(
        first_date=datetime.date(2025, 6, 1),
        last_date=datetime.date(2025, 6, 30),
        on_change=_on_date_change,
    )

    # Botón para abrir el DatePicker
    date_button = ft.ElevatedButton(
        text="Seleccionar Fecha",
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda e: page.open(date_picker)
    )

    # Selector de hora
    times = [
        f"{h}:00 PM" for h in range(2, 9)
    ]
    time_dropdown = ft.Dropdown(
        width=200,
        label="Hora",
        options=[ft.dropdown.Option(t) for t in times],
        value=times[0]
    )

    # Botones de navegación
    nav_buttons = ft.Row(
        [
            ft.ElevatedButton("Regresar", on_click=lambda e: page.go("/")),
            ft.ElevatedButton("Siguiente", on_click=lambda e: page.go("/form")),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        width=400
    )

    # Construir y retornar la vista
    return ft.View(
        route="/calendar",
        controls=[
            ft.Column(
                [
                    header,
                    ft.Row([date_button, date_display], spacing=20),
                    time_dropdown,
                    nav_buttons
                ],
                spacing=30,
                horizontal_alignment=ft.CrossAxisAlignment.START
            )
        ]
    )
