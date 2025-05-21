from sqlalchemy import Column, Integer, String
from database import Base

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, nullable=False, unique=True)
    telefono = Column(String, nullable=True)
    registrado_por = Column(String, default="paciente")
