
import flet as ft
from utils.email import enviar_correo_confirmacion


def ConfirmView(page: ft.Page):
    datos = {
        "nombre": page.client_storage.get("nombre"),
        "correo": page.client_storage.get("correo"),
        "telefono": page.client_storage.get("telefono"),
        "motivo": page.client_storage.get("motivo"),
        **(page.client_storage.get("cita") or {})
    }

    mensaje_envio = ft.Text("", size=14, color=ft.Colors.GREEN_400, visible=False, text_align="center")

    def reenviar_correo(e):
        enviar_correo_confirmacion(cita=datos, paciente=datos)
        mensaje_envio.value = "✅ Se ha reenviado la confirmación al correo electrónico."
        mensaje_envio.color = ft.Colors.GREEN_400
        mensaje_envio.visible = True
        page.update()

    def ir_pago(e):
        page.go("/pago")

    def regresar(e):
        page.go("/form")

    return ft.View(
        "/confirm",
        bgcolor="#f1f5f9",
        controls=[
            ft.Column(
                alignment="center",
                horizontal_alignment="center",
                expand=True,
                controls=[
                    ft.Text("Confirmación de datos de cita", size=24, weight="bold", color=ft.Colors.WHITE, text_align="center"),
                    ft.Container(
                        bgcolor="#334155",
                        border_radius=10,
                        padding=20,
                        content=ft.Column(
                            spacing=10,
                            controls=[
                                ft.Row([
                                    ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE),
                                    ft.Text(f"Nombre: {datos.get('nombre', '')}", color=ft.Colors.WHITE),
                                ]),
                                ft.Row([
                                    ft.Icon(ft.Icons.EMAIL, color=ft.Colors.WHITE),
                                    ft.Text(f"Correo: {datos.get('correo', '')}", color=ft.Colors.WHITE),
                                ]),
                                ft.Row([
                                    ft.Icon(ft.Icons.PHONE, color=ft.Colors.WHITE),
                                    ft.Text(f"Teléfono: {datos.get('telefono', '')}", color=ft.Colors.WHITE),
                                ]),
                                ft.Row([
                                    ft.Icon(ft.Icons.MEDICAL_SERVICES, color=ft.Colors.WHITE),
                                    ft.Text(f"Servicio: {datos.get('servicio', '')}", color=ft.Colors.WHITE),
                                ]),
                                ft.Row([
                                    ft.Icon(ft.Icons.LOCATION_ON, color=ft.Colors.WHITE),
                                    ft.Text(f"Sucursal: {datos.get('sucursal', '')}", color=ft.Colors.WHITE),
                                ]),
                                ft.Row([
                                    ft.Icon(ft.Icons.CALENDAR_MONTH, color=ft.Colors.WHITE),
                                    ft.Text(f"Fecha: {datos.get('fecha', '')}", color=ft.Colors.WHITE),
                                ]),
                                ft.Row([
                                    ft.Icon(ft.Icons.ACCESS_TIME, color=ft.Colors.WHITE),
                                    ft.Text(f"Hora: {datos.get('hora', '')}", color=ft.Colors.WHITE),
                                ]),
                                ft.Row([
                                    ft.Icon(ft.Icons.EDIT, color=ft.Colors.WHITE),
                                    ft.Text(f"Motivo: {datos.get('motivo', '')}", color=ft.Colors.WHITE),
                                ]),
                            ]
                        )
                    ),
                    mensaje_envio,
                    ft.Row(
                        alignment="center",
                        controls=[
                            ft.ElevatedButton("← Regresar", icon=ft.Icons.ARROW_BACK, bgcolor=ft.Colors.RED_400, color="white", on_click=regresar),
                            ft.ElevatedButton("Confirmar cita ✅", icon=ft.Icons.CHECK, bgcolor=ft.Colors.TEAL, color="white", on_click=reenviar_correo),
                            ft.ElevatedButton("Pagar ahora 🟩", icon=ft.Icons.PAYMENTS, bgcolor=ft.Colors.GREEN, color="white", on_click=ir_pago),
                        ]
                    )
                ]
            )
        ]
    )
