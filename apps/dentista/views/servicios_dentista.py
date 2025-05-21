import flet as ft
from common import colors
from components.navbar import NavbarDentista
import re
from datetime import datetime
import httpx

servicio_map = {
    "Limpieza Bucal": (1, 500),
    "Extracción Dental": (2, 700),
    "Obturación": (3, 900),
    "Ortodoncia": (4, 1500),
    "Blanqueamiento": (5, 1200),
    "Carillas Dentales": (6, 1800)
}

def ServiciosDentistaView(page: ft.Page):
    servicio_dropdown = ft.Dropdown(
        label="Selecciona un servicio",
        options=[ft.dropdown.Option(text=nombre, key=nombre) for nombre in servicio_map.keys()],
        width=300,
        border_color=colors.PRIMARY,
        focused_border_color=colors.PRIMARY_DARK
    )

    precio_text = ft.Text(value="Precio del servicio: $0", size=16)
    total_text = ft.Text(value="Total: $0", size=16, weight=ft.FontWeight.BOLD)

    def actualizar_precio(servicio):
        if servicio in servicio_map:
            precio = servicio_map[servicio][1]
            precio_text.value = f"Precio del servicio: ${precio}"
            total_text.value = f"Total: ${precio}"
            page.update()

    servicio_dropdown.on_change = lambda e: actualizar_precio(e.control.value)

    nombre_input = ft.TextField(label="Nombre del paciente", width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    correo_input = ft.TextField(label="Correo del paciente", width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    fecha_input = ft.TextField(label="Fecha (DD/MM/YYYY)", width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    hora_input = ft.TextField(label="Hora (HH:MM)", width=200, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    am_pm = ft.Dropdown(label="AM / PM", width=100, options=[ft.dropdown.Option("AM"), ft.dropdown.Option("PM")])
    notas_input = ft.TextField(label="Notas / Observaciones", multiline=True, min_lines=3, max_lines=5, width=300,
                               border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    mensaje = ft.Text(value="", color=colors.ERROR, size=14)

    def validar_nombre(valor): return len(valor.strip()) >= 20 and re.fullmatch(r"[A-Za-záéíóúÁÉÍÓÚñÑ ]+", valor)
    def validar_correo(valor): return re.fullmatch(r"[^@]+@[^@]+\.[^@]+", valor)
    def validar_fecha(valor):
        if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", valor): return False
        try: return datetime.strptime(valor, "%d/%m/%Y").year >= 2025
        except ValueError: return False
    def validar_hora(valor, periodo):
        if not re.fullmatch(r"\d{2}:\d{2}", valor): return False
        h, m = map(int, valor.split(":"))
        if not (1 <= h <= 12 and 0 <= m <= 59): return False
        if periodo == "AM":
            return (h == 12 and m == 0) or (7 <= h <= 11)
        elif periodo == "PM":
            return 12 <= h <= 7  # 12:00 PM to 7:59 PM
        return False

    async def registrar_cita(e):
        mensaje.value = ""
        errores = []

        if not servicio_dropdown.value: errores.append("Selecciona un servicio")
        if not validar_nombre(nombre_input.value):
            errores.append("Nombre inválido: mínimo 20 letras, sin números ni símbolos")
            nombre_input.border_color = colors.ERROR
        else: nombre_input.border_color = colors.PRIMARY
        if not validar_correo(correo_input.value):
            errores.append("Correo inválido. Ej: nombre@ejemplo.com")
            correo_input.border_color = colors.ERROR
        else: correo_input.border_color = colors.PRIMARY
        if not validar_fecha(fecha_input.value):
            errores.append("Fecha inválida. Usa DD/MM/YYYY y año ≥ 2025")
            fecha_input.border_color = colors.ERROR
        else: fecha_input.border_color = colors.PRIMARY
        if not validar_hora(hora_input.value, am_pm.value):
            errores.append("Hora inválida. Solo entre 07:00 AM y 07:00 PM")
            hora_input.border_color = colors.ERROR
        else: hora_input.border_color = colors.PRIMARY
        if not am_pm.value:
            errores.append("Selecciona AM o PM")
            am_pm.border_color = colors.ERROR
        else: am_pm.border_color = colors.PRIMARY

        if servicio_dropdown.value not in servicio_map:
            errores.append("El servicio seleccionado no es válido")

        if errores:
            mensaje.value = "❌ " + "\n".join(errores)
            mensaje.color = colors.ERROR
            page.update()
            return

        servicio_id = servicio_map[servicio_dropdown.value][0]

        try:
            usuario_id = page.session.get("usuario_id")

            async with httpx.AsyncClient() as client:
                response = await client.post("http://localhost:8000/api/citas/", json={
                    "usuario_id": usuario_id,
                    "nombre": nombre_input.value,
                    "apellido": "",
                    "correo": correo_input.value,
                    "telefono": "",
                    "notas": notas_input.value,
                    "servicio": servicio_id,
                    "fecha": datetime.strptime(fecha_input.value, "%d/%m/%Y").strftime("%Y-%m-%d"),
                    "hora": hora_input.value + " " + am_pm.value,
                    "sucursal": ""
                })

            if response.status_code == 200:
                mensaje.value = "✅ Cita registrada correctamente"
                mensaje.color = colors.SUCCESS
            else:
                mensaje.value = f"❌ Error al registrar cita: {response.text}"
                mensaje.color = colors.ERROR

        except Exception as ex:
            mensaje.value = f"❌ Error de conexión: {ex}"
            mensaje.color = colors.ERROR

        page.update()

    return ft.View(
        "/servicios_dentista",
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Text("Registro Manual de Cita", size=24, weight=ft.FontWeight.BOLD, color=colors.SECONDARY),
                    servicio_dropdown,
                    precio_text,
                    total_text,
                    nombre_input,
                    correo_input,
                    fecha_input,
                    ft.Row([hora_input, am_pm], alignment=ft.MainAxisAlignment.CENTER),
                    notas_input,
                    ft.ElevatedButton("Registrar cita", on_click=registrar_cita, bgcolor=colors.PRIMARY, color=colors.TEXT_PRIMARY),
                    mensaje
                ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=30,
                bgcolor=colors.PRIMARY_LIGHT,
                border_radius=10
            ),
            NavbarDentista(page=page, ruta_actual="servicios")
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
