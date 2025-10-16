import logging
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required
from flask_jwt_extended.exceptions import NoAuthorizationError

# Importaciones de tu arquitectura
from services.users_services import UsersService
from config.database import get_db_session # Necesitas importar esta función

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. Definición del Blueprint
users_bp = Blueprint('users', __name__)

# --- Funciones de Utilidad de Servicio por Petición ---
def get_user_service():
    """
    Proporciona una instancia de UsersService con una sesión de DB fresca.
    Esto asegura que cada petición HTTP use su propia sesión.
    """
    db_session = get_db_session()
    return UsersService(db_session)

# --- Manejador de Errores JWT ---
def register_jwt_error_handlers(app):
    """
    Registra un manejador global para el error NoAuthorizationError,
    que ocurre cuando una ruta protegida es accedida sin un token válido.
    """
    @app.errorhandler(NoAuthorizationError)
    def handle_no_auth_error(e):
        logger.warning("Intento de acceso a ruta protegida sin autenticación JWT")
        return jsonify({'error': 'No autenticado. Debe enviar un token JWT válido en el encabezado Authorization.'}), 401

# --- Rutas de Autenticación ---

@users_bp.route('/register', methods=['POST'])
def register():
    """
    POST /auth/register
    Crea un nuevo usuario y su perfil de biciusuario.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # CRUCIAL: Capturamos el nombre de perfil para tu API
    nombre_biciusuario = data.get('nombre_biciusuario') 
    
    if not username or not password or not nombre_biciusuario:
        logger.warning("Registro fallido: Faltan campos obligatorios.")
        return jsonify({'error': 'Todos los campos (username, password, nombre_biciusuario) son obligatorios'}), 400
    
    service = get_user_service()
    
    # Llama al servicio que hashea y crea el usuario
    try:
        user = service.create_user(username, password, nombre_biciusuario)
    except Exception as e:
        logger.error(f"Error al crear usuario: {e}")
        # Manejo simple para el caso de username duplicado
        return jsonify({'error': 'No se pudo crear el usuario. El nombre de usuario podría ya existir.'}), 409

    logger.info(f"Usuario y perfil de biciusuario creados: {username}")
    return jsonify({'id': user.id, 'username': user.username, 'nombre_biciusuario': user.nombre_biciusuario}), 201


@users_bp.route('/login', methods=['POST'])
def login():
    """
    POST /auth/login
    Autentica a un usuario y retorna un token JWT si las credenciales son correctas.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        logger.warning("Login fallido: usuario o contraseña no proporcionados")
        return jsonify({'error': 'El nombre de usuario y la contraseña son obligatorios'}), 400
    
    service = get_user_service()
    
    # Llama al servicio que verifica las credenciales
    user = service.authenticate_user(username, password)
    
    if user:
        # Genera el token de acceso, usando el ID del usuario como identidad
        access_token = create_access_token(identity=str(user.id))
        logger.info(f"Usuario autenticado y token generado: {username}")
        return jsonify({'access_token': access_token}), 200
    
    logger.warning(f"Login fallido para usuario: {username}")
    return jsonify({'error': 'Credenciales inválidas'}), 401

# --- Rutas CRUD Protegidas ---

# Las rutas de GET, PUT y DELETE del perfil de usuario
# deben estar protegidas con @jwt_required() y usar get_user_service().

@users_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """GET /auth/users - Recupera todos los usuarios (Ruta Protegida)."""
    service = get_user_service()
    users = service.get_all_users()
    logger.info("Consulta de todos los usuarios")
    # Aseguramos que solo mostramos datos públicos
    return jsonify([{'id': u.id, 'username': u.username, 'nombre_biciusuario': u.nombre_biciusuario} for u in users]), 200

@users_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """GET /auth/users/<user_id> - Recupera un usuario por ID (Ruta Protegida)."""
    service = get_user_service()
    user = service.get_user_by_id(user_id)
    if user:
        logger.info(f"Consulta de usuario por ID: {user_id}")
        return jsonify({'id': user.id, 'username': user.username, 'nombre_biciusuario': user.nombre_biciusuario}), 200
    logger.warning(f"Usuario no encontrado: {user_id}")
    return jsonify({'error': 'Usuario no encontrado'}), 404

@users_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """PUT /auth/users/<user_id> - Actualiza un usuario (Ruta Protegida)."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    nombre_biciusuario = data.get('nombre_biciusuario')
    
    service = get_user_service()
    
    # El servicio se encarga de hashear la contraseña si se proporciona
    user = service.update_user(user_id, username, password, nombre_biciusuario)
    
    if user:
        logger.info(f"Usuario actualizado: {user_id}")
        return jsonify({'id': user.id, 'username': user.username, 'nombre_biciusuario': user.nombre_biciusuario}), 200
    logger.warning(f"Usuario no encontrado para actualizar: {user_id}")
    return jsonify({'error': 'Usuario no encontrado'}), 404

@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """DELETE /auth/users/<user_id> - Elimina un usuario (Ruta Protegida)."""
    service = get_user_service()
    
    user_deleted = service.delete_user(user_id)
    if user_deleted:
        logger.info(f"Usuario eliminado: {user_id}")
        return jsonify({'message': 'Usuario eliminado correctamente'}), 200
    logger.warning(f"Usuario no encontrado para eliminar: {user_id}")
    return jsonify({'error': 'Usuario no encontrado'}), 404