import logging
from sqlalchemy.orm import Session
# Importaciones de Modelos (Asegúrate de que estas rutas sean correctas)
from models.users_model import User 
from models.users_model import RegistroBiciusuario, Bicicleta 
from repositories.users_repository import UserRepository 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BiciusuariosService:
    """
    Capa de servicios para la gestión de perfiles de Biciusuario (User).
    Maneja la lógica de negocio para obtener, actualizar y eliminar usuarios
    incluyendo sus datos anidados (registros y bicicletas).
    Delega las operaciones de base de datos a UserRepository.
    """

    def __init__(self, db_session: Session):
        """Inicializa el servicio con una sesión de base de datos."""
        self.repository = UserRepository(db_session)
        logger.info("Servicio de Biciusuarios inicializado")

    def _to_dict(self, user: User) -> dict:
        """
        Serializa un objeto User, incluyendo sus relaciones, a un diccionario.
        """
        if not user:
            return None
            
        # Nota: La password_hash NO se expone.
        # Serialización de las relaciones (lista de dicts)
        bicicletas_serializadas = [{
            'id': b.id,
            'marca': b.marca,
            'modelo': b.modelo,
            'color': b.color,
            'serial': b.serial
        } for b in user.bicicletas]
        
        # FIX / RECOMENDACIÓN: Se elimina 'nombre_biciusuario' del registro anidado
        # ya que es redundante, pues ya está en el objeto padre (user).
        registros_serializadas = [{
            'id': r.id, 
            'serial': r.serial
        } for r in user.registros]
        
        return {
            'id': user.id,
            'username': user.username,
            'nombre_biciusuario': user.nombre_biciusuario,
            'bicicletas': bicicletas_serializadas,
            'registros': registros_serializadas
        }

    # --- Métodos Públicos (Usados por el Controlador) ---
    
    def get_all_biciusuarios(self) -> list[dict]:
        """Recupera todos los perfiles de Biciusuario (User) serializados."""
        logger.info("Listando todos los Biciusuarios")
        users = self.repository.get_all_users()
        return [self._to_dict(user) for user in users]

    def get_biciusuario_by_id(self, user_id: int) -> dict | None:
        """Busca y retorna un Biciusuario específico por ID, serializado."""
        logger.info(f"Obteniendo Biciusuario por ID: {user_id}")
        user = self.repository.get_user_by_id(user_id)
        return self._to_dict(user)
        
    def update_biciusuario(self, user_id: int, data: dict) -> dict | None:
        """
        Actualiza el nombre, registros y bicicletas de un Biciusuario.
        """
        logger.info(f"Actualizando Biciusuario: {user_id}")
        
        user = self.repository.get_user_by_id(user_id)
        if not user:
            logger.warning(f"Biciusuario no encontrado para actualizar: {user_id}")
            return None

        # 1. Actualizar el nombre principal
        new_name = data.get('nombre_biciusuario', user.nombre_biciusuario)
        if user.nombre_biciusuario != new_name:
            user.nombre_biciusuario = new_name

        # 2. Actualizar Bicicletas (Upsert: Crea si no existe, actualiza si sí)
        if 'bicicletas' in data:
            current_serials = {b.serial for b in user.bicicletas}
            
            for bici_data in data['bicicletas']:
                serial = bici_data.get('serial')
                if not serial: continue
                
                if serial in current_serials:
                    # Actualizar bicicleta existente
                    bicicleta = next(b for b in user.bicicletas if b.serial == serial)
                    bicicleta.marca = bici_data.get('marca', bicicleta.marca)
                    bicicleta.modelo = bici_data.get('modelo', bicicleta.modelo)
                    bicicleta.color = bici_data.get('color', bicicleta.color)
                else:
                    # Crear nueva bicicleta
                    new_bici = Bicicleta(
                        marca=bici_data.get('marca'),
                        modelo=bici_data.get('modelo'),
                        color=bici_data.get('color'),
                        serial=serial,
                        biciusuario_id=user.id
                    )
                    self.repository.db.add(new_bici)
                    
        # 3. Actualizar Registros (Solo agregamos nuevos si el serial no existe)
        if 'registros' in data:
            current_reg_serials = {r.serial for r in user.registros}
            
            for reg_data in data['registros']:
                serial = reg_data.get('serial')
                if not serial: continue

                if serial not in current_reg_serials:
                    # Crear nuevo registro
                    new_registro = RegistroBiciusuario(
                        nombre_biciusuario=user.nombre_biciusuario,
                        serial=serial,
                        biciusuario_id=user.id
                    )
                    self.repository.db.add(new_registro)

        # 4. Persistir los cambios
        self.repository.db.commit()
        self.repository.db.refresh(user)
        
        return self._to_dict(user)

    def delete_biciusuario(self, user_id: int) -> bool:
        """Elimina un Biciusuario por ID (UserRepository debe manejar las eliminaciones en cascada)."""
        logger.info(f"Eliminando Biciusuario: {user_id}")
        
        # El UserRepository es el responsable de la eliminación en la tabla principal
        deleted_user = self.repository.delete_user(user_id) 
        
        # El método delete_user en el repository debe devolver el usuario eliminado
        # o None si no se encuentra. Asumo que devuelve True/False o el objeto.
        return deleted_user is not None
