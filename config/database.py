import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from models.users_model import Base
from dotenv import load_dotenv


# --- Configuración de Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# --------------------------------

# Cargar variables de entorno desde .env
load_dotenv()

MYSQL_URI = os.getenv('MYSQL_URI')
SQLITE_URI = 'sqlite:///biciusuarios_local.db'

def create_tables():
    """
    Crea todas las tablas definidas en la Base de SQLAlchemy.
    Esta función es esencial para la inicialización.
    """
    logger.info("Creando tablas de la base de datos...")
    Base.metadata.create_all(bind=engine)

def get_engine():
    """
    Intenta crear una conexión con MySQL. Si falla, usa SQLite local.
    """
    if MYSQL_URI:
        try:
            engine = create_engine(MYSQL_URI, echo=True)
            # Probar conexión
            conn = engine.connect()
            conn.close()
            logging.info('Conexión a MySQL exitosa.')
            return engine
        except OperationalError:
            logging.warning('No se pudo conectar a MySQL. Usando SQLite local.')
    # Fallback a SQLite
    engine = create_engine(SQLITE_URI, echo=True)
    return engine

engine = get_engine()
Session = sessionmaker(bind=engine)
SessionLocal = Session  # Alias para compatibilidad con imports existentes
Base.metadata.create_all(engine)

def get_db_session():
    """
    Retorna una nueva sesión de base de datos para ser utilizada en los servicios o controladores.
    """
    return Session()

# Alias para compatibilidad con imports existentes
def get_db():
    """
    Alias de get_db_session para compatibilidad.
    """
    return get_db_session()

