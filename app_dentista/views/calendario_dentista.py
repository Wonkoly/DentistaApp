
import flet as ft
from components.navbar import navbar
from datetime import datetime

# Lista global de citas (esto luego se puede guardar en JSON)
citas = [
    {"fecha": "2024-05-13", "hora": "14:00", "paciente": "Ana Gómez", "motivo": "Limpieza dental"},
    {"fecha": "2024-05-13", "hora": "16:00", "paciente": "Luis Pérez", "motivo": "Extracción"},
    {"fecha": "2024-05-14", "hora": "15:00", "paciente": "María Díaz", "motivo": "Revisión general"},
]

def CalendarioDentistaView(page: ft.Page):
    fecha_seleccionada = ft.Text("")
    lista_citas = ft.Column()

    nombre_input = ft.TextField(label="Nombre del paciente", width=300)
    fecha_input = ft.TextField(label="Fecha (YYYY-MM-DD)", width=150)
    hora_input = ft.TextField(label="Hora (HH:MM)", width=150)
    motivo_input = ft.TextField(label="Motivo", width=300)

    def actualizar_citas(fecha: str):
        lista_citas.controls.clear()
        encontrados = [c for c in citas if c["fecha"] == fecha]
        if not encontrados:
            lista_citas.controls.append(ft.Text("No hay citas para esta fecha.", color=ft.colors.AMBER))
        else:
            for cita in encontrados:
                lista_citas.controls.append(
                    ft.Container(
                        content=ft.Text(f"{cita['hora']} - {cita['paciente']} ({cita['motivo']})"),
                        padding=10,
                        bgcolor=ft.colors.BLUE_GREY_100,
                        border_radius=8
                    )
                )
        page.update()

    def seleccionar_fecha(e):
        if datepicker.value:
            fecha_str = datepicker.value.strftime("%Y-%m-%d")
            fecha_input.value = fecha_str  # auto rellenar campo de fecha
            fecha_seleccionada.value = f"Citas para: {fecha_str}"
            actualizar_citas(fecha_str)

    def registrar_cita(e):
        if not nombre_input.value.strip() or not fecha_input.value.strip() or not hora_input.value.strip():
            page.dialog = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text("Todos los campos son obligatorios."), actions=[ft.TextButton("OK", on_click=lambda x: page.dialog.close())])
            page.dialog.open = True
            page.update()
            return

        nueva_cita = {
            "fecha": fecha_input.value.strip(),
            "hora": hora_input.value.strip(),
            "paciente": nombre_input.value.strip(),
            "motivo": motivo_input.value.strip() or "Consulta"
        }

        citas.append(nueva_cita)
        actualizar_citas(fecha_input.value.strip())

        nombre_input.value = ""
        hora_input.value = ""
        motivo_input.value = ""
        page.update()

    datepicker = ft.DatePicker(on_change=seleccionar_fecha)
    page.overlay.append(datepicker)

    return ft.View(
        route="/calendario_dentista",
        appbar=navbar(page),
        controls=[
            ft.Container(
                padding=20,
                content=ft.Column(
                    spacing=20,
                    controls=[
                        ft.Text("Calendario del Dentista", size=28, weight="bold"),
                        ft.ElevatedButton("Seleccionar fecha", on_click=lambda e: datepicker.pick_date()),
                        fecha_seleccionada,
                        lista_citas,
                        ft.Divider(),
                        ft.Text("Registrar nueva cita", size=22, weight="bold"),
                        nombre_input,
                        ft.Row([fecha_input, hora_input]),
                        motivo_input,
                        ft.ElevatedButton("Registrar cita", icon=ft.icons.ADD, on_click=registrar_cita)
                    ]
                )
            )
        ]
    )
