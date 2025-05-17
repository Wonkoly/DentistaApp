import flet as ft
import smtplib
import ssl
from email.message import EmailMessage

def PagoView(page: ft.Page):
    page.title = "Pago en línea"
    page.bgcolor = ft.Colors.WHITE

    # Recuperar datos
    nombre = page.client_storage.get("nombre") or "Paciente"
    correo = page.client_storage.get("correo") or "correo@ejemplo.com"
    telefono = page.client_storage.get("telefono") or "Sin número"
    motivo = page.client_storage.get("motivo") or "Sin motivo"
    cita = page.client_storage.get("cita") or {}
    servicio = cita.get("servicio", "Tratamiento")
    precio = "$1,000 MXN"
    fecha = cita.get("fecha", "Sin fecha")
    hora = cita.get("hora", "Sin hora")
    sucursal = cita.get("sucursal", "Sin sucursal")

    mensaje = ft.Text(value="", size=14, color=ft.Colors.GREEN_400, visible=False)

    # Campos de tarjeta
    nombre_tarjeta = ft.Dropdown(
        label="Banco emisor",
        width=350,
        options=[
            ft.dropdown.Option("BBVA"),
            ft.dropdown.Option("SANTANDER"),
            ft.dropdown.Option("BANORTE")
        ]
    )
    numero_tarjeta = ft.TextField(label="Número de tarjeta", width=350, hint_text="1234 5678 9012 3456")
    expiracion = ft.TextField(label="Expiración", width=170, hint_text="MM/AA")
    cvv = ft.TextField(label="CVV", width=170, password=True, can_reveal_password=True)

    def enviar_comprobante():
        try:
            email_emisor = "dentista.choyo@gmail.com"
            email_contraseña = "gunr jovz luvu tpot"
            email_receptor = correo

            asunto = "Comprobante de pago - Clínica Choyo"
            cuerpo = f"""Hola {nombre},

Tu pago ha sido registrado correctamente.

🦷 Tratamiento: {servicio}
📅 Fecha: {fecha}
🕒 Hora: {hora}
📍 Sucursal: {sucursal}
💳 Monto: {precio}

Gracias por tu preferencia.

— Clínica Dental Choyo
"""

            mensaje_correo = EmailMessage()
            mensaje_correo["From"] = email_emisor
            mensaje_correo["To"] = email_receptor
            mensaje_correo["Subject"] = asunto
            mensaje_correo.set_content(cuerpo)

            contexto = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as smtp:
                smtp.login(email_emisor, email_contraseña)
                smtp.send_message(mensaje_correo)

        except Exception as err:
            print("Error al enviar el comprobante:", err)

    
    
    def procesar_pago(e):
        import re
        mensaje.visible = True

        # Reset borders
        nombre_tarjeta.border_color = None
        numero_tarjeta.border_color = None
        expiracion.border_color = None
        cvv.border_color = None

        if not nombre_tarjeta.value:
            mensaje.value = "❗ El nombre en la tarjeta es obligatorio."
            mensaje.color = ft.Colors.RED
            nombre_tarjeta.border_color = ft.Colors.RED
        elif re.search(r"[^a-zA-Z\s]", nombre_tarjeta.value):
            mensaje.value = "❗ El nombre no debe contener números ni caracteres especiales."
            mensaje.color = ft.Colors.RED
            nombre_tarjeta.border_color = ft.Colors.RED
        elif not numero_tarjeta.value.isdigit():
            mensaje.value = "❗ El número de tarjeta solo debe contener dígitos."
            mensaje.color = ft.Colors.RED
            numero_tarjeta.border_color = ft.Colors.RED
        elif not re.match(r"^\d{2}/\d{2}$", expiracion.value):
            mensaje.value = "❗ La expiración debe estar en formato MM/YY (ej. 12/28)."
            mensaje.color = ft.Colors.RED
            expiracion.border_color = ft.Colors.RED
        elif not cvv.value.isdigit() or len(cvv.value) != 3:
            mensaje.value = "❗ El CVV debe tener exactamente 3 números."
            mensaje.color = ft.Colors.RED
            cvv.border_color = ft.Colors.RED
        else:
            enviar_comprobante()
            mensaje.value = "✅ Pago realizado con éxito. Se ha enviado un comprobante a tu correo electrónico."
            mensaje.color = ft.Colors.GREEN_600

        page.update()
    
        import re
        mensaje.visible = True

        # Validaciones
        if not nombre_tarjeta.value:
            mensaje.value = "❗ El nombre en la tarjeta es obligatorio."
            mensaje.color = ft.Colors.RED
        elif re.search(r"[^a-zA-Z\s]", nombre_tarjeta.value):
            mensaje.value = "❗ El nombre no debe contener números ni caracteres especiales."
            mensaje.color = ft.Colors.RED
        elif not numero_tarjeta.value.isdigit():
            mensaje.value = "❗ El número de tarjeta solo debe contener dígitos."
            mensaje.color = ft.Colors.RED
        elif not re.match(r"^\d{2}/\d{2}$", expiracion.value):
            mensaje.value = "❗ La expiración debe estar en formato MM/YY (ej. 12/28)."
            mensaje.color = ft.Colors.RED
        elif not cvv.value.isdigit() or len(cvv.value) != 3:
            mensaje.value = "❗ El CVV debe tener exactamente 3 números."
            mensaje.color = ft.Colors.RED
        else:
            enviar_comprobante()
            mensaje.value = "✅ Pago realizado con éxito. Se ha enviado un comprobante a tu correo electrónico."
            mensaje.color = ft.Colors.GREEN_600

        page.update()
    
        if not nombre_tarjeta.value.strip() or not numero_tarjeta.value.strip() or not expiracion.value.strip() or not cvv.value.strip():
            mensaje.value = "❗ Todos los campos de la tarjeta son obligatorios."
            mensaje.color = ft.Colors.RED
            mensaje.visible = True
            page.update()
            return
        enviar_comprobante()
        mensaje.value = "✅ Pago realizado con éxito. Se ha enviado un comprobante a tu correo electrónico."
        mensaje.color = ft.Colors.GREEN_600
        mensaje.visible = True
        page.update()

    def regresar(e):
        page.go("/confirmacion")

    return ft.View(
        route="/pago",
        controls=[
            ft.Container(
                expand=True,
                padding=30,
                alignment=ft.alignment.center,
                bgcolor=ft.Colors.WHITE,
                content=ft.Column(
                    spacing=30,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text("Pago en línea", size=28, weight="bold", text_align="center", color=ft.Colors.BLACK),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                            controls=[
                                # Columna izquierda: pago
                                ft.Column(
                                    spacing=15,
                                    width=400,
                                    controls=[
                                        ft.Text("Información de la tarjeta", size=20, weight="bold", color=ft.Colors.BLACK),
                                        nombre_tarjeta,
                                        numero_tarjeta,
                                        ft.Row([expiracion, cvv], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                        mensaje
                                    ]
                                ),
                                # Columna derecha: resumen
                                ft.Container(
                                    padding=20,
                                    bgcolor=ft.Colors.BLUE_50,
                                    border_radius=10,
                                    width=400,
                                    content=ft.Column(
                                        spacing=12,
                                        controls=[
                                            ft.Text("Resumen de la cita", size=20, weight="bold", color=ft.Colors.BLACK),
                                            ft.Text(f"👤 Nombre: {nombre}", color=ft.Colors.BLACK),
                                            ft.Text(f"📧 Correo: {correo}", color=ft.Colors.BLACK),
                                            ft.Text(f"📱 Teléfono: {telefono}", color=ft.Colors.BLACK),
                                            ft.Text(f"🦷 Servicio: {servicio}", color=ft.Colors.BLACK),
                                            ft.Text(f"📍 Sucursal: {sucursal}", color=ft.Colors.BLACK),
                                            ft.Text(f"📅 Fecha: {fecha}", color=ft.Colors.BLACK),
                                            ft.Text(f"🕒 Hora: {hora}", color=ft.Colors.BLACK),
                                            ft.Text(f"💳 Total: {precio}", weight="bold", color=ft.Colors.BLACK),
                                        ]
                                    )
                                )
                            ]
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.ElevatedButton("← Regresar", icon=ft.Icons.ARROW_BACK, on_click=regresar, bgcolor=ft.Colors.RED, color=ft.Colors.WHITE),
                                ft.ElevatedButton("💳 Realizar pago", icon=ft.Icons.PAYMENT, on_click=procesar_pago, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE)
                            ]
                        )
                    ]
                )
            )
        ]
    )