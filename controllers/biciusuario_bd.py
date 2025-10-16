import logging
from flask import Blueprint, jsonify, request
# Importaciones cruciales para JWT y para obtener la identidad del usuario
from flask_jwt_extended import jwt_required, get_jwt_identity 

# Importaciones de tu arquitectura
from config.database import get_db_session 
from services.biciusuarios_services import BiciusuariosService # Importar la CLASE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. Definición del Blueprint
biciusuario_bp = Blueprint('biciusuario_bp', __name__)

# --- Funciones de Utilidad de Servicio por Petición ---

def get_biciusuarios_service():
    """
    Proporciona una instancia de BiciusuariosService con una sesión de DB fresca.
    Esto asegura el manejo correcto de la sesión por cada petición.
    """
    db_session = get_db_session()
    # Asume que BiciusuariosService.__init__ acepta una sesión
    return BiciusuariosService(db_session)

# --- Rutas CRUD de Perfiles ---

@biciusuario_bp.route('/', methods=['GET'])
@jwt_required() # <-- RUTA PROTEGIDA (Necesita Token)
def get_all_biciusuarios_route():
    """GET /biciusuarios - Recupera la lista de todos los biciusuarios."""
    logger.info("Consulta de todos los biciusuarios (acceso autenticado)")
    service = get_biciusuarios_service()
    
    # Asume que el servicio devuelve una lista de objetos o diccionarios serializables
    biciusuarios = service.get_all_biciusuarios()
    
    return jsonify(biciusuarios), 200

@biciusuario_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required() # Protegemos esta ruta para asegurar que solo usuarios autenticados consulten perfiles
def get_biciusuario_route(user_id):
    """GET /biciusuarios/<id> - Recupera un biciusuario por ID, incluyendo sus relaciones."""
    logger.info(f"Consulta de biciusuario por ID: {user_id}")
    service = get_biciusuarios_service()
    
    # Asume que este método del servicio ya trae Bicicletas y Registros
    biciusuario = service.get_biciusuario_by_id(user_id) 
    
    if biciusuario is None:
        logger.warning(f"Biciusuario no encontrado: {user_id}")
        return jsonify({'error': 'Usuario no encontrado'}), 404
        
    return jsonify(biciusuario), 200

# La ruta POST /biciusuarios es REDUNDANTE, ya que /auth/register maneja la creación inicial del perfil.
# Solo dejamos GET, PUT, DELETE para la gestión del perfil existente.

@biciusuario_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required() # <-- RUTA PROTEGIDA (Necesita Token)
def update_biciusuario_route(user_id):
    """
    PUT /biciusuarios/<id> - Actualiza un biciusuario y sus sub-recursos (bicicletas/registros).
    Solo permite actualizar el propio perfil.
    """
    # CRÍTICO: AUTORIZACIÓN. Verificar que el token pertenezca al usuario que se intenta modificar.
    current_user_id = get_jwt_identity()
    if str(user_id) != current_user_id:
        logger.warning(f"Intento de actualizar perfil ajeno. Token ID: {current_user_id}, Target ID: {user_id}")
        return jsonify({'error': 'No tienes permiso para modificar este perfil.'}), 403

    data = request.get_json()
    if not data:
        logger.warning(f"Intento de actualización sin datos para ID: {user_id}")
        return jsonify({'error': 'Bad request'}), 400
    
    service = get_biciusuarios_service()
    biciusuario = service.update_biciusuario(user_id, data)
    
    if biciusuario is None:
        logger.warning(f"Biciusuario no encontrado para actualizar: {user_id}")
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    logger.info(f"Biciusuario actualizado: {user_id}")
    return jsonify(biciusuario), 200


@biciusuario_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required() # <-- RUTA PROTEGIDA (Necesita Token)
def delete_biciusuario_route(user_id):
    """
    DELETE /biciusuarios/<id> - Elimina un biciusuario y sus sub-recursos.
    Solo permite eliminar el propio perfil.
    """
    # CRÍTICO: AUTORIZACIÓN. Verificar que el token pertenezca al usuario que se intenta eliminar.
    current_user_id = get_jwt_identity()
    if str(user_id) != current_user_id:
        logger.warning(f"Intento de eliminar perfil ajeno. Token ID: {current_user_id}, Target ID: {user_id}")
        return jsonify({'error': 'No tienes permiso para eliminar este perfil.'}), 403
        
    service = get_biciusuarios_service()
    success = service.delete_biciusuario(user_id)
    
    if not success:
        logger.warning(f"Biciusuario no encontrado para eliminar: {user_id}")
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    logger.info(f"Biciusuario y todos sus datos eliminados: {user_id}")
    return jsonify({'result': 'Usuario y datos asociados eliminados correctamente'}), 200