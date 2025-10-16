import logging
from sqlalchemy.orm import Session
from models.users_model import User
from models.db import RegistroBiciusuario, Bicicleta
from repositories.users_repository import UserRepository 
# Asegúrate de que UserRepository esté importado correctamente

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BiciusuariosService:
    """
    Capa de servicios para la gestión de perfiles de Biciusuario.
    Esta clase maneja la lógica de negocio para crear, obtener, actualizar
    y eliminar usuarios, incluyendo sus datos anidados (registros y bicicletas).
    Delega las operaciones de base de datos a UserRepository.
    """

    def __init__(self, db_session: Session):
        """Inicializa el servicio con una sesión de base de datos."""
        # Utilizamos el UserRepository ya que la tabla principal es 'users'
        # y la clase User contiene las relaciones con Bicicleta y RegistroBiciusuario.
        self.repository = UserRepository(db_session)
        logger.info("Servicio de Biciusuarios inicializado")

    def _to_dict(self, user: User) -> dict:
        """
        Serializa un objeto User, incluyendo sus relaciones, a un diccionario.
        Esta es la lógica compleja que antes tenías en las funciones.
        """
        if not user:
            return None
            
        # Nota: La password_hash no se expone en el servicio
        return {
            'id': user.id,
            'username': user.username,
            'nombre_biciusuario': user.nombre_biciusuario,
            'registros': [{
                'id': r.id, 
                'nombre_biciusuario': r.nombre_biciusuario,
                'serial': r.serial
            } for r in user.registros],
            'bicicletas': [{
                'id': b.id,
                'marca': b.marca,
                'modelo': b.modelo,
                'color': b.color,
                'serial': b.serial
            } for b in user.bicicletas]
        }

    def listar_biciusuarios(self) -> list[dict]:
        """Recupera todos los perfiles de Biciusuario (User) serializados."""
        logger.info("Listando todos los Biciusuarios")
        users = self.repository.get_all_users()
        return [self._to_dict(user) for user in users]

    def obtener_biciusuario(self, biciusuario_id: int) -> dict | None:
        """Busca y retorna un Biciusuario específico por ID, serializado."""
        logger.info(f"Obteniendo Biciusuario por ID: {biciusuario_id}")
        user = self.repository.get_user_by_id(biciusuario_id)
        return self._to_dict(user)

    def crear_biciusuario(self, data: dict) -> dict | None:
        """
        Crea un nuevo Biciusuario y sus entidades relacionadas (registros, bicicletas).
        Nota: Este método debe ser llamado desde el users_services.py 
        después de hashear la contraseña.
        """
        # Asumiendo que esta función solo crea la información del perfil si 
        # el usuario ya fue creado por UsersService.

        # Este método no se usará directamente para el registro,
        # pero mantenemos la firma si se necesitara:
        
        # En una arquitectura pura, la creación es responsabilidad del UsersService.
        # Solo retornamos None para evitar duplicar lógica de create_user.
        logger.warning("El método crear_biciusuario debe ser llamado a través de UsersService para manejar la seguridad.")
        return None
        
    def actualizar_biciusuario(self, biciusuario_id: int, data: dict) -> dict | None:
        """
        Actualiza el nombre, registros y bicicletas de un Biciusuario.
        """
        logger.info(f"Actualizando Biciusuario: {biciusuario_id}")
        
        # 1. Obtener el usuario
        user = self.repository.get_user_by_id(biciusuario_id)
        if not user:
            logger.warning(f"Biciusuario no encontrado para actualizar: {biciusuario_id}")
            return None

        # 2. Actualizar el nombre principal
        new_name = data.get('nombre_biciusuario', user.nombre_biciusuario)
        if user.nombre_biciusuario != new_name:
            user.nombre_biciusuario = new_name

        # 3. Actualizar Registros (Lógica de negocio compleja)
        if 'registros' in data:
            # Aquí se simplifica la lógica de actualización/creación de Registros
            # Idealmente se haría una lógica más fina para updates, pero por 
            # simplicidad, solo agregamos nuevos si el serial no existe.
            for reg_data in data['registros']:
                # Buscar por serial (asumiendo que es la clave única para registro)
                registro = next((r for r in user.registros if r.serial == reg_data.get('serial')), None)
                if not registro and reg_data.get('serial'):
                    # Crear nuevo registro si no existe
                    new_registro = RegistroBiciusuario(
                        nombre_biciusuario=user.nombre_biciusuario,
                        serial=reg_data['serial'],
                        biciusuario_id=user.id
                    )
                    self.repository.db.add(new_registro)
        
        # 4. Actualizar Bicicletas (Lógica de negocio compleja)
        if 'bicicletas' in data:
            for bici_data in data['bicicletas']:
                # Buscar bicicleta por serial (asumiendo que es la clave única)
                bicicleta = next((b for b in user.bicicletas if b.serial == bici_data.get('serial')), None)
                if bicicleta:
                    # Actualizar si existe
                    bicicleta.marca = bici_data.get('marca', bicicleta.marca)
                    bicicleta.modelo = bici_data.get('modelo', bicicleta.modelo)
                    bicicleta.color = bici_data.get('color', bicicleta.color)
                elif bici_data.get('serial'):
                    # Crear nueva bicicleta si no existe
                    new_bici = Bicicleta(
                        marca=bici_data.get('marca'),
                        modelo=bici_data.get('modelo'),
                        color=bici_data.get('color'),
                        serial=bici_data['serial'],
                        biciusuario_id=user.id
                    )
                    self.repository.db.add(new_bici)

        # 5. Persistir los cambios
        self.repository.db.commit()
        self.repository.db.refresh(user)
        
        return self._to_dict(user)

    def eliminar_biciusuario(self, biciusuario_id: int) -> bool:
        """Elimina un Biciusuario por ID."""
        logger.info(f"Eliminando Biciusuario: {biciusuario_id}")
        deleted_user = self.repository.delete_user(biciusuario_id)
        return deleted_user is not None