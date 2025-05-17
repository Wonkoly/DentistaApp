import os

def enviar_correo_confirmacion(cita, paciente):
    print("📧 Simulando envío de correo...")
    print(f"Para: {paciente['correo']}")
    print(f"Nombre: {paciente['nombre']}")
    print(f"Servicio: {cita['servicio']}")
    print("✅ Correo enviado (simulado).")

def enviar_sms_confirmacion(cita, paciente):
    print("📱 Simulando envío de SMS...")
    print(f"Para: {paciente['telefono']}")
    print(f"Nombre: {paciente['nombre']}")
    print(f"Servicio: {cita['servicio']}")
    print("✅ SMS enviado (simulado).")