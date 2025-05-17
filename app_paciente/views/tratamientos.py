
import flet as ft

def TratamientosView(page: ft.Page):
    tratamientos = [
        {"titulo": "Limpieza", "descripcion": "Remueve la placa y el sarro acumulado.", "precio": "$250 MXN"},
        {"titulo": "Extracción", "descripcion": "Extracción segura y sin dolor.", "precio": "$750 MXN"},
        {"titulo": "Ortodoncia", "descripcion": "Corrige la alineación dental con brackets.", "precio": "$1,500 MXN"},
        {"titulo": "Blanqueamiento", "descripcion": "Devuelve el blanco natural a tus dientes.", "precio": "$250 MXN"},
        {"titulo": "Carillas dentales", "descripcion": "Mejora la estética dental cubriendo imperfecciones.", "precio": "$400 MXN"},
    ]

    return ft.View(
        route="/tratamientos",
        controls=[
            ft.Container(
                expand=True,
                bgcolor="#0f172a",
                padding=30,
                content=ft.Column(
                    spacing=30,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            "Tratamientos Dentales Disponibles 🦷",
                            size=28,
                            weight="bold",
                            color=ft.Colors.WHITE,
                            text_align="center"
                        ),
                        ft.Column(
                            spacing=10,
                            controls=[
                                ft.ListTile(
                                    title=ft.Text(t["titulo"], size=20, weight="bold", color=ft.Colors.WHITE),
                                    subtitle=ft.Text(f"{t['descripcion']} — {t['precio']}", size=16, color=ft.Colors.WHITE70),
                                    leading=ft.Icon(name=ft.Icons.CHECK_CIRCLE, color=ft.Colors.LIGHT_GREEN)
                                )
                                for t in tratamientos
                            ]
                        ),
                        ft.Divider(height=1, color=ft.Colors.WHITE24),
                        ft.ElevatedButton(
                            text="← Volver al inicio",
                            icon=ft.Icons.ARROW_BACK,
                            bgcolor=ft.Colors.TEAL,
                            color=ft.Colors.WHITE,
                            on_click=lambda e: page.go("/")
                        )
                    ]
                )
            )
        ]
    )
