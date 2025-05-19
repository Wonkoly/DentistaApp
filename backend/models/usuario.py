from sqlalchemy import Column, Integer, String, Boolean
from backend.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    telefono = Column(String(20))
    rol = Column(String(50), default="dentista")  # o administrador
    activo = Column(Boolean, default=True)

