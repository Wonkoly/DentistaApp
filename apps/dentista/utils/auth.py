# utils/auth.py
import re
import hashlib
import json
from pathlib import Path

USERS_FILE = Path(__file__).resolve().parent.parent / "database" / "dummy_users.json"


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def validar_email(email: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


def cargar_usuarios():
    if USERS_FILE.exists():
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return []


def guardar_usuarios(lista):
    with open(USERS_FILE, "w") as f:
        json.dump(lista, f, indent=4)


def usuario_existe(email: str) -> bool:
    usuarios = cargar_usuarios()
    return any(u["email"] == email for u in usuarios)


def registrar_usuario(nombre: str, apellido: str, email: str, password: str):
    usuarios = cargar_usuarios()
    if usuario_existe(email):
        return False
    usuarios.append({
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "password": hash_password(password)
    })
    guardar_usuarios(usuarios)
    return True


def autenticar_usuario(email: str, password: str) -> bool:
    usuarios = cargar_usuarios()
    hashed = hash_password(password)
    return any(u["email"] == email and u["password"] == hashed for u in usuarios)
