
import flet as ft

def ClinicaView(page: ft.Page):
    return ft.View(
        route="/",
        controls=[
            ft.Container(
                expand=True,
                bgcolor="#0f172a",
                alignment=ft.alignment.center,
                padding=40,
                content=ft.Column(
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text("Bienvenido a Clínica Dental Choyo", size=28, weight="bold", color=ft.Colors.WHITE, text_align="center"),
                        ft.Text("Nos especializamos en ofrecer atención dental de calidad en un ambiente cómodo y profesional.", size=18, color=ft.Colors.WHITE70, text_align="center"),
                        ft.Text("📍 Calle Guatemala #125, El Pitillal, Puerto Vallarta, JAL", size=16, color=ft.Colors.WHITE, text_align="center"),
                        ft.Text("📞 Teléfono: 322-349-61-55", size=16, color=ft.Colors.WHITE, text_align="center"),
                        ft.Text("✉️ Email: dentista.choyo@gmail.com", size=16, color=ft.Colors.WHITE, text_align="center"),
                        ft.Text("⏰ Horarios: Lunes a Sábado, 9:00 am - 6:00 pm", size=16, color=ft.Colors.WHITE, text_align="center"),
                        ft.ElevatedButton("← Volver al inicio", on_click=lambda e: page.go("/"), bgcolor=ft.Colors.TEAL, color=ft.Colors.WHITE)
                    ]
                )
            )
        ]
    )
