import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Carga variables desde .env
load_dotenv()


def get_env_var(name: str) -> str:
    """Obtiene y valida una variable de entorno.

    Args:
        name: Nombre de la variable de entorno.

    Returns:
        str: Valor de la variable de entorno.

    Raises:
        RuntimeError: Si la variable no está definida.
    """

    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"La variable de entorno '{name}' no está definida")
    return value


DB_USER = get_env_var("DB_USER")
DB_PASSWORD = get_env_var("DB_PASSWORD")
DB_HOST = get_env_var("DB_HOST")
DB_PORT = get_env_var("DB_PORT")
DB_NAME = get_env_var("DB_NAME")

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
