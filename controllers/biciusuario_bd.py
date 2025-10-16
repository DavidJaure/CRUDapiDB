import logging
# Configuración básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from flask import Blueprint, jsonify, request
# Importación clave para la autenticación:
from flask_jwt_extended import jwt_required, get_jwt_identity 

# Las importaciones de tu base de datos y servicios
from sqlalchemy.orm import Session
from config.database import get_db_session # Aquí tu función para obtener sesión de DB

# CAMBIO CRÍTICO 1: Importar solo la CLASE del servicio, no las funciones que no existen.
from services.biciusuarios_services import BiciusuariosService 

biciusuario_bp = Blueprint('biciusuario_bp', __name__)

# --- Funciones de Utilidad de Servicio por Petición (Reintroducidas) ---

def get_biciusuarios_service() -> BiciusuariosService:
    """
    Proporciona una instancia de BiciusuariosService con una sesión de DB fresca.
    Esto asegura el manejo correcto de la sesión por cada petición.
    """
    # Usamos 'with' o 'try/finally' si get_db_session() usa un generador
    # Si get_db_session() retorna la sesión directamente, no necesitamos 'with' aquí.
    db_session = get_db_session()
    # Asume que BiciusuariosService.__init__ acepta una sesión
    return BiciusuariosService(db_session)

# --- Rutas CRUD de Perfiles ---

@biciusuario_bp.route('/', methods=['GET']) 
@jwt_required() # <-- RUTA PROTEGIDA
def get_all_biciusuarios_route():
    """GET /biciusuarios - Recupera la lista de todos los biciusuarios."""
    logger.info("Consulta de todos los biciusuarios (acceso autenticado)")
    
    # CAMBIO 2: Obtener la instancia del servicio e invocar el método
    service = get_biciusuarios_service()
    biciusuarios = service.get_all_biciusuarios()   
    
    return jsonify(biciusuarios), 200

@biciusuario_bp.route('/<int:biciusuario_id>', methods=['GET'])
@jwt_required() # Protegemos esta ruta para asegurar que solo usuarios autenticados consulten perfiles
def get_biciusuario_route(biciusuario_id):
    """GET /biciusuarios/<id> - Recupera un biciusuario por ID."""
    
    logger.info(f"Consulta de biciusuario por ID: {biciusuario_id}")
    
    # CAMBIO 2: Obtener la instancia del servicio e invocar el método
    service = get_biciusuarios_service()
    biciusuario = service.get_biciusuario_by_id(biciusuario_id) 
    
    if biciusuario is None:
        logger.warning(f"Biciusuario no encontrado: {biciusuario_id}")
        return jsonify({'error': 'Usuario no encontrado'}), 404
        
    return jsonify(biciusuario), 200

# La ruta POST /biciusuarios es REDUNDANTE, ya que /auth/register maneja la creación inicial del perfil.
# Sin embargo, si quieres mantenerla para crear perfiles detallados por separado:
@biciusuario_bp.route('/', methods=['POST'])
@jwt_required()
def create_biciusuario_route():
    """Crea un nuevo biciusuario (perfil detallado)."""
    data = request.get_json()
    if not data or 'nombre_biciusuario' not in data:
        logger.warning("Intento de creación sin datos/nombre")
        return jsonify({'error': 'Bad request, nombre_biciusuario es obligatorio'}), 400
    
    # CAMBIO 2: Obtener la instancia del servicio e invocar el método
    service = get_biciusuarios_service()
    # NOTA: Debes asegurarte de que tu servicio tiene un método 'create_biciusuario' implementado.
    # Si el registro inicial ya se hace en /auth/register, esta ruta podría ser innecesaria.
    biciusuario = service.create_biciusuario(data) 
    
    logger.info(f"Biciusuario creado: {data.get('nombre_biciusuario')}")
    return jsonify(biciusuario), 201 

@biciusuario_bp.route('/<int:biciusuario_id>', methods=['PUT'])
@jwt_required()
def update_biciusuario_route(biciusuario_id):
    """
    PUT /biciusuarios/<id> - Actualiza un biciusuario y sus sub-recursos.
    CRÍTICO: Solo permite actualizar el propio perfil.
    """
    current_user_id = get_jwt_identity()
    if str(biciusuario_id) != current_user_id:
        logger.warning(f"Intento de actualizar perfil ajeno. Token ID: {current_user_id}, Target ID: {biciusuario_id}")
        return jsonify({'error': 'No tienes permiso para modificar este perfil.'}), 403

    data = request.get_json()
    if not data:
        logger.warning(f"Intento de actualización sin datos para ID: {biciusuario_id}")
        return jsonify({'error': 'Bad request'}), 400
    
    # CAMBIO 2: Obtener la instancia del servicio e invocar el método
    service = get_biciusuarios_service()
    biciusuario = service.update_biciusuario(biciusuario_id, data)
    
    if biciusuario is None:
        logger.warning(f"Biciusuario no encontrado para actualizar: {biciusuario_id}")
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    logger.info(f"Biciusuario actualizado: {biciusuario_id}")
    return jsonify(biciusuario), 200


@biciusuario_bp.route('/<int:biciusuario_id>', methods=['DELETE'])
@jwt_required()
def delete_biciusuario_route(biciusuario_id):
    """
    DELETE /biciusuarios/<id> - Elimina un biciusuario y sus sub-recursos.
    CRÍTICO: Solo permite eliminar el propio perfil.
    """
    current_user_id = get_jwt_identity()
    if str(biciusuario_id) != current_user_id:
        logger.warning(f"Intento de eliminar perfil ajeno. Token ID: {current_user_id}, Target ID: {biciusuario_id}")
        return jsonify({'error': 'No tienes permiso para eliminar este perfil.'}), 403
        
    # CAMBIO 2: Obtener la instancia del servicio e invocar el método
    service = get_biciusuarios_service()
    success = service.delete_biciusuario(biciusuario_id)
    
    if not success:
        logger.warning(f"Biciusuario no encontrado para eliminar: {biciusuario_id}")
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    logger.info(f"Biciusuario eliminado: {biciusuario_id}")
    return jsonify({'result': 'Usuario y datos asociados eliminados correctamente'}), 200
