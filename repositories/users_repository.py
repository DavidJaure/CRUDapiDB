import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from sqlalchemy.orm import Session
# Importamos el modelo User que ya definiste en models/users.model.py
from models.users_model import User 

class UsersRepository:
    """
    Repositorio para la gestión de usuarios (User/Biciusuario) en la base de datos.
    Proporciona métodos CRUD y de búsqueda, cruciales para la autenticación 
    y la gestión del perfil de biciusuario.
    """

    def __init__(self, db_session: Session):
        """Inicializa el repositorio con la sesión de base de datos."""
        self.db = db_session

    def get_all_users(self):
        """Recupera todos los usuarios registrados."""
        logger.info("Obteniendo todos los usuarios desde el repositorio")
        return self.db.query(User).all()

    def get_user_by_id(self, user_id: int):
        """Busca y retorna un usuario por su ID."""
        logger.info(f"Buscando usuario por ID: {user_id}")
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str):
        """
        Busca y retorna un usuario por su nombre de usuario. 
        Método CRUCIAL para el proceso de Login/Autenticación.
        """
        logger.info(f"Buscando usuario por username para login: {username}")
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, username: str, password_hash: str, nombre_biciusuario: str):
        """
        Crea y almacena un nuevo usuario. 
        IMPORTANTE: Recibe el hash de la contraseña, no la contraseña plana.
        """
        logger.info(f"Creando usuario: {username}")
        new_user = User(
            username=username, 
            password_hash=password_hash, 
            nombre_biciusuario=nombre_biciusuario
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
    
    def update_user(self, user_id: int, username: str = None, password_hash: str = None, nombre_biciusuario: str = None):
        """
        Actualiza la información de un usuario existente.
        El 'password_hash' solo se actualiza si se proporciona un nuevo hash.
        """
        user = self.get_user_by_id(user_id)
        if user:
            logger.info(f"Actualizando usuario: {user_id}")
            if username:
                user.username = username
            if password_hash:
                # Solo se asigna si se ha hasheado en la capa de servicio
                user.password_hash = password_hash 
            if nombre_biciusuario:
                user.nombre_biciusuario = nombre_biciusuario
                
            self.db.commit()
            self.db.refresh(user)
            return user
        
        logger.warning(f"Usuario no encontrado para actualizar: {user_id}")
        return None
    
    def delete_user(self, user_id: int):
        """Elimina un usuario de la base de datos según su ID."""
        user = self.get_user_by_id(user_id)
        if user:
            logger.info(f"Eliminando usuario: {user_id}")
            self.db.delete(user)
            self.db.commit()
            return user
        
        logger.warning(f"Usuario no encontrado para eliminar: {user_id}")
        return None
