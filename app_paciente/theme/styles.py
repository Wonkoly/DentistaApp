import flet as ft
from .colors import PRIMARY_COLOR, TEXT_COLOR

BUTTON_STYLE = ft.ButtonStyle(
    color=ft.colors.WHITE,
    bgcolor=PRIMARY_COLOR,
    padding=ft.padding.symmetric(horizontal=20, vertical=12),
    shape=ft.RoundedRectangleBorder(radius=10),
)

LABEL_STYLE = {
    "size": 14,
    "color": TEXT_COLOR
}
