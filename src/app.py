import logging
from dotenv import load_dotenv
import os # Necesario para usar os.getenv en el futuro

# CRÍTICO: Cargar .env al inicio
load_dotenv() 

from sqlalchemy import create_engine
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS 
# 1. Configuración de la Base de Datos
# Importamos la Base para que SQLAlchemy la conozca y cree las tablas
from models.users_model import Base 

# 2. Configuración de JWT (Importa todas las constantes, AHORA LUEGO DE load_dotenv)
from config.jwt import JWT_SECRET_KEY, JWT_TOKEN_LOCATION, JWT_ACCESS_TOKEN_EXPIRES, JWT_HEADER_NAME, JWT_HEADER_TYPE

# 3. Importación de Controladores (Blueprints)
from controllers.biciusuario_bd import biciusuario_bp 
from controllers.users_controllers import users_bp 
# La importación de config.database la haremos en create_app para evitar problemas de dependencia circular.

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
    
    # Importamos la configuración de la base de datos aquí para evitar problemas de orden
    from config.database import SessionLocal, engine
    app = Flask(__name__)
    
    # Configuramos la DB_URI si fuera necesario, usando el env
    # Nota: Asumo que config/database.py ya usa os.getenv("SQLALCHEMY_DATABASE_URI")
        # ***********************************
    # CRÍTICO: HABILITAR CORS AQUÍ
    CORS(app) 
    # ***********************************
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
# Importamos la función de creación aquí para asegurar que el .env esté cargado
from config.database import create_tables
create_tables()

# 2. Crear la aplicación
app = create_app()

if __name__ == '__main__':
    logger.info("Iniciando servidor Flask...")
    # Puedes cambiar el host o puerto si es necesario
    # NOTA: En un entorno real, usaríamos FLASK_DEBUG=os.getenv("FLASK_DEBUG")
    app.run(debug=True, host='0.0.0.0', port=5200)
