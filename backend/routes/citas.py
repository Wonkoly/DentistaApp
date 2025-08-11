from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.paciente import Paciente
from backend.models.cita import Cita
from datetime import datetime, time

router = APIRouter(prefix="/api/citas")

class CitaInput(BaseModel):
    usuario_id: int
    nombre: str
    apellido: str
    correo: str
    telefono: str
    notas: str = ""
    servicio: int
    fecha: str
    hora: str
    sucursal: str = ""


@router.get("/")
def listar_citas(db: Session = Depends(get_db)):
    return db.query(Cita).all()


@router.post("/")
def registrar_cita(data: CitaInput, db: Session = Depends(get_db)):
    formatos = ["%Y-%m-%d %I:%M %p", "%Y-%m-%d %H:%M"]
    fecha_hora = None
    for formato in formatos:
        try:
            fecha_hora = datetime.strptime(f"{data.fecha} {data.hora}", formato)
            break
        except ValueError:
            continue
    if not fecha_hora:
        raise HTTPException(
            status_code=400,
            detail="La hora seleccionada está fuera del horario laboral permitido (2:00 PM a 8:00 PM, excluyendo 4:30–5:00 PM)."
        )

    hora_cita = fecha_hora.time()
    hora_inicio = time(14, 0)
    hora_descanso_ini = time(16, 30)
    hora_descanso_fin = time(17, 0)
    hora_fin = time(20, 0)

    if not (hora_inicio <= hora_cita <= hora_fin) or (hora_descanso_ini <= hora_cita < hora_descanso_fin):
        raise HTTPException(
            status_code=400,
            detail="La hora seleccionada está fuera del horario laboral permitido (2:00 PM a 8:00 PM, excluyendo 4:30–5:00 PM)."
        )

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


@router.get("/pacientes")
def obtener_pacientes_con_citas(db: Session = Depends(get_db)):
    pacientes_db = db.query(Paciente).all()
    resultado = []

    for paciente in pacientes_db:
        if not paciente.nombre or not paciente.email:
            continue
        citas = db.query(Cita).filter(Cita.paciente_id == paciente.id).all()
        citas_formateadas = [
            f"{cita.fecha_hora.strftime('%Y-%m-%d %H:%M')} - Servicio ID: {cita.servicio_id}"
            for cita in citas
        ]
        resultado.append({
            "nombre": paciente.nombre,
            "correo": paciente.email,
            "telefono": paciente.telefono or "No disponible",
            "citas": citas_formateadas
        })

    return resultado


@router.get("/citas_completas")
def obtener_citas_completas(usuario_id: int = Query(...), db: Session = Depends(get_db)):
    citas = db.query(Cita).filter(Cita.usuario_id == usuario_id, Cita.estado != "finalizada").all()
    resultado = []

    for cita in citas:
        resultado.append({
            "id": cita.id,
            "paciente_id": cita.paciente.id,
            "nombre": f"{cita.paciente.nombre} {cita.paciente.apellido}",
            "fecha": cita.fecha_hora.strftime("%Y-%m-%d"),
            "hora": cita.fecha_hora.strftime("%H:%M"),
            "servicio": cita.servicio.nombre if cita.servicio else f"ID {cita.servicio_id}",
            "notas": cita.notas or "Sin notas",
            "pago_en_linea": "Sí" if cita.estado == "pagado" else "No"
        })

    return resultado


@router.put("/{cita_id}/finalizar")
def finalizar_cita(cita_id: int, db: Session = Depends(get_db)):
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    cita.estado = "finalizada"
    db.commit()

    return {"mensaje": "Cita finalizada correctamente"}


@router.get("/finalizadas")
def obtener_citas_finalizadas(usuario_id: int = Query(...), db: Session = Depends(get_db)):
    citas = db.query(Cita).filter(Cita.usuario_id == usuario_id, Cita.estado == "finalizada").all()
    resultado = []

    for cita in citas:
        resultado.append({
            "id": cita.id,
            "paciente_id": cita.paciente.id,
            "nombre": f"{cita.paciente.nombre} {cita.paciente.apellido}",
            "fecha": cita.fecha_hora.strftime("%Y-%m-%d"),
            "hora": cita.fecha_hora.strftime("%H:%M"),
            "servicio": cita.servicio.nombre if cita.servicio else f"ID {cita.servicio_id}",
            "notas": cita.notas or "Sin notas",
            "pago_en_linea": "Sí" if cita.estado == "pagado" else "No",
            "estado": cita.estado
        })

    return resultado
