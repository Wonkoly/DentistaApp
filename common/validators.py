import re
from typing import Tuple


def validar_email(email: str) -> Tuple[bool, str]:
    """Valida el formato y el dominio de un correo electrónico.

    Args:
        email: Correo electrónico a validar.

    Returns:
        Tuple con un booleano que indica si es válido y un mensaje de error.
    """
    pattern = r'^[\w\.-]+@([\w\.-]+\.\w+)$'
    match = re.match(pattern, email)
    if not match:
        return False, "Correo electrónico no válido"

    dominio = email.split('@')[1].lower()
    dominios_prohibidos = {
        "gmai.com": "¿Quisiste decir gmail.com?",
        "hotmial.com": "¿Quisiste decir hotmail.com?",
        "yaho.com": "¿Quisiste decir yahoo.com?",
        "outlok.com": "¿Quisiste decir outlook.com?",
        "gmal.com": "¿Quisiste decir gmail.com?",
    }
    if dominio in dominios_prohibidos:
        return False, dominios_prohibidos[dominio]
    return True, ""
