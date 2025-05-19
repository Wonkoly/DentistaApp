import flet as ft
import sys, os

# Importar colores
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from common import colors


# Tratamientos disponibles
SERVICIOS = [
    {"nombre": "Limpieza Dental", "precio": 350, "descripcion": "Eliminación de sarro y placa dental."},
    {"nombre": "Extracción Dental", "precio": 700, "descripcion": "Extracción de pieza dental dañada."},
    {"nombre": "Ortodoncia", "precio": 1500, "descripcion": "Evaluación y aplicación de brackets."},
    {"nombre": "Blanqueamiento", "precio": 1200, "descripcion": "Tratamiento estético de blanqueo dental."},
    {"nombre": "Carillas Dentales", "precio": 1800, "descripcion": "Carillas estéticas para mejorar tu sonrisa."}
]


def TratamientosView(page: ft.Page) -> ft.View:
    cards = []

    for servicio in SERVICIOS:
        cards.append(
            ft.Container(
                content=ft.Column([
                    ft.Text(f"🦷 {servicio['nombre']}", size=18, weight="bold", color=colors.PRIMARY_DARK),
                    ft.Text(servicio['descripcion'], size=14, color=colors.TEXT_DARK),
                    ft.Text(f"💲 Precio: ${servicio['precio']} MXN", size=14, color=colors.SECONDARY),
                ],
                spacing=5),
                padding=15,
                bgcolor=colors.PRIMARY_LIGHT,
                border_radius=15,
                width=400
            )
        )

    return ft.View(
        route="/tratamientos",
        controls=[
            ft.Text("🦷 Catálogo de Tratamientos", size=24, weight="bold", color=colors.PRIMARY_DARK),
            ft.Text("Explora los tratamientos que ofrecemos en el consultorio.", size=16, color=colors.TEXT_DARK),
            ft.Column(cards, spacing=20),
            ft.ElevatedButton("← Regresar al inicio", on_click=lambda _: page.go("/"))
        ],
        padding=30,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.START
    )