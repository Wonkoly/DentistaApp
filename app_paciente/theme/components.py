import flet as ft
from .styles import BUTTON_STYLE, LABEL_STYLE
from .colors import TEXT_COLOR

def AppButton(text, on_click=None, expand=False):
    return ft.ElevatedButton(
        text=text,
        style=BUTTON_STYLE,
        on_click=on_click,
        expand=expand
    )

def AppDropdown(label, options, width=150):
    return ft.Dropdown(
        label=label,
        options=[ft.dropdown.Option(opt) for opt in options],
        width=width,
        label_style=ft.TextStyle(**LABEL_STYLE)
    )

def AppLabel(texto, size=14, bold=False, italic=False):
    return ft.Text(
        texto,
        size=size,
        color=TEXT_COLOR,
        weight=ft.FontWeight.BOLD if bold else ft.FontWeight.NORMAL,
        italic=italic
    )
