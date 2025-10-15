import logging
# Configuración básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from flask import Blueprint, jsonify, request
# Importación clave para la autenticación:
from flask_jwt_extended import jwt_required 

# Asegúrate de tener este paquete instalado: pip install Flask-JWT-Extended

# Las importaciones de tu base de datos y servicios
from sqlalchemy.orm import Session
from config.database import get_db # Aquí tu función para obtener sesión de DB
from services.biciusuarios_services import (
    get_all_biciusuarios, get_biciusuario_by_id, create_biciusuario,
    update_biciusuario, delete_biciusuario
)

biciusuario_bp = Blueprint('biciusuario_bp', __name__)


@biciusuario_bp.route('/biciusuarios', methods=['GET'])
@jwt_required() # <-- RUTA PROTEGIDA (Necesita Token)
def get_biciusuarios():
    """Recupera la lista de todos los biciusuarios. Requiere JWT válido."""
    logger.info("Consulta de todos los biciusuarios (acceso autenticado)")
    biciusuarios = get_all_biciusuarios()   
    # Nota: Tu estructura de respuesta parece ser un diccionario, no un objeto SQLAlchemy,
    # por lo que mantengo la serialización original que ya tenías.
    result = [{'id': b['id'], 'nombre_biciusuario': b['nombre_biciusuario']} for b in biciusuarios]
    return jsonify(result), 200


@biciusuario_bp.route('/biciusuarios/<int:biciusuario_id>', methods=['GET'])
# Mantengo esta ruta pública, ya que la consulta por ID a veces no requiere autenticación
def get_biciusuario(biciusuario_id):
    """Recupera un biciusuario por ID (pública o no protegida)"""
    logger.info(f"Consulta de biciusuario por ID: {biciusuario_id}")
    biciusuario = get_biciusuario_by_id(biciusuario_id)
    if biciusuario is None:
        logger.warning(f"Biciusuario no encontrado: {biciusuario_id}")
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify(biciusuario), 200

# Crear
@biciusuario_bp.route('/biciusuarios', methods=['POST'])
@jwt_required() # <-- RUTA PROTEGIDA (Necesita Token)
def create_biciusuario_route():
    """Crea un nuevo biciusuario. Requiere JWT válido."""
    data = request.get_json()
    if not data or 'nombre_biciusuario' not in data:
        logger.warning("Intento de creación sin datos/nombre")
        return jsonify({'error': 'Bad request, nombre_biciusuario es obligatorio'}), 400
    
    biciusuario = create_biciusuario(data)
    logger.info(f"Biciusuario creado: {data.get('nombre_biciusuario')}")
    # Tu servicio devuelve el objeto directamente (asumo que es un dict o serializable)
    return jsonify(biciusuario), 201 

# Actualizar
@biciusuario_bp.route('/biciusuarios/<int:biciusuario_id>', methods=['PUT'])
@jwt_required() # <-- RUTA PROTEGIDA (Necesita Token)
def update_biciusuario_route(biciusuario_id):
    """Actualiza un biciusuario por ID. Requiere JWT válido."""
    data = request.get_json()
    if not data:
        logger.warning(f"Intento de actualización sin datos para ID: {biciusuario_id}")
        return jsonify({'error': 'Bad request'}), 400
    
    biciusuario = update_biciusuario(biciusuario_id, data)
    
    if biciusuario is None:
        logger.warning(f"Biciusuario no encontrado para actualizar: {biciusuario_id}")
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    logger.info(f"Biciusuario actualizado: {biciusuario_id}")
    return jsonify(biciusuario), 200


# Eliminar
@biciusuario_bp.route('/biciusuarios/<int:biciusuario_id>', methods=['DELETE'])
@jwt_required() # <-- RUTA PROTEGIDA (Necesita Token)
def delete_biciusuario_route(biciusuario_id):
    """Elimina un biciusuario por ID. Requiere JWT válido."""
    success = delete_biciusuario(biciusuario_id)
    if not success:
        logger.warning(f"Biciusuario no encontrado para eliminar: {biciusuario_id}")
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    logger.info(f"Biciusuario eliminado: {biciusuario_id}")
    return jsonify({'result': 'Usuario eliminado'}), 200
