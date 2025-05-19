import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

import flet as ft
import re
from datetime import datetime
from common import colors
from common.email import enviar_factura


def PagoView(page: ft.Page) -> ft.View:
    metodo_pago = ft.Ref[ft.RadioGroup]()
    tarjeta = ft.TextField(label="Número de tarjeta", width=300)
    titular = ft.TextField(label="Titular", width=300)
    expiracion = ft.TextField(label="Fecha de expiración (MMYY)", width=300)
    cvv = ft.TextField(label="CVV", width=150)

    snack_bar = ft.SnackBar(
        content=ft.Text(""),
        bgcolor=colors.ERROR
    )

    def confirmar_pago(e):
        numero = tarjeta.value.strip()
        titular_nombre = titular.value.strip()
        expiracion_valor = expiracion.value.strip()
        cvv_valor = cvv.value.strip()

        # Validaciones completas
        if not numero or not titular_nombre or not expiracion_valor or not cvv_valor:
            snack_bar.content.value = "⚠️ Todos los campos son obligatorios."
        elif not numero.isdigit() or len(numero) != 16:
            snack_bar.content.value = "❌ Número de tarjeta inválido. Debe tener 16 dígitos numéricos."
        elif not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$", titular_nombre):
            snack_bar.content.value = "❌ El nombre del titular solo debe contener letras."
        elif not expiracion_valor.isdigit() or len(expiracion_valor) != 4:
            snack_bar.content.value = "❌ Fecha inválida. Usa formato MMYY."
        else:
            mes = int(expiracion_valor[:2])
            anio = int("20" + expiracion_valor[2:])
            now = datetime.now()
            if mes < 1 or mes > 12 or anio < now.year or (anio == now.year and mes < now.month):
                snack_bar.content.value = "❌ Fecha de expiración no puede ser anterior a hoy."
            elif not cvv_valor.isdigit() or len(cvv_valor) != 3:
                snack_bar.content.value = "❌ CVV inválido. Deben ser 3 dígitos."
            else:
                # ✅ Datos válidos
                page.client_storage.set("pago", {
                    "numero": numero,
                    "titular": titular_nombre,
                    "expiracion": expiracion_valor,
                    "cvv": cvv_valor,
                    "metodo": metodo_pago.current.value
                })
                page.go("/pago_exitoso")
                return

        page.snack_bar = snack_bar
        snack_bar.open = True
        page.update()

    selector_metodos = ft.RadioGroup(
        ref=metodo_pago,
        content=ft.Row(
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Column([
                    ft.Image(src="mastercard.png", width=60),
                    ft.Radio(value="Mastercard", label="")
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Column([
                    ft.Image(src="visa.png", width=60),
                    ft.Radio(value="Visa", label="")
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Column([
                    ft.Image(src="paypal.png", width=60),
                    ft.Radio(value="PayPal", label="")
                ], alignment=ft.MainAxisAlignment.CENTER)
            ]
        )
    )

    campos_tarjeta = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        wrap=True,
        controls=[tarjeta, titular, expiracion, cvv]
    )

    resumen_pago = ft.Column([
        ft.Divider(thickness=1),
        ft.Text("Subtotal: $500.00"),
        ft.Text("Comisión: $12.00"),
        ft.Text("Total: $512.00", weight="bold", size=16)
    ], spacing=4)

    botones = ft.Row([
        ft.ElevatedButton(
            text="CONFIRMAR PAGO",
            bgcolor=colors.SUCCESS,
            color="white",
            on_click=confirmar_pago
        ),
        ft.TextButton(
            "← Regresar",
            on_click=lambda _: page.go("/confirm"),
            style=ft.ButtonStyle(color=colors.PRIMARY)
        )
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    pasos = ft.Row([
        ft.Icon(name="check_circle", color=colors.SUCCESS, size=24),
        ft.Icon(name="check_circle", color=colors.SUCCESS, size=24),
        ft.Icon(name="check_circle", color=colors.SUCCESS, size=24),
    ], alignment=ft.MainAxisAlignment.CENTER)

    return ft.View(
        route="/pago",
        controls=[
            pasos,
            ft.Container(
                bgcolor=colors.PRIMARY_LIGHT,
                border_radius=10,
                padding=20,
                content=ft.Column([
                    ft.Text("🪙 Selecciona un método de pago", size=18, weight="bold"),
                    selector_metodos,
                    snack_bar,
                    campos_tarjeta,
                    resumen_pago,
                    botones
                ], spacing=20)
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
def PagoExitosoView(page: ft.Page) -> ft.View:
    from common.email import enviar_factura

    cita = page.client_storage.get("cita") or {}
    paciente = page.client_storage.get("paciente") or {}
    pago = page.client_storage.get("pago") or {}

    def reenviar_factura(e):
        enviar_factura(cita, paciente, pago)
        page.snack_bar = ft.SnackBar(ft.Text("📩 Factura enviada al correo"), bgcolor=colors.SUCCESS)
        page.snack_bar.open = True
        page.update()

    tarjeta_info = f"{pago.get('numero', '')[:4]} **** **** {pago.get('numero', '')[-4:]}"
    fecha = pago.get("expiracion", "----")
    cvv = "***"

    detalles = ft.Container(
        width=600,
        bgcolor=colors.PRIMARY_LIGHT,
        border_radius=10,
        padding=30,
        shadow=ft.BoxShadow(blur_radius=12, color=colors.SECONDARY_DARK),
        content=ft.Column([
            ft.Text("✅ ¡Pago realizado con éxito!", size=24, weight="bold", color=colors.SUCCESS, text_align="center"),
            ft.Divider(),
            ft.Text("📋 Resumen de la factura", size=20, weight="bold"),
            ft.Text(f"👤 Nombre del paciente: {paciente.get('nombre', '')}"),
            ft.Text(f"📧 Correo electrónico: {paciente.get('correo', '')}"),
            ft.Text(f"📞 Teléfono: {paciente.get('telefono', '')}"),
            ft.Divider(thickness=1),
            ft.Text("🦷 Detalles de la cita:", weight="bold"),
            ft.Text(f"🗓 Fecha: {cita.get('fecha', '')}"),
            ft.Text(f"🕒 Hora: {cita.get('hora', '')}"),
            ft.Text(f"🏥 Sucursal: {cita.get('sucursal', '')}"),
            ft.Text(f"📝 Motivo: {paciente.get('notas', 'N/A')}"),
            ft.Text(f"📌 Servicio: {cita.get('servicio', '')}"),
            ft.Divider(thickness=1),
            ft.Text("💳 Datos del pago:", weight="bold"),
            ft.Text(f"🏦 Tarjeta: {tarjeta_info}"),
            ft.Text(f"📆 Expiración: {fecha}"),
            ft.Text(f"🔐 CVV: {cvv}"),
            ft.Text(f"💰 Total pagado: $512.00", weight="bold", size=18),
            ft.Divider(),
            ft.Row([
                ft.TextButton("← Regresar al inicio", on_click=lambda _: page.go("/"), style=ft.ButtonStyle(color=colors.PRIMARY)),
                ft.ElevatedButton("📧 Enviar factura al correo", on_click=reenviar_factura, bgcolor=colors.SUCCESS, color="white")
            ], alignment=ft.MainAxisAlignment.END)
        ], spacing=10)
    )

    return ft.View(
        route="/pago_exitoso",
        controls=[
            ft.Row([
                ft.Icon(name="check_circle", color=colors.SUCCESS),
                ft.Icon(name="check_circle", color=colors.SUCCESS),
                ft.Icon(name="check_circle", color=colors.SUCCESS),
            ], alignment=ft.MainAxisAlignment.CENTER),
            detalles
        ],
        padding=40,
        bgcolor=colors.BACKGROUND
    )