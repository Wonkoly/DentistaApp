import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_confirmacion_cita(nombre, correo, telefono, servicio, sucursal, fecha, hora, motivo, total):
    remitente = "dentista.choyo@gmail.com"
    password = "gunr jovz luvu tpot"
    destinatario = paciente.get (correo)

    asunto = "Confirmación de tu cita dental"
    cuerpo = f"""
    Hola {nombre},

    Esta es la confirmación de tu cita:

    📅 Fecha: {fecha}
    🕒 Hora: {hora}
    🦷 Servicio: {servicio}
    📍 Sucursal: {sucursal}
    📞 Teléfono: {telefono}
    📝 Motivo: {motivo}
    💵 Total: ${total} MXN

    ¡Gracias por confiar en nosotros!
    Clínica Dental Choyo
    """

    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto
    msg.attach(MIMEText(cuerpo, 'plain'))

    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remitente, password)
        servidor.send_message(msg)
        servidor.quit()
        print("[✅] Correo enviado con éxito.")
        return True
    except Exception as e:
        print(f"[❌] Error enviando el correo: {e}")
        return False
