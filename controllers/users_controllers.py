import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from services.users_services import UsersService
from flask import Blueprint, request, jsonify
# Importaciones cruciales para la autenticación
from flask_jwt_extended import create_access_token, jwt_required
# Importaciones para el manejo de errores de JWT
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask import current_app

# Asume que tu función para obtener la sesión de DB está aquí
from config.database import get_db_session 

# Inicializa el servicio, asumiendo que tu UsersService acepta la sesión
service = UsersService(get_db_session())

user_bp = Blueprint('users', __name__)

# Función para registrar el manejador de errores de JWT en la aplicación principal
# (Esto lo llamaremos luego en tu archivo app.py)
def register_jwt_error_handlers(app):
    """
    Registra un manejador global para el error NoAuthorizationError, 
    que ocurre cuando una ruta @jwt_required() es accedida sin un token válido.
    """
    @app.errorhandler(NoAuthorizationError)
    def handle_no_auth_error(e):
        logger.warning("Intento de acceso sin autenticación JWT")
        return jsonify({'error': 'No autenticado. Debe enviar un token JWT valido en el header Authorization.'}), 401, {'Content-Type': 'application/json; charset=utf-8'}


@user_bp.route('/login', methods=['POST'])
def login():
    """
    POST /login
    Autentica a un usuario y retorna un token JWT si las credenciales son correctas.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        logger.warning("Login fallido: usuario o contrasena no proporcionados")
        return jsonify({'error': 'El nombre de usuario y la contrasena son obligatorios'}), 400, {'Content-Type': 'application/json; charset=utf-8'}
    
    # Llama al servicio que verifica las credenciales (debes asegurarte que tu UsersService.authenticate_user exista)
    user = service.authenticate_user(username, password)
    
    if user:
        # Genera el token de acceso, la identidad se configura con el ID del usuario
        access_token = create_access_token(identity=str(user.id))
        logger.info(f"Usuario autenticado: {username}")
        return jsonify({'access_token': access_token}), 200, {'Content-Type': 'application/json; charset=utf-8'}
    
    logger.warning(f"Login fallido para usuario: {username}")
    return jsonify({'error': 'Credenciales invalidas'}), 401, {'Content-Type': 'application/json; charset=utf-8'}

@user_bp.route('/registry', methods=['POST'])
def create_user():
    """
    POST /registry
    Crea un nuevo usuario (Registro).
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        logger.warning("Registro fallido: usuario o contraseña no proporcionados")
        return jsonify({'error': 'El nombre de usuario y la contraseña son obligatorios'}), 400, {'Content-Type': 'application/json; charset=utf-8'}
    
    # Llama al servicio para crear el usuario (debes asegurarte que tu UsersService.create_user hashee la contraseña)
    user = service.create_user(username, password)
    logger.info(f"Usuario creado: {username}")
    return jsonify({'id': user.id, 'username': user.username}), 201, {'Content-Type': 'application/json; charset=utf-8'}

# Las siguientes rutas de GET, PUT y DELETE requieren un token válido
@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """GET /users - Recupera todos los usuarios (Ruta Protegida)."""
    users = service.get_all_users()
    logger.info("Consulta de todos los usuarios")
    return jsonify([{'id': u.id, 'username': u.username} for u in users]), 200, {'Content-Type': 'application/json; charset=utf-8'}

@user_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """GET /users/<user_id> - Recupera un usuario por ID (Ruta Protegida)."""
    user = service.get_user_by_id(user_id)
    if user:
        logger.info(f"Consulta de usuario por ID: {user_id}")
        return jsonify({'id': user.id, 'username': user.username}), 200, {'Content-Type': 'application/json; charset=utf-8'}
    logger.warning(f"Usuario no encontrado: {user_id}")
    return jsonify({'error': 'Usuario no encontrado'}), 404, {'Content-Type': 'application/json; charset=utf-8'}

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """PUT /users/<user_id> - Actualiza un usuario (Ruta Protegida)."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = service.update_user(user_id, username, password)
    
    if user:
        logger.info(f"Usuario actualizado: {user_id}")
        return jsonify({'id': user.id, 'username': user.username}), 200, {'Content-Type': 'application/json; charset=utf-8'}
    logger.warning(f"Usuario no encontrado para actualizar: {user_id}")
    return jsonify({'error': 'Usuario no encontrado'}), 404, {'Content-Type': 'application/json; charset=utf-8'}

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """DELETE /users/<user_id> - Elimina un usuario (Ruta Protegida)."""
    user = service.delete_user(user_id)
    if user:
        logger.info(f"Usuario eliminado: {user_id}")
        return jsonify({'message': 'Usuario eliminado correctamente'}), 200, {'Content-Type': 'application/json; charset=utf-8'}
    logger.warning(f"Usuario no encontrado para eliminar: {user_id}")
    return jsonify({'error': 'Usuario no encontrado'}), 404, {'Content-Type': 'application/json; charset=utf-8'}
