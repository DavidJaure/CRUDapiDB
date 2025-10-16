import logging
from sqlalchemy.orm import Session
# Importamos la librería de hashing que usaremos para seguridad
from werkzeug.security import generate_password_hash, check_password_hash 

# Importamos el modelo y el repositorio
from repositories.users_repository import UserRepository
from models.users_model import User 
from models.db import RegistroBiciusuario 
# Usamos RegistroBiciusuario solo para referencia si fuera necesario, 
# pero la lógica principal usa User.

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UsersService:
    """
    Capa de servicios para la gestión de usuarios y la seguridad (autenticación).
    Se encarga de hashear contraseñas, verificar credenciales y delegar el CRUD.
    """
    def __init__(self, db_session: Session):
        """Inicializa el servicio con una sesión de base de datos e instancia el repositorio."""
        self.users_repository = UserRepository(db_session)
        logger.info("Servicio de Usuarios (Seguridad) inicializado")

    def authenticate_user(self, username: str, password: str):
        """
        Verifica las credenciales del usuario.
        Busca el usuario y compara el password proporcionado con el hash almacenado.
        """
        # Se asume que UserRepository tiene un método para buscar por nombre de usuario
        user = self.users_repository.get_user_by_username(username)
        
        logger.info(f"Intentando autenticar usuario: {username}")
        
        # user.password_hash es el campo correcto que definimos en el modelo
        if user and check_password_hash(user.password_hash, password):
            logger.info(f"Usuario autenticado exitosamente: {username}")
            return user
            
        logger.warning(f"Intento de autenticación fallido para: {username}")
        return None

    def get_all_users(self):
        """Recupera todos los usuarios."""
        logger.info("Obteniendo todos los usuarios")
        return self.users_repository.get_all_users()

    def get_user_by_id(self, user_id: int):
        """Busca un usuario por su ID."""
        logger.info(f"Obteniendo usuario por ID: {user_id}")
        return self.users_repository.get_user_by_id(user_id)

    def create_user(self, username: str, password: str, nombre_biciusuario: str):
        """
        Crea un nuevo usuario, hasheando la contraseña antes de guardarla.
        Incluye el campo adicional 'nombre_biciusuario'.
        """
        # 1. Hasheo de la contraseña por seguridad
        password_hashed = generate_password_hash(password)
        
        logger.info(f"Creando usuario: {username} con nombre de perfil: {nombre_biciusuario}")
        
        # 2. Delegamos la creación al repositorio, usando el hash y el campo adicional
        return self.users_repository.create_user(
            username=username, 
            password_hash=password_hashed, # Usamos el hash, no el password en texto plano
            nombre_biciusuario=nombre_biciusuario
        )
        
    def update_user(self, user_id: int, username: str = None, password: str = None, nombre_biciusuario: str = None):
        """
        Actualiza el usuario. Si se proporciona un password, debe ser hasheado.
        Nota: Esto es peligroso en una API real, se recomienda un endpoint aparte para cambiar password.
        """
        password_hash = None
        if password:
            # Si se proporciona una nueva contraseña, la hasheamos
            password_hash = generate_password_hash(password)
            
        logger.info(f"Actualizando usuario: {user_id}")
        
        # Delegamos la actualización al repositorio.
        # Si password_hash es None, el repositorio no debería actualizarlo.
        return self.users_repository.update_user(
            user_id=user_id, 
            username=username, 
            password_hash=password_hash,
            nombre_biciusuario=nombre_biciusuario
        )

    def delete_user(self, user_id: int):
        """Elimina un usuario por su ID."""
        logger.info(f"Eliminando usuario: {user_id}")
        return self.users_repository.delete_user(user_id)