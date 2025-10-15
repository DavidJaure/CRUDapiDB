import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from sqlalchemy.orm import Session
# Importamos los modelos de tu API
from models.db import RegistroBiciusuario 

class RegistroBiciusuarioRepository:
    """
    Repositorio para la gestión de los registros de biciusuarios en la base de datos.
    Implementa los métodos básicos CRUD para la entidad RegistroBiciusuario.
    """

    def __init__(self, db_session: Session):
        """Inicializa el repositorio con la sesión de base de datos."""
        self.db = db_session

    def get_all_registros(self):
        """Recupera todos los registros de biciusuarios."""
        logger.info("Obteniendo todos los registros de biciusuarios desde el repositorio")
        return self.db.query(RegistroBiciusuario).all()

    def get_registro_by_id(self, registro_id: int):
        """Busca y retorna un registro específico por su ID."""
        logger.info(f"Buscando registro por ID: {registro_id}")
        return self.db.query(RegistroBiciusuario).filter(RegistroBiciusuario.id == registro_id).first()
    
    def create_registro(self, data: dict):
        """
        Crea y almacena un nuevo registro de biciusuario.
        Se espera que 'data' contenga los campos necesarios.
        """
        logger.info(f"Creando nuevo registro para: {data.get('nombre_biciusuario')}")
        
        # Asumimos que los datos del diccionario 'data' coinciden con los campos del modelo
        new_registro = RegistroBiciusuario(
            nombre_biciusuario=data.get('nombre_biciusuario'),
            serial=data.get('serial'),
            biciusuario_id=data.get('biciusuario_id')
        )
        
        self.db.add(new_registro)
        self.db.commit()
        self.db.refresh(new_registro)
        return new_registro

    def update_registro(self, registro_id: int, data: dict):
        """
        Actualiza la información de un registro existente.
        """
        registro = self.get_registro_by_id(registro_id)
        if registro:
            logger.info(f"Actualizando registro ID: {registro_id}")
            
            # Actualiza solo los campos presentes en el diccionario 'data'
            if 'nombre_biciusuario' in data:
                registro.nombre_biciusuario = data['nombre_biciusuario']
            if 'serial' in data:
                registro.serial = data['serial']
            if 'biciusuario_id' in data:
                registro.biciusuario_id = data['biciusuario_id']

            self.db.commit()
            self.db.refresh(registro)
        else:
            logger.warning(f"Registro no encontrado para actualizar: {registro_id}")
        return registro

    def delete_registro(self, registro_id: int):
        """Elimina un registro de la base de datos según su ID."""
        registro = self.get_registro_by_id(registro_id)
        if registro:
            logger.info(f"Eliminando registro: {registro_id}")
            self.db.delete(registro)
            self.db.commit()
        else:
            logger.warning(f"Registro no encontrado para eliminar: {registro_id}")
        return registro
