import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from sqlalchemy import Column, Integer, String
# Importamos la base declarativa, asumiendo que está definida en models.db
from models.db import Base 


class User(Base):
    """
    Define el modelo de Usuario (User) para la autenticación y como entidad Biciusuario principal.
    Mapeado a la tabla 'users'.
    """
    __tablename__ = 'users' 

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    # Almacena el hash de la contraseña para una gestión segura
    password_hash = Column(String(255), nullable=False) 
    nombre_biciusuario = Column(String(255), nullable=False)

    # Nota: Las relaciones (registros y bicicletas) se definen en el otro archivo de modelos 
    # para evitar una dependencia circular.
    
    # Este método mágico ayuda en la depuración y representación
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"