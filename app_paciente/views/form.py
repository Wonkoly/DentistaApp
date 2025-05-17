
import flet as ft

def FormView(page: ft.Page):
    nombre = ft.TextField(label="Nombre completo", width=400, bgcolor=ft.Colors.WHITE, value=page.client_storage.get("nombre") or "")
    correo = ft.TextField(label="Correo electrónico", width=400, bgcolor=ft.Colors.WHITE, value=page.client_storage.get("correo") or "")
    telefono = ft.TextField(label="Teléfono celular", width=400, bgcolor=ft.Colors.WHITE, value=page.client_storage.get("telefono") or "")
    motivo = ft.TextField(label="Motivo de la cita", multiline=True, min_lines=3, width=400, bgcolor=ft.Colors.WHITE, value=page.client_storage.get("motivo") or "")

    mensaje_error = ft.Text("", color=ft.Colors.RED)

    def validar_datos(e):
        if not (10 <= len(nombre.value.strip()) <= 45) or not nombre.value.replace(" ", "").isalpha():
            mensaje_error.value = "El nombre debe tener entre 10 y 45 letras, sin números ni caracteres especiales."
        elif not (correo.value and "@" in correo.value and "." in correo.value):
            mensaje_error.value = "Ingresa un correo válido."
        elif not (telefono.value.isdigit() and len(telefono.value) == 10):
            mensaje_error.value = "El teléfono debe tener exactamente 10 dígitos numéricos."
        elif not motivo.value.strip():
            mensaje_error.value = "Por favor, describe el motivo de la cita."
        else:
            page.client_storage.set("nombre", nombre.value)
            page.client_storage.set("correo", correo.value)
            page.client_storage.set("telefono", telefono.value)
            page.client_storage.set("motivo", motivo.value)
            page.go("/confirm")
            return
        page.update()

    return ft.View(
        route="/form",
        controls=[
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                bgcolor=ft.Colors.BLUE_900,
                content=ft.Column(
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text("Ingresa los datos de tu cita", size=24, weight="bold", color=ft.Colors.WHITE),
                        nombre,
                        correo,
                        telefono,
                        motivo,
                        mensaje_error,
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.ElevatedButton("← Regresar", bgcolor=ft.Colors.RED_400, color=ft.Colors.WHITE, on_click=lambda e: page.go("/calendar")),
                                ft.ElevatedButton("Siguiente →", bgcolor=ft.Colors.GREEN_400, color=ft.Colors.WHITE, on_click=validar_datos)
                            ]
                        )
                    ]
                )
            )
        ]
    )
