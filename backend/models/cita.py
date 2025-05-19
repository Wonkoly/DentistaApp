from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.database import Base

class Cita(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    servicio_id = Column(Integer, ForeignKey("servicios.id"), nullable=False)
    fecha_hora = Column(DateTime, nullable=False)
    estado = Column(String(50), default="pendiente")  # pendiente, confirmada, cancelada
    notas = Column(Text)

    # Relaciones
    paciente = relationship("Paciente")
    servicio = relationship("Servicio")

