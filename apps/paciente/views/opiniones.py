import flet as ft
import sys, os, json, re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from common import colors

RUTA_OPINIONES = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../storage/opiniones.json'))


def cargar_opiniones():
    if not os.path.exists(RUTA_OPINIONES):
        return []
    with open(RUTA_OPINIONES, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_opiniones(opiniones):
    os.makedirs(os.path.dirname(RUTA_OPINIONES), exist_ok=True)
    with open(RUTA_OPINIONES, "w", encoding="utf-8") as f:
        json.dump(opiniones, f, indent=2, ensure_ascii=False)


def validar_nombre(texto):
    if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$', texto):
        return False
    letras = len(re.sub(r'\s+', '', texto))
    return letras >= 20


def OpinionesView(page: ft.Page) -> ft.View:
    nombre = ft.TextField(label="Nombre", width=300)
    comentario = ft.TextField(label="Comentario", multiline=True, width=300, min_lines=3, max_lines=5)
    lista_opiniones = ft.Column()
    mensaje_error = ft.Text("", visible=False, color=colors.ERROR)
    snackbar = ft.SnackBar(content=ft.Text("Gracias por tu comentario ✅"))

    opiniones = cargar_opiniones()
    eliminar_index = ft.Ref[int]()
    dlg = ft.AlertDialog()

    def renderizar_opiniones():
        lista_opiniones.controls.clear()
        for i, op in enumerate(opiniones):
            lista_opiniones.controls.append(crear_opinion_card(op["nombre"], op["comentario"], i))
        page.update()

    def crear_opinion_card(nombre_op, comentario_op, index):
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(f"🧑 {nombre_op}", weight="bold", size=16, color=colors.PRIMARY_DARK),
                    ft.Text(f"💬 {comentario_op}", color=colors.TEXT_DARK),
                    ft.ElevatedButton(
                        "Eliminar",
                        icon=ft.Icon(name="delete"),
                        bgcolor=colors.ERROR,
                        color="white",
                        on_click=lambda e: confirmar_eliminacion(index)
                    )
                ], spacing=10),
                padding=10,
                bgcolor=colors.PRIMARY_LIGHT,
                border_radius=10
            )
        )

    def confirmar_eliminacion(index):
        eliminar_index.value = index
        dlg.title = ft.Text("⚠️ Confirmación")
        dlg.content = ft.Text("¿Seguro que quieres eliminar este comentario?")
        dlg.actions = [
            ft.TextButton("Cancelar", on_click=cerrar_dialogo),
            ft.TextButton("Eliminar", on_click=confirmar_si)
        ]
        dlg.actions_alignment = ft.MainAxisAlignment.END
        dlg.open = True
        page.dialog = dlg
        page.update()

    def cerrar_dialogo(e=None):
        dlg.open = False
        page.update()

    def confirmar_si(e=None):
        index = eliminar_index.value
        if 0 <= index < len(opiniones):
            del opiniones[index]
            guardar_opiniones(opiniones)
            renderizar_opiniones()
        cerrar_dialogo()

    def agregar_opinion(e):
        nombre_valor = nombre.value.strip()
        comentario_valor = comentario.value.strip()

        if not nombre_valor or not comentario_valor:
            mensaje_error.value = "⚠️ Debe llenar los campos vacíos."
            mensaje_error.visible = True
            page.update()
            return

        if not validar_nombre(nombre_valor):
            mensaje_error.value = "⚠️ El nombre solo debe contener letras y mínimo 20 caracteres."
            mensaje_error.visible = True
            page.update()
            return

        mensaje_error.visible = False
        nueva_opinion = {"nombre": nombre_valor, "comentario": comentario_valor}
        opiniones.append(nueva_opinion)
        guardar_opiniones(opiniones)
        renderizar_opiniones()

        nombre.value = ""
        comentario.value = ""
        page.snack_bar = snackbar
        snackbar.open = True
        page.update()

    # Inicializar lista
    renderizar_opiniones()

    return ft.View(
        route="/opiniones",
        controls=[
            ft.Text("⭐ Opiniones de pacientes", size=24, weight="bold", color=colors.PRIMARY_DARK),
            mensaje_error,
            nombre,
            comentario,
            ft.ElevatedButton(
                text="Enviar opinión",
                icon=ft.Icon(name="send"),
                on_click=agregar_opinion,
                bgcolor=colors.PRIMARY,
                color=colors.TEXT_PRIMARY
            ),
            ft.Divider(),
            ft.Text("🗣 Comentarios publicados:", size=18, weight="w600", color=colors.SECONDARY),
            lista_opiniones,
            ft.TextButton("← Regresar", on_click=lambda _: page.go("/")),
            snackbar
        ],
        padding=30,
        scroll=ft.ScrollMode.AUTO
    )
