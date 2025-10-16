import logging
from sqlalchemy.orm import Session
from repositories.users_repository import UsersRepository
from models.users_model import User
from typing import Optional
from flask_jwt_extended import create_access_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UsersService:
    """
    Capa de servicios para la gestión de usuarios y la seguridad (autenticación).
    Se encarga de hashear contraseñas, verificar credenciales y delegar el CRUD.
    """
    def __init__(self, db_session: Session):
        """Inicializa el servicio con una sesión de base de datos e instancia el repositorio."""
        # Corregido: Usamos el nombre de clase correcto (UsersRepository)
        self.users_repository = UsersRepository(db_session) 
        logger.info("Servicio de Usuarios (Seguridad) inicializado")

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Verifica las credenciales del usuario.
        Retorna el objeto User si las credenciales son válidas, None en caso contrario.
        """
        user = self.users_repository.get_user_by_username(username)
        
        # 1. Verifica si el usuario existe
        if user is None:
            logger.warning(f"Intento de login fallido: Usuario '{username}' no encontrado.")
            return None
        
        # 2. Verifica la contraseña hasheada
        if user.check_password(password):
            logger.info(f"Login exitoso para usuario: {username}")
            return user
        else:
            logger.warning(f"Intento de login fallido: Contraseña incorrecta para {username}.")
            return None

    def create_user(self, username: str, password: str, nombre_biciusuario: str) -> User:
        """Crea un nuevo usuario, hasheando la contraseña antes de guardarlo."""
        # El modelo User se encarga de hashear la contraseña en su __init__
        new_user = User(username=username, password=password, nombre_biciusuario=nombre_biciusuario)
        
        return self.users_repository.add(new_user)
        
    def generate_access_token(self, user: User) -> str:
        """Genera un token de acceso JWT para un usuario."""
        # Los claims se usan para incluir datos adicionales en el token
        identity = user.id
        # Claim personalizado para el nombre del biciusuario
        additional_claims = {"rs_biciusuario": user.nombre_biciusuario} 

        access_token = create_access_token(
            identity=identity, 
            additional_claims=additional_claims
        )
        return access_token