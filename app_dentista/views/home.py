import flet as ft
from theme.components import AppButton, AppDropdown, AppLabel
from theme.colors import PRIMARY_COLOR

def HomeView(page: ft.Page):
    page.title = "Clínica Choyo - Puerto Vallarta"
    page.scroll = "auto"
    page.bgcolor = "#FFFFFF"

    return ft.View(
        route="/",
        vertical_alignment=ft.MainAxisAlignment.START,
        controls=[
            ft.Container(
                expand=True,
                padding=20,
                content=ft.Column(
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        # Header responsivo
                        ft.ResponsiveRow(
                            controls=[
                                ft.Row([
                                    ft.Image(
                                        src="https://cdn-icons-png.flaticon.com/512/1827/1827392.png",
                                        width=20,
                                        height=20
                                    ),
                                    AppLabel("ABIERTO DE 9 AM - 8 PM", size=12)
                                ]),
                                AppLabel("CLÍNICA CHOYO", size=22, bold=True),
                                ft.Row([
                                    AppDropdown("Tratamientos", ["Limpieza", "Ortodoncia", "Blanqueamiento"]),
                                    AppDropdown("Clínica", ["Instalaciones", "Equipo"]),
                                    AppDropdown("Opiniones", ["Ver testimonios"]),
                                    AppButton("PEDIR CITA", on_click=lambda _: page.go("/calendar"))
                                ], wrap=True, spacing=10)
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            run_spacing=10
                        ),

                        ft.Container(height=50),

                        # Cuerpo central
                        AppLabel("CLÍNICA DENTAL EN PUERTO VALLARTA", size=24, bold=True),
                        ft.Container(height=20),
                        AppLabel(
                            "ESTA CLÍNICA DENTAL ESTÁ DISPUESTA A DAR SU MEJOR SERVICIO PARA SUS CLIENTES, "
                            "DONDE SE SIENTAN CÓMODOS Y TENGAN UNA MEJOR EXPERIENCIA, TU SALUD ES PRIMERO, "
                            "Y NOSOTROS NOS ENCARGAREMOS DE QUE TENGAS UNA MEJOR SONRISA AL MUNDO!!",
                            size=16,
                            italic=True
                        ),
                        ft.Container(height=10),
                        AppLabel("REALIZAMOS EVALUACIÓN DENTAL GRATUITA", size=14, italic=True, bold=True),
                        ft.Container(height=40),

                        # Pie de página
                        ft.ResponsiveRow(
                            controls=[
                                AppLabel("CALLE GUATEMALA #125 COL. DEL TORO, EL PITILLAL, PUERTO VALLARTA. JAL", size=12),
                                ft.Column([
                                    AppLabel("DENTISTA: RODOLFO CASTELLÓN", size=12),
                                    AppLabel("322-349-61-55\n322-22-44-847", size=12)
                                ], alignment=ft.MainAxisAlignment.END)
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            run_spacing=10
                        )
                    ]
                )
            )
        ]
    )
