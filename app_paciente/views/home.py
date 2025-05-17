
import flet as ft
import datetime
import asyncio

def HomeView(page: ft.Page):
    page.title = "Clínica Dental Choyo"

    hora_actual = ft.Text(size=16, color="white")

    async def reloj_loop():
        while True:
            hora_actual.value = datetime.datetime.now().strftime("🕒 %I:%M %p")
            page.update()
            await asyncio.sleep(1)

    page.run_task(reloj_loop)

    def on_seccion_change(e):
        if e.control.value == "Opiniones":
            page.go("/opiniones")
        elif e.control.value == "Tratamientos":
            page.go("/tratamientos")
        elif e.control.value == "Clínica":
            page.go("/clinica")

    seccion_combo = ft.Dropdown(
        label="Explora",
        options=[
            ft.dropdown.Option("Tratamientos"),
            ft.dropdown.Option("Clínica"),
            ft.dropdown.Option("Opiniones")
        ],
        width=200,
        on_change=on_seccion_change
    )

    bienvenido = ft.Text("CLÍNICA DENTAL EN PUERTO VALLARTA", size=26, weight=ft.FontWeight.BOLD, color="white")

    descripcion = ft.Text(
        "Esta clínica dental está dispuesta a dar su mejor servicio para sus clientes, "
        "donde se sientan cómodos y tengan una mejor experiencia. Tu salud es primero, "
        "¡y nosotros nos encargaremos de que tengas una mejor sonrisa al mundo!!",
        size=18,
        text_align=ft.TextAlign.CENTER,
        color="white"
    )

    contacto = ft.Column([
        ft.Text("📍 Dirección: Calle Guatemala #125, El Pitillal, Puerto Vallarta, JAL", size=14, color="white"),
        ft.Text("📞 Teléfono: 322-349-61-55", size=14, color="white"),
        ft.Text("📧 Email: dentista.choyo@gmail.com", size=14, color="white"),
        ft.Text("🕒 Horarios: Lunes a Sábado, 9:00 am - 6:00 pm", size=14, color="white"),
    ], spacing=5)

    pedir_cita_btn = ft.ElevatedButton(
        text="Pedir cita",
        on_click=lambda e: page.go("/calendar"),
        bgcolor=ft.Colors.BLUE_500,
        color=ft.Colors.WHITE,
        scale=ft.Scale(1),
        animate_scale=ft.Animation(300, "easeOut")
    )

    def on_hover(e):
        if e.data == "true":
            pedir_cita_btn.scale.value = 1.08
            pedir_cita_btn.bgcolor = ft.Colors.BLUE_700
        else:
            pedir_cita_btn.scale.value = 1
            pedir_cita_btn.bgcolor = ft.Colors.BLUE_500
        page.update()

    pedir_cita_btn.on_hover = on_hover

    barra_superior = ft.Row([
        ft.Text("CLÍNICA CHOYO", size=20, weight=ft.FontWeight.BOLD, color="white"),
        seccion_combo,
        ft.Container(expand=True),
        hora_actual
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    contenido = ft.Column([
        barra_superior,
        ft.VerticalDivider(opacity=0),
        ft.Container(
            content=ft.Column([
                bienvenido,
                descripcion,
                contacto,
                pedir_cita_btn
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20),
            alignment=ft.alignment.center,
            padding=40
        )
    ], spacing=25, scroll=ft.ScrollMode.AUTO)

    return ft.View(
        route="/",
        controls=[
            ft.Stack([
                ft.Image(src="assets/6c3e62c8.png", fit=ft.ImageFit.COVER, expand=True),
                ft.Container(
                    content=contenido,
                    expand=True,
                    padding=40,
                    bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.BLACK)
                )
            ], expand=True)
        ]
    )
