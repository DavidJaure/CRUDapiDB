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

##Endpoint para MIperfil segun el id
@biciusuario_bp.route('/me', methods=['GET'])
@jwt_required()
def get_my_profile():
    """
    GET /biciusuarios/me - Devuelve el perfil del usuario autenticado.
    """
    current_user_id = get_jwt_identity()
    logger.info(f"Consulta de mi perfil. User ID: {current_user_id}")

    service = get_biciusuarios_service()
    biciusuario = service.get_biciusuario_by_id(int(current_user_id))

    if biciusuario is None:
        logger.warning(f"Perfil no encontrado para el usuario {current_user_id}")
        return jsonify({'error': 'Perfil no encontrado'}), 404

    return jsonify(biciusuario), 200


# Agregar estos endpoints al final del archivo controllers/biciusuario_bd.py

@biciusuario_bp.route('/registros/<string:serial>', methods=['DELETE'])
@jwt_required()
def delete_registro_by_serial(serial):
    """
    DELETE /biciusuarios/registros/<serial> - Elimina un registro por serial.
    Solo permite eliminar registros del usuario autenticado.
    """
    current_user_id = get_jwt_identity()
    logger.info(f"Eliminando registro con serial: {serial} para usuario: {current_user_id}")

    service = get_biciusuarios_service()
    
    # Primero obtener el perfil para verificar que el registro pertenece al usuario
    biciusuario = service.get_biciusuario_by_id(int(current_user_id))
    if not biciusuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    # Verificar que el registro existe y pertenece al usuario
    registro = next((reg for reg in biciusuario['registros'] if reg['serial'] == serial), None)
    if not registro:
        return jsonify({'error': 'Registro no encontrado o no pertenece al usuario'}), 404
    
    # Aquí necesitarías agregar un método en el servicio para eliminar por serial
    # Por ahora usaremos una solución temporal
    success = service.delete_registro_by_serial(int(current_user_id), serial)
    
    if success:
        logger.info(f"Registro eliminado: {serial}")
        return jsonify({'result': 'Registro eliminado correctamente'}), 200
    else:
        return jsonify({'error': 'Error al eliminar registro'}), 500

@biciusuario_bp.route('/bicicletas/<string:serial>', methods=['DELETE'])
@jwt_required()
def delete_bicicleta_by_serial(serial):
    """
    DELETE /biciusuarios/bicicletas/<serial> - Elimina una bicicleta por serial.
    Solo permite eliminar bicicletas del usuario autenticado.
    """
    current_user_id = get_jwt_identity()
    logger.info(f"Eliminando bicicleta con serial: {serial} para usuario: {current_user_id}")

    service = get_biciusuarios_service()
    
    # Primero obtener el perfil para verificar que la bicicleta pertenece al usuario
    biciusuario = service.get_biciusuario_by_id(int(current_user_id))
    if not biciusuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    # Verificar que la bicicleta existe y pertenece al usuario
    bicicleta = next((bici for bici in biciusuario['bicicletas'] if bici['serial'] == serial), None)
    if not bicicleta:
        return jsonify({'error': 'Bicicleta no encontrada o no pertenece al usuario'}), 404
    
    # Aquí necesitarías agregar un método en el servicio para eliminar bicicleta por serial
    success = service.delete_bicicleta_by_serial(int(current_user_id), serial)
    
    if success:
        logger.info(f"Bicicleta eliminada: {serial}")
        return jsonify({'result': 'Bicicleta eliminada correctamente'}), 200
    else:
        return jsonify({'error': 'Error al eliminar bicicleta'}), 500