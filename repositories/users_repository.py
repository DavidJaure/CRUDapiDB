import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound
from typing import Optional, List, Dict, Any
from models.users_model import User 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UsersRepository:
    """
    Capas de repositorio para la gestión de datos de la tabla 'users'.
    Interactúa directamente con la sesión de SQLAlchemy.
    """
    def __init__(self, db_session: Session):
        self.db = db_session
        logger.info("Repositorio de Usuarios inicializado.")
        
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Busca un usuario por su ID, incluyendo relaciones."""
        logger.info(f"Buscando usuario por ID: {user_id}")
        return self.db.query(User).filter(User.id == user_id).first()
        
    def get_all_users(self) -> List[User]:
        """Obtiene todos los usuarios."""
        logger.info("Obteniendo todos los usuarios.")
        return self.db.query(User).all()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Busca un usuario por su nombre de usuario (para login)."""
        logger.info(f"Buscando usuario por username: {username}")
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
            raise ValueError(f"El usuario o email ya existe.")
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error desconocido al añadir usuario: {e}")
            raise e
            
    # --- NUEVOS MÉTODOS PARA SOPORTAR EL SERVICE ---
    
    def update_user_scalars(self, user_id: int, data: Dict[str, Any]) -> Optional[User]:
        """
        Actualiza los campos principales (escalares) del modelo User. 
        Este método es una alternativa al Service para la actualización simple.
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return None
            
        try:
            if 'nombre_biciusuario' in data:
                user.nombre_biciusuario = data['nombre_biciusuario']
            
            # La actualización de Bicicletas y Registros se maneja en el Service
            
            self.db.commit()
            self.db.refresh(user)
            logger.info(f"Campos escalares del Usuario ID {user_id} actualizados.")
            return user
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error al actualizar campos escalares del usuario {user_id}: {e}")
            return None

    def delete_user(self, user_id: int) -> Optional[User]:
        """
        Elimina un usuario por ID. 
        Retorna el usuario eliminado o None.
        """
        user = self.get_user_by_id(user_id)
        if user:
            self.db.delete(user)
            try:
                self.db.commit()
                logger.info(f"Usuario ID {user_id} eliminado exitosamente.")
                return user
            except Exception as e:
                self.db.rollback()
                logger.error(f"Error al confirmar la eliminación del usuario {user_id}: {e}")
                return None
        return None
