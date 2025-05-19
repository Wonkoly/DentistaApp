from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.database import Base
from backend.models.paciente import Paciente
from backend.models.servicio import Servicio  # ✅ Asegúrate de importar esto
paciente = relationship("Paciente", back_populates="citas")


class Cita(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    servicio_id = Column(Integer, ForeignKey("servicios.id"), nullable=False)
    fecha_hora = Column(DateTime, nullable=False)
    estado = Column(String(50), default="pendiente")
    notas = Column(Text)

    # Relaciones
    paciente = relationship("Paciente", back_populates="citas")
    servicio = relationship("Servicio", back_populates="citas")
