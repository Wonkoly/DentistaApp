import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from common.validators import validar_email


def test_email_valido():
    assert validar_email("usuario@example.com") == (True, "")


def test_email_formato_invalido():
    valido, mensaje = validar_email("usuarioexample.com")
    assert not valido
    assert mensaje == "Correo electrónico no válido"


def test_email_dominios_sugeridos():
    valido, mensaje = validar_email("usuario@gmai.com")
    assert not valido
    assert mensaje == "¿Quisiste decir gmail.com?"
