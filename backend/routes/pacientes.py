from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from backend.models import Paciente

router = APIRouter()

@router.get("/pacientes")
def obtener_pacientes(db: Session = Depends(get_db)):
    return db.query(Paciente).all()

@router.post("/pacientes")
def crear_paciente(paciente: dict, db: Session = Depends(get_db)):
    if db.query(Paciente).filter(Paciente.correo == paciente["correo"]).first():
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    nuevo = Paciente(
        nombre=paciente["nombre"],
        correo=paciente["correo"],
        telefono=paciente.get("telefono", ""),
        registrado_por=paciente.get("registrado_por", "paciente")
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo
