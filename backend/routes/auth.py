from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models.usuario import Usuario
from backend.utils.security import hashear_password, verificar_password

router = APIRouter(prefix="/api/usuarios", tags=["usuarios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/registrar")
def registrar_usuario(nombre: str, apellido: str, email: str, password: str, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El usuario ya está registrado")

    usuario_nuevo = Usuario(
        nombre=nombre,
        apellido=apellido,
        email=email,
        password=hashear_password(password)
    )

    db.add(usuario_nuevo)
    db.commit()
    db.refresh(usuario_nuevo)

    return {"mensaje": "Usuario registrado exitosamente", "usuario_id": usuario_nuevo.id}

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if not verificar_password(password, usuario.password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    return {
        "mensaje": "Inicio de sesión exitoso",
        "usuario_id": usuario.id,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "email": usuario.email,
        "rol": usuario.rol
    }

