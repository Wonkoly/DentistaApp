import flet as ft
import json
import os
from datetime import datetime

class OpinionesView(ft.View):
    def __init__(self, page):
        super().__init__(route="/opiniones", scroll="auto")
        self.page = page
        self.ruta_archivo = os.path.join(os.path.dirname(__file__), "..", "database", "opiniones.json")
        os.makedirs(os.path.dirname(self.ruta_archivo), exist_ok=True)

        self.opiniones = self.cargar_opiniones()
        self.index_a_eliminar = None
        self.opiniones_column = ft.Column(spacing=15)

        self.input_nombre = ft.TextField(label="Nombre del paciente", width=400, color=ft.Colors.WHITE)
        self.input_opinion = ft.TextField(label="Escribe tu opinión", width=400, multiline=True, min_lines=3, color=ft.Colors.WHITE)
        self.btn_enviar = ft.ElevatedButton("Enviar opinión", on_click=self.enviar_opinion, bgcolor=ft.Colors.TEAL, color=ft.Colors.WHITE)

        self.btn_volver = ft.TextButton("← Volver al inicio", on_click=lambda e: self.page.go("/"), style=ft.ButtonStyle(color=ft.Colors.BLUE_200))

        self.controls.append(
            ft.Container(
                expand=True,
                bgcolor="#0f172a",
                padding=30,
                content=ft.Column(
                    spacing=25,
                    controls=[
                        ft.Text("Opiniones de nuestros pacientes", size=28, weight="bold", color=ft.Colors.WHITE),
                        self.opiniones_column,
                        self.input_nombre,
                        self.input_opinion,
                        ft.Row([self.btn_enviar, self.btn_volver], spacing=10)
                    ]
                )
            )
        )

    def did_mount(self):
        self.actualizar_opiniones()

    def cargar_opiniones(self):
        if os.path.exists(self.ruta_archivo):
            try:
                with open(self.ruta_archivo, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def guardar_opiniones(self):
        with open(self.ruta_archivo, "w", encoding="utf-8") as f:
            json.dump(self.opiniones, f, ensure_ascii=False, indent=4)

    def mostrar_mensaje(self, texto, color):
        self.page.snack_bar = ft.SnackBar(ft.Text(texto, color=ft.Colors.WHITE), bgcolor=color, open=True)
        self.page.update()

    def confirmar_eliminacion(self, e, idx):
        self.index_a_eliminar = idx
        dialog = ft.AlertDialog(
            title=ft.Text("¿Confirmar eliminación?"),
            content=ft.Text("Esta acción no se puede deshacer."),
            actions=[
                ft.TextButton("Cancelar", on_click=self.cerrar_dialogo),
                ft.TextButton("Eliminar", on_click=self.eliminar_opinion),
            ],
            on_dismiss=self.cerrar_dialogo
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def cerrar_dialogo(self, e=None):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.dialog = None
            self.page.update()

    def eliminar_opinion(self, e=None):
        idx = self.index_a_eliminar
        if 0 <= idx < len(self.opiniones):
            self.opiniones.pop(idx)
            self.guardar_opiniones()
            self.actualizar_opiniones()
            self.mostrar_mensaje("✅ Opinión eliminada", ft.Colors.GREEN)
        self.cerrar_dialogo()

    
    def generar_callback_eliminar(self, idx):
        return lambda e: self.confirmar_eliminacion(e, idx)

    def actualizar_opiniones(self):
        self.opiniones_column.controls.clear()
        for i, item in enumerate(self.opiniones):
            nombre = item["nombre"]
            texto = item["texto"]
            fecha = item["fecha"]
            self.opiniones_column.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Row(
                            alignment="spaceBetween",
                            controls=[
                                ft.Row(controls=[
                                    ft.Icon(ft.Icons.RECORD_VOICE_OVER, color=ft.Colors.LIGHT_GREEN),
                                    ft.Text(f"{nombre} dijo:", color=ft.Colors.WHITE, weight="bold")
                                ]),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color=ft.Colors.RED,
                                    tooltip="Eliminar opinión",
                                    on_click=self.generar_callback_eliminar(i)
                                )
                            ]
                        ),
                        ft.Text(texto, color=ft.Colors.WHITE),
                        ft.Text(f"🕒 {fecha}", size=12, color=ft.Colors.WHITE54),
                        ft.Divider(color=ft.Colors.WHITE24)
                    ])
                )
            )
        self.page.update()

    def enviar_opinion(self, e):
        nombre = self.input_nombre.value.strip()
        texto = self.input_opinion.value.strip()

        if not nombre or not texto:
            self.mostrar_mensaje("Llenar los campos obligatorios", ft.Colors.RED)
            return

        nueva_opinion = {
            "nombre": nombre,
            "texto": texto,
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        self.opiniones.append(nueva_opinion)
        self.guardar_opiniones()
        self.actualizar_opiniones()
        self.input_nombre.value = ""
        self.input_opinion.value = ""
        self.page.update()
        self.mostrar_mensaje("✅ Opinión guardada", ft.Colors.GREEN)
