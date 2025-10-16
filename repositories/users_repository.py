import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional
from models.users_model import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UsersRepository:
    """
    Capa de repositorio para la gestión de datos de la tabla 'users'.
    Interactúa directamente con la sesión de SQLAlchemy.
    """
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Busca un usuario por su nombre de usuario."""
        logger.info(f"Buscando usuario por username: {username}")
        #Usamos .first() en lugar de .scalar_one_or_none()
        # .first() ejecuta la consulta y devuelve el primer objeto o None
        return self.db.query(User).filter(User.username == username).first()

    def add(self, user: User) -> User:
        """Guarda un nuevo objeto User en la base de datos."""
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            logger.info(f"Usuario {user.username} añadido exitosamente con ID {user.id}.")
            return user
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Error de integridad al añadir usuario: {e}")
            raise ValueError(f"El usuario o email ya existe.") # Error más amigable
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error desconocido al añadir usuario: {e}")
            raise e