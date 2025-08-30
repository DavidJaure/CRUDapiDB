import flask import blueprint

bans_bp =blueprint('band_bp',__name__)

@bans_bp.route('/bands', methods=['GET'])

@bans_bp.route('/bands/<int:band_id>', methods=['GET'])

@bans_bp.route('/bands', methods=['POST'])

@bans_bp.route('/bands/<int:band_id>', methods=['PUT'])

@bans_bp.route('/bands/<int:band_id>', methods=['DELETE'])