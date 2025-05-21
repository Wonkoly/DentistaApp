from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models.usuario import Usuario
from backend.utils.security import hashear_password, verificar_password

router = APIRouter(prefix="/api/usuarios", tags=["usuarios"])

# ✅ Modelo de entrada para registro
class RegistroInput(BaseModel):
    nombre: str
    apellido: str
    email: str
    password: str

class LoginInput(BaseModel):
    email: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Registro
@router.post("/registrar")
def registrar_usuario(data: RegistroInput, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.email == data.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El usuario ya está registrado")

    usuario_nuevo = Usuario(
        nombre=data.nombre,
        apellido=data.apellido,
        email=data.email,
        password=hashear_password(data.password)
    )

    db.add(usuario_nuevo)
    db.commit()
    db.refresh(usuario_nuevo)

    return {"mensaje": "Usuario registrado exitosamente", "usuario_id": usuario_nuevo.id}


# ✅ Login
@router.post("/login")

def login(data: LoginInput, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == data.email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if not verificar_password(data.password, usuario.password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    return {
        "mensaje": "Inicio de sesión exitoso",
        "usuario_id": usuario.id,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "email": usuario.email,
        "rol": usuario.rol
    }

