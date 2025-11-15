import logging
from sqlalchemy.orm import Session
from models.users_model import User, RegistroBiciusuario, Bicicleta
from repositories.users_repository import UsersRepository 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BiciusuariosService:
    def __init__(self, db_session: Session):
        self.repository = UsersRepository(db_session)
        logger.info("Servicio de Biciusuarios inicializado")

    def _to_dict(self, user: User) -> dict:
        if not user:
            return None
            
        bicicletas_serializadas = [{
            'id': b.id,
            'marca': b.marca,
            'modelo': b.modelo,
            'color': b.color,
            'serial': b.serial
        } for b in user.bicicletas]
        
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

    def get_all_biciusuarios(self) -> list[dict]:
        logger.info("Listando todos los Biciusuarios")
        users = self.repository.get_all_users()
        return [self._to_dict(user) for user in users]

    def get_biciusuario_by_id(self, user_id: int) -> dict | None:
        logger.info(f"Obteniendo Biciusuario por ID: {user_id}")
        user = self.repository.get_user_by_id(user_id)
        return self._to_dict(user)
        
    def update_biciusuario(self, user_id: int, data: dict) -> dict | None:
        logger.info(f"Actualizando Biciusuario: {user_id}")
        
        user = self.repository.get_user_by_id(user_id)
        if not user:
            logger.warning(f"Biciusuario no encontrado para actualizar: {user_id}")
            return None

        new_name = data.get('nombre_biciusuario', user.nombre_biciusuario)
        if user.nombre_biciusuario != new_name:
            user.nombre_biciusuario = new_name

        if 'bicicletas' in data:
            current_serials = {b.serial for b in user.bicicletas}
            
            for bici_data in data['bicicletas']:
                serial = bici_data.get('serial')
                if not serial: continue
                
                if serial in current_serials:
                    bicicleta = next(b for b in user.bicicletas if b.serial == serial)
                    bicicleta.marca = bici_data.get('marca', bicicleta.marca)
                    bicicleta.modelo = bici_data.get('modelo', bicicleta.modelo)
                    bicicleta.color = bici_data.get('color', bicicleta.color)
                else:
                    new_bici = Bicicleta(
                        marca=bici_data.get('marca'),
                        modelo=bici_data.get('modelo'),
                        color=bici_data.get('color'),
                        serial=serial,
                        biciusuario_id=user.id
                    )
                    self.repository.db.add(new_bici)
                    
        if 'registros' in data:
            current_reg_serials = {r.serial for r in user.registros}
            
            for reg_data in data['registros']:
                serial = reg_data.get('serial')
                if not serial: continue

                if serial not in current_reg_serials:
                    new_registro = RegistroBiciusuario(
                        nombre_biciusuario=user.nombre_biciusuario,
                        serial=serial,
                        biciusuario_id=user.id
                    )
                    self.repository.db.add(new_registro)

        self.repository.db.commit()
        self.repository.db.refresh(user)
        
        return self._to_dict(user)

    def delete_biciusuario(self, user_id: int) -> bool:
        logger.info(f"Eliminando Biciusuario: {user_id}")
        deleted_user = self.repository.delete_user(user_id) 
        return deleted_user is not None

    def delete_registro_by_serial(self, user_id: int, serial: str) -> bool:
        """Elimina un registro por serial para un usuario específico."""
        logger.info(f"Eliminando registro con serial: {serial} para usuario: {user_id}")
        
        user = self.repository.get_user_by_id(user_id)
        if not user:
            return False
        
        registro = next((reg for reg in user.registros if reg.serial == serial), None)
        if not registro:
            return False
        
        self.repository.db.delete(registro)
        self.repository.db.commit()
        return True

    def delete_bicicleta_by_serial(self, user_id: int, serial: str) -> bool:
        """Elimina una bicicleta por serial para un usuario específico."""
        logger.info(f"Eliminando bicicleta con serial: {serial} para usuario: {user_id}")
        
        user = self.repository.get_user_by_id(user_id)
        if not user:
            return False
        
        bicicleta = next((bici for bici in user.bicicletas if bici.serial == serial), None)
        if not bicicleta:
            return False
        
        self.repository.db.delete(bicicleta)
        self.repository.db.commit()
        return True