from flask import Blueprint, jsonify, request
from services.band_service import (
    get_all_bands, get_band_by_id, create_band, update_band, delete_band
)

band_bp = Blueprint('band_bp', __name__)

@band_bp.route('/bands', methods=['GET'])
def get_bands():
    return jsonify(get_all_bands()), 200

@band_bp.route('/bands/<int:band_id>', methods=['GET'])
def get_band(band_id):
    band = get_band_by_id(band_id)
    if band is None:
        return jsonify({'error': 'Band not found'}), 404
    return jsonify(band), 200

@band_bp.route('/bands', methods=['POST'])
def create_band_route():
    if not request.json or 'name' not in request.json or 'albums' not in request.json:
        return jsonify({'error': 'Bad request'}), 400
    band = create_band(request.json)
    return jsonify(band), 201

@band_bp.route('/bands/<int:band_id>', methods=['PUT'])
def update_band_route(band_id):
    if not request.json:
        return jsonify({'error': 'Bad request'}), 400
    band = update_band(band_id, request.json)
    if band is None:
        return jsonify({'error': 'Band not found'}), 404
    return jsonify(band), 200

@band_bp.route('/bands/<int:band_id>', methods=['DELETE'])
def delete_band_route(band_id):
    success = delete_band(band_id)
    if not success:
        return jsonify({'error': 'Band not found'}), 404
    return jsonify({'result': 'Band deleted'}), 200