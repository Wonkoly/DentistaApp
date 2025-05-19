from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.paciente import Paciente
from backend.models.cita import Cita
from datetime import datetime

router = APIRouter()

from pydantic import BaseModel

class CitaInput(BaseModel):
    nombre: str
    apellido: str
    correo: str
    telefono: str
    notas: str = ""
    servicio: int
    fecha: str  # formato "YYYY-MM-DD"
    hora: str   # formato "HH:MM"
    sucursal: str = ""

@router.get("/api/citas/")
def listar_citas(db: Session = Depends(get_db)):
    return db.query(Cita).all()
@router.post("/api/citas/")
def registrar_cita(data: CitaInput, db: Session = Depends(get_db)):
    # Verifica si el paciente ya existe
    paciente = db.query(Paciente).filter(Paciente.email == data.correo).first()

    if not paciente:
        paciente = Paciente(
            nombre=data.nombre,
            apellido=data.apellido,
            email=data.correo,
            telefono=data.telefono,
            notas=data.notas
        )
        db.add(paciente)
        db.commit()
        db.refresh(paciente)
        

    # Crear cita asociada
    fecha_hora = datetime.strptime(f"{data.fecha} {data.hora}", "%Y-%m-%d %H:%M")

    cita = Cita(
        paciente_id=paciente.id,
        servicio_id=data.servicio,  # asegurarte que exista en la tabla servicios
        fecha_hora=fecha_hora,
        notas=data.notas,
        estado="pendiente"
    )

    db.add(cita)
    db.commit()

    return {"mensaje": "Cita registrada correctamente", "id": cita.id}
