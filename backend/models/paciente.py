from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from backend.database import Base

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    apellido = Column(String(100))
    email = Column(String(100), unique=True)
    telefono = Column(String(20))
    notas = Column(Text)

    # ✅ ESTA ES LA PARTE QUE FALTA
    citas = relationship("Cita", back_populates="paciente")

