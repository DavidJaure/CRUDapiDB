import logging
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager

# 1. Configuración de la Base de Datos
from config.database import create_tables, engine, SessionLocal
# Importamos la Base para que SQLAlchemy la conozca y cree las tablas
from models.users_model import Base 

# 2. Configuración de JWT (Importa todas las constantes)
from config.jwt import * # 3. Importación de Controladores (Blueprints)
from controllers.biciusuario_bd import biciusuario_bp 
from controllers.users_controllers import users_bp 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Funciones de Configuración ---

def configure_jwt(app):
    """Configura Flask-JWT-Extended con la aplicación."""
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
    app.config["JWT_TOKEN_LOCATION"] = JWT_TOKEN_LOCATION
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = JWT_ACCESS_TOKEN_EXPIRES
    app.config["JWT_HEADER_NAME"] = JWT_HEADER_NAME
    app.config["JWT_HEADER_TYPE"] = JWT_HEADER_TYPE
    JWTManager(app)

def register_jwt_error_handlers(app):
    """Define manejadores de errores de JWT personalizados."""
    
    @app.errorhandler(401)
    def unauthorized(error):
        # Maneja cualquier 401 que pueda lanzar JWT, asegurando una respuesta JSON
        return jsonify({'msg': 'Token faltante o inválido'}), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'msg': 'Acceso prohibido, permisos insuficientes'}), 403

# --- Creación de la Aplicación ---

def create_app():
    """Crea y configura la instancia de la aplicación Flask."""
    
    # 1. Crear la instancia de Flask
    app = Flask(__name__)

    # 2. Configuración de JWT
    configure_jwt(app)
    
    # 3. Registro de Blueprints
    app.register_blueprint(users_bp, url_prefix='/auth')
    app.register_blueprint(biciusuario_bp, url_prefix='/biciusuarios')

    # 4. Registro de Manejadores de Errores JWT
    register_jwt_error_handlers(app)

    # 5. Ruta de Bienvenida/Estado
    @app.route('/')
    def index():
        return jsonify({
            'message': 'API de Biciusuarios activa',
            'endpoints': {
                'login': '/auth/login',
                'register': '/auth/register',
                'profiles': '/biciusuarios'
            }
        }), 200

    return app

# --- Ejecución y Creación de Tablas ---

# 1. Crear las tablas de la base de datos si no existen
create_tables()

# 2. Crear la aplicación
app = create_app()

if __name__ == '__main__':
    logger.info("Iniciando servidor Flask...")
    # Puedes cambiar el host o puerto si es necesario
    app.run(debug=True, host='0.0.0.0', port=5000)