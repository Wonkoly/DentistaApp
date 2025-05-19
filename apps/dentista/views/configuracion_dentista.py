import flet as ft
from common import colors
from components.navbar import NavbarDentista
import re

# Vista para actualizar datos del dentista, incluida su contraseña y foto

def ConfiguracionDentistaView(page: ft.Page):
    nombre_input = ft.TextField(label="Nombre completo", width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    apellido_input = ft.TextField(label="Apellidos completos", width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    correo_input = ft.TextField(label="Correo", width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)

    contra_antigua_input = ft.TextField(label="Contraseña actual", password=True, can_reveal_password=True, width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    nueva_contra_input = ft.TextField(label="Nueva contraseña", password=True, can_reveal_password=True, width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)
    confirmar_contra_input = ft.TextField(label="Confirmar nueva contraseña", password=True, can_reveal_password=True, width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)

    foto_input = ft.TextField(label="Ruta de la fotografía (opcional)", width=300, border_color=colors.PRIMARY, focused_border_color=colors.PRIMARY_DARK)

    mensaje = ft.Text(value="", size=14)

    def es_valido_nombre_apellido(nombre, apellido):
        return (
            7 <= len(nombre.strip()) <= 25 and
            7 <= len(apellido.strip()) <= 25 and
            re.fullmatch(r"[A-Za-záéíóúÁÉÍÓÚñÑ ]+", nombre.strip() + apellido.strip())
        )

    def es_correo_valido(valor):
        return re.fullmatch(r"[^@]+@[^@]+\.[^@]+", valor)

    def es_imagen(val):
        return val.strip() == "" or val.lower().endswith((".jpg", ".jpeg", ".png", ".gif"))

    def guardar_configuracion(e):
        mensaje.value = ""
        errores = []

        if not all([nombre_input.value.strip(), apellido_input.value.strip(), correo_input.value.strip(),
                    contra_antigua_input.value.strip(), nueva_contra_input.value.strip(), confirmar_contra_input.value.strip()]):
            errores.append("❌ Llenar los espacios vacíos")

        if not es_valido_nombre_apellido(nombre_input.value, apellido_input.value):
            errores.append("❌ Nombre y Apellido: entre 7 y 25 letras, solo letras")

        if not es_correo_valido(correo_input.value):
            errores.append("❌ Correo inválido")

        if nueva_contra_input.value != confirmar_contra_input.value:
            errores.append("❌ La nueva contraseña y la confirmación no coinciden")

        if not es_imagen(foto_input.value):
            errores.append("❌ Solo se permiten rutas de imágenes (.jpg, .jpeg, .png, .gif)")

        if errores:
            mensaje.value = "\n".join(errores)
            mensaje.color = colors.ERROR
        else:
            mensaje.value = "✅ Cambios guardados correctamente"
            mensaje.color = colors.SUCCESS

        page.update()

    return ft.View(
        "/configuracion_dentista",
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Text("Configuración del Perfil", size=24, weight=ft.FontWeight.BOLD, color=colors.SECONDARY),
                    nombre_input,
                    apellido_input,
                    correo_input,
                    contra_antigua_input,
                    nueva_contra_input,
                    confirmar_contra_input,
                    foto_input,
                    ft.ElevatedButton(
                        "Guardar cambios",
                        on_click=guardar_configuracion,
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
            NavbarDentista(page=page, ruta_actual="configuracion")
        ]
    )