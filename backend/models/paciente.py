from sqlalchemy import Column, Integer, String, Text
from backend.database import Base

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefono = Column(String(20), nullable=False)
    domicilio = Column(String(255))
    ciudad = Column(String(100))
    codigo_postal = Column(String(10))
    notas = Column(Text)  # puede incluir motivo, observaciones, etc.


