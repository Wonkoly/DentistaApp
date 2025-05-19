from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.database import SessionLocal
from backend.models.usuario import Usuario
from backend.utils.security import hash_password, verificar_password

router = APIRouter(prefix="/api/usuarios", tags=["usuarios"])

# -------------------------------
# 🚀 Dependencia de la base de datos
# -------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------------
# 📩 Modelo para recuperación de contraseña
# -------------------------------
class RecuperarContrasenaRequest(BaseModel):
    email: str
    codigo: str
    nueva_contrasena: str

# -------------------------------
# 🔑 Endpoint: Recuperar contraseña
# -------------------------------
@router.post("/recuperar")
def recuperar_contrasena(data: RecuperarContrasenaRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter_by(email=data.email).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if data.codigo != "123456":  # Aquí debes implementar validación real de código
        raise HTTPException(status_code=400, detail="Código incorrecto")

    usuario.password = hash_password(data.nueva_contrasena)
    db.commit()

    return {"mensaje": "Contraseña actualizada correctamente"}

# -------------------------------
# 📝 Endpoint: Registrar nuevo usuario
# -------------------------------
@router.post("/registrar")
def registrar_usuario(nombre: str, apellido: str, email: str, password: str, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.email == email).first()

    if usuario_existente:
        raise HTTPException(status_code=400, detail="El usuario ya está registrado")

    usuario_nuevo = Usuario(
        nombre=nombre,
        apellido=apellido,
        email=email,
        password=hash_password(password)
    )
    db.add(usuario_nuevo)
    db.commit()

    return {"mensaje": "Usuario registrado exitosamente"}
