from flask import Blueprint, jsonify, request
from sqlalchemy.orm import Session
from config.database import get_db  # Aquí tu función para obtener sesión de DB
from services.biciusuarios_services import (
    get_all_biciusuarios, get_biciusuario_by_id, create_biciusuario,
    update_biciusuario, delete_biciusuario
)

biciusuario_bp = Blueprint('biciusuario_bp', __name__)


@biciusuario_bp.route('/biciusuarios', methods=['GET'])
def get_biciusuarios():
    biciusuarios = get_all_biciusuarios()   
    result = [{'id': b['id'], 'nombre_biciusuario': b['nombre_biciusuario']} for b in biciusuarios]
    return jsonify(result), 200


@biciusuario_bp.route('/biciusuarios/<int:biciusuario_id>', methods=['GET'])
def get_biciusuario(biciusuario_id):
    biciusuario = get_biciusuario_by_id(biciusuario_id)
    if biciusuario is None:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify(biciusuario), 200

# Crear
@biciusuario_bp.route('/biciusuarios', methods=['POST'])
def create_biciusuario_route():
    if not request.json or 'nombre_biciusuario' not in request.json:
        return jsonify({'error': 'Bad request'}), 400
    biciusuario = create_biciusuario(request.json)
    return jsonify(biciusuario), 201
     #return jsonify({'id': biciusuario.id, 'nombre_biciusuario': biciusuario.nombre_biciusuario}), 201

# Actualizar
@biciusuario_bp.route('/biciusuarios/<int:biciusuario_id>', methods=['PUT'])
def update_biciusuario_route(biciusuario_id):
    if not request.json:
        return jsonify({'error': 'Bad request'}), 400
    biciusuario = update_biciusuario(biciusuario_id, request.json)
    if biciusuario is None:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify(biciusuario), 200

    #return jsonify({'id': biciusuario.id, 'nombre_biciusuario': biciusuario.nombre_biciusuario}), 200


# Eliminar
@biciusuario_bp.route('/biciusuarios/<int:biciusuario_id>', methods=['DELETE'])
def delete_biciusuario_route(biciusuario_id):
    success = delete_biciusuario(biciusuario_id)
    if not success:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify({'result': 'Usuario eliminado'}), 200



