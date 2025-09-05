from flask import Blueprint, jsonify, request
from sqlalchemy.orm import Session
from database import get_db  # Aquí tu función para obtener sesión de DB
from biciusuario_service import (
    get_all_biciusuarios, get_biciusuario_by_id, create_biciusuario,
    update_biciusuario, delete_biciusuario
)

biciusuario_bp = Blueprint('biciusuario_bp', __name__)

@biciusuario_bp.route('/biciusuarios', methods=['GET'])
def get_biciusuarios():
    db: Session = get_db()
    biciusuarios = get_all_biciusuarios(db)
    # Serializar datos a JSON (puedes usar Marshmallow o hacer dicts a mano)
    result = [{'id': b.id, 'nombre_biciusuario': b.nombre_biciusuario} for b in biciusuarios]
    return jsonify(result), 200

@biciusuario_bp.route('/biciusuarios/<int:biciusuario_id>', methods=['GET'])
def get_biciusuario(biciusuario_id):
    db: Session = get_db()
    biciusuario = get_biciusuario_by_id(db, biciusuario_id)
    if biciusuario is None:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify({'id': biciusuario.id, 'nombre_biciusuario': biciusuario.nombre_biciusuario}), 200

@biciusuario_bp.route('/biciusuarios', methods=['POST'])
def create_biciusuario_route():
    if not request.json or 'nombre_biciusuario' not in request.json:
        return jsonify({'error': 'Bad request'}), 400
    db: Session = get_db()
    biciusuario = create_biciusuario(db, request.json)
    return jsonify({'id': biciusuario.id, 'nombre_biciusuario': biciusuario.nombre_biciusuario}), 201

@biciusuario_bp.route('/biciusuarios/<int:biciusuario_id>', methods=['PUT'])
def update_biciusuario_route(biciusuario_id):
    if not request.json:
        return jsonify({'error': 'Bad request'}), 400
    db: Session = get_db()
    biciusuario = update_biciusuario(db, biciusuario_id, request.json)
    if biciusuario is None:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify({'id': biciusuario.id, 'nombre_biciusuario': biciusuario.nombre_biciusuario}), 200

@biciusuario_bp.route('/biciusuarios/<int:biciusuario_id>', methods=['DELETE'])
def delete_biciusuario_route(biciusuario_id):
    db: Session = get_db()
    success = delete_biciusuario(db, biciusuario_id)
    if not success:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify({'result': 'Usuario eliminado'}), 200
