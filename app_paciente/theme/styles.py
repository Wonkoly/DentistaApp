import flet as ft
from .colors import BUTTON_BG, BUTTON_TEXT, TEXT_COLOR

BUTTON_STYLE = ft.ButtonStyle(
    color=BUTTON_TEXT,
    bgcolor=BUTTON_BG,
    padding=ft.padding.symmetric(horizontal=20, vertical=12),
    shape=ft.RoundedRectangleBorder(radius=10),
)

LABEL_STYLE = {
    "size": 14,
    "color": TEXT_COLOR
}
