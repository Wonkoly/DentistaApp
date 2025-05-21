from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.paciente import Paciente
from backend.models.cita import Cita
from datetime import datetime, time

router = APIRouter()

class CitaInput(BaseModel):
    usuario_id: int 
    nombre: str
    apellido: str
    correo: str
    telefono: str
    notas: str = ""
    servicio: int
    fecha: str  # "YYYY-MM-DD"
    hora: str   # "HH:MM AM/PM" o "HH:MM"
    sucursal: str = ""

@router.get("/api/citas/")
def listar_citas(db: Session = Depends(get_db)):
    return db.query(Cita).all()


@router.post("/api/citas/")
def registrar_cita(data: CitaInput, db: Session = Depends(get_db)):
    # Convertir hora en formato 12h o 24h
    try:
        fecha_hora = datetime.strptime(f"{data.fecha} {data.hora}", "%Y-%m-%d %I:%M %p")
    except ValueError:
        try:
            fecha_hora = datetime.strptime(f"{data.fecha} {data.hora}", "%Y-%m-%d %H:%M")
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha y hora inválido.")

    # Validación de horario laboral
    hora_cita = fecha_hora.time()
    hora_inicio = time(14, 0)            # 2:00 PM
    hora_descanso_ini = time(16, 30)     # 4:30 PM
    hora_descanso_fin = time(17, 0)      # 5:00 PM
    hora_fin = time(20, 0)               # 8:00 PM

    if not (hora_inicio <= hora_cita <= hora_fin) or (hora_descanso_ini <= hora_cita < hora_descanso_fin):
        raise HTTPException(status_code=400, detail="La hora seleccionada no está disponible dentro del horario laboral.")

    # Buscar o registrar paciente
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

    # Crear cita
    cita = Cita(
        paciente_id=paciente.id,
        servicio_id=data.servicio,
        fecha_hora=fecha_hora,
        estado="pendiente",
        notas=data.notas,
        usuario_id=data.usuario_id
    )
    db.add(cita)
    db.commit()

    return {"mensaje": "Cita registrada correctamente", "id": cita.id}


@router.get("/api/pacientes")
def obtener_pacientes_con_citas(db: Session = Depends(get_db)):
    pacientes_db = db.query(Paciente).all()
    resultado = []

    for paciente in pacientes_db:
        citas = db.query(Cita).filter(Cita.paciente_id == paciente.id).all()
        citas_formateadas = [
            f"{cita.fecha_hora.strftime('%Y-%m-%d %H:%M')} - Servicio ID: {cita.servicio_id}"
            for cita in citas
        ]
        resultado.append({
            "nombre": paciente.nombre,
            "correo": paciente.email,
            "telefono": paciente.telefono,
            "citas": citas_formateadas
        })

    return resultado


@router.get("/api/citas_completas")
def obtener_citas_completas(usuario_id: int = Query(...), db: Session = Depends(get_db)):
    citas = db.query(Cita).filter(Cita.usuario_id == usuario_id).all()
    resultado = []

    for cita in citas:
        resultado.append({
            "paciente_id": cita.paciente.id,
            "nombre": f"{cita.paciente.nombre} {cita.paciente.apellido}",
            "fecha": cita.fecha_hora.strftime("%Y-%m-%d"),
            "hora": cita.fecha_hora.strftime("%H:%M"),
            "servicio": cita.servicio.nombre,
            "notas": cita.notas or "Sin notas",
            "pago_en_linea": "Sí" if cita.estado == "pagado" else "No"
        })

    return resultado
