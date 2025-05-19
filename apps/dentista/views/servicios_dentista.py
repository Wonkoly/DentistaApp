import flet as ft
from common import colors
from components.navbar import NavbarDentista
import re
from datetime import datetime

# Vista para mostrar servicios y registrar citas manualmente

def ServiciosDentistaView(page: ft.Page):
    servicio_dropdown = ft.Dropdown(
        label="Selecciona un servicio",
        options=[
            ft.dropdown.Option("Limpieza Bucal"),
            ft.dropdown.Option("Extracción Dental"),
            ft.dropdown.Option("Obturación"),
            ft.dropdown.Option("Ortodoncia"),
            ft.dropdown.Option("Blanqueamiento"),
            ft.dropdown.Option("Carillas Dentales")
        ],
        width=300,
        border_color=colors.PRIMARY,
        focused_border_color=colors.PRIMARY_DARK
    )

    nombre_input = ft.TextField(label="Nombre del paciente", width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    correo_input = ft.TextField(label="Correo del paciente", width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    fecha_input = ft.TextField(label="Fecha (DD/MM/YYYY)", width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    hora_input = ft.TextField(label="Hora (HH:MM)", width=200, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    am_pm = ft.Dropdown(label="AM / PM", width=100, options=[
        ft.dropdown.Option("AM"),
        ft.dropdown.Option("PM")
    ])
    mensaje = ft.Text(value="", color=colors.ERROR, size=14)

    def validar_nombre(valor):
        return len(valor.strip()) >= 20 and re.fullmatch(r"[A-Za-záéíóúÁÉÍÓÚñÑ ]+", valor)

    def validar_correo(valor):
        return re.fullmatch(r"[^@]+@[^@]+\.[^@]+", valor)

    def validar_fecha(valor):
        if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", valor):
            return False
        try:
            f = datetime.strptime(valor, "%d/%m/%Y")
            return f.year >= 2025
        except ValueError:
            return False

    def validar_hora(valor):
        if not re.fullmatch(r"\d{2}:\d{2}", valor):
            return False
        h, m = map(int, valor.split(":"))
        return 0 <= h <= 23 and 0 <= m <= 59

    def registrar_cita(e):
        mensaje.value = ""
        errores = []

        if not servicio_dropdown.value:
            errores.append("Selecciona un servicio")

        if not validar_nombre(nombre_input.value):
            errores.append("Nombre inválido: mínimo 20 letras, sin números ni símbolos")
            nombre_input.border_color = colors.ERROR
        else:
            nombre_input.border_color = colors.PRIMARY

        if not validar_correo(correo_input.value):
            errores.append("Correo inválido. Ej: nombre@ejemplo.com")
            correo_input.border_color = colors.ERROR
        else:
            correo_input.border_color = colors.PRIMARY

        if not validar_fecha(fecha_input.value):
            errores.append("Fecha inválida. Usa DD/MM/YYYY y año ≥ 2025")
            fecha_input.border_color = colors.ERROR
        else:
            fecha_input.border_color = colors.PRIMARY

        if not validar_hora(hora_input.value):
            errores.append("Hora inválida. Usa HH:MM con valores válidos")
            hora_input.border_color = colors.ERROR
        else:
            hora_input.border_color = colors.PRIMARY

        if not am_pm.value:
            errores.append("Selecciona AM o PM")
            am_pm.border_color = colors.ERROR
        else:
            am_pm.border_color = colors.PRIMARY

        if errores:
            mensaje.value = "❌ " + "\n".join(errores)
            mensaje.color = colors.ERROR
        else:
            mensaje.value = f"✅ Cita registrada para {nombre_input.value} el {fecha_input.value} a las {hora_input.value} {am_pm.value}"
            mensaje.color = colors.SUCCESS

        page.update()

    return ft.View(
        "/servicios_dentista",
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Text("Registro Manual de Cita", size=24, weight=ft.FontWeight.BOLD, color=colors.SECONDARY),
                    servicio_dropdown,
                    nombre_input,
                    correo_input,
                    fecha_input,
                    ft.Row([hora_input, am_pm], alignment=ft.MainAxisAlignment.CENTER),
                    ft.ElevatedButton(
                        "Registrar cita",
                        on_click=registrar_cita,
                        bgcolor=colors.PRIMARY,
                        color=colors.TEXT_PRIMARY
                    ),
                    mensaje
                ],
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=30,
                bgcolor=colors.PRIMARY_LIGHT,
                border_radius=10
            ),
            NavbarDentista(page=page, ruta_actual="servicios")
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )