
import flet as ft
import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from twilio.rest import Client

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

def enviar_mensajes(cita, paciente):
    errores = []
    if not EMAIL_USER:
        errores.append("❌ EMAIL_USER no está definido")
    if not EMAIL_PASS:
        errores.append("❌ EMAIL_PASS no está definido")
    if not TWILIO_ACCOUNT_SID:
        errores.append("❌ TWILIO_ACCOUNT_SID no está definido")
    if not TWILIO_AUTH_TOKEN:
        errores.append("❌ TWILIO_AUTH_TOKEN no está definido")
    if not TWILIO_PHONE:
        errores.append("❌ TWILIO_PHONE no está definido")

    if errores:
        return False, False, "\n".join(errores)

    # Enviar correo
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Confirmación de tu cita dental"
        msg["From"] = EMAIL_USER
        msg["To"] = paciente["correo"]

        html = f'''
        <html>
          <body>
            <h2>Confirmación de cita</h2>
            <p><strong>Nombre:</strong> {paciente["nombre"]}</p>
            <p><strong>Correo:</strong> {paciente["correo"]}</p>
            <p><strong>Teléfono:</strong> {paciente["telefono"]}</p>
            <hr>
            <p><strong>Servicio:</strong> {cita["servicio"]}</p>
            <p><strong>Sucursal:</strong> {cita["sucursal"]}</p>
            <p><strong>Fecha:</strong> {cita["fecha"]}</p>
            <p><strong>Hora:</strong> {cita["hora"]}</p>
          </body>
        </html>
        '''

        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, paciente["correo"], msg.as_string())

        correo_ok = True
    except Exception as e:
        print("Error al enviar correo:", e)
        correo_ok = False

    # Enviar SMS
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        mensaje = f"Cita confirmada para {paciente['nombre']} el {cita['fecha']} a las {cita['hora']}"
        client.messages.create(
            body=mensaje,
            from_=TWILIO_PHONE,
            to=f"+52{paciente['telefono']}"
        )
        sms_ok = True
    except Exception as e:
        print("Error al enviar SMS:", e)
        sms_ok = False

    return correo_ok, sms_ok, None

def ConfirmView(page: ft.Page):
    cita = page.client_storage.get("cita") or {}
    paciente = page.client_storage.get("paciente") or {}

    status = ft.Text("", visible=False)

    def reenviar(e):
        status.visible = True
        page.update()
        correo_ok, sms_ok, error_env = enviar_mensajes(cita, paciente)
        if error_env:
            status.value = error_env
            status.color = "red"
        elif correo_ok and sms_ok:
            status.value = "✅ Correo y SMS enviados correctamente"
            status.color = "green"
        elif correo_ok:
            status.value = "✅ Correo enviado, pero SMS falló"
            status.color = "orange"
        elif sms_ok:
            status.value = "✅ SMS enviado, pero correo falló"
            status.color = "orange"
        else:
            status.value = "❌ No se pudo enviar ni correo ni SMS"
            status.color = "red"
        page.update()

    return ft.View(
        route="/confirm",
        controls=[
            ft.Text("Resumen de tu cita", size=20, weight=ft.FontWeight.BOLD),
            ft.Text(f"👤 {paciente.get('nombre', '')}"),
            ft.Text(f"📧 {paciente.get('correo', '')}"),
            ft.Text(f"📱 {paciente.get('telefono', '')}"),
            ft.Text(f"🦷 {cita.get('servicio', '')}"),
            ft.Text(f"📍 {cita.get('sucursal', '')}"),
            ft.Text(f"📅 {cita.get('fecha', '')}"),
            ft.Text(f"⏰ {cita.get('hora', '')}"),
            ft.Divider(),
            status,
            ft.ElevatedButton("Reenviar", on_click=reenviar),
            ft.OutlinedButton("Volver al inicio", on_click=lambda e: page.go("/"))
        ],
        scroll=ft.ScrollMode.AUTO
    )
