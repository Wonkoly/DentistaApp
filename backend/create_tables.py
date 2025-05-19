import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.database import Base, engine
from backend.models import paciente, usuario, servicio, cita

print("🛠️ Creando las tablas en la base de datos...")

Base.metadata.create_all(bind=engine)

print("✅ Tablas creadas correctamente.")

