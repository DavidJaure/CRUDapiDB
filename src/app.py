import logging
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS 
from controllers.biciusuario_bd import biciusuario_bp 
from controllers.users_controllers import users_bp 
from config.database import create_tables
from config.jwt import (
    JWT_SECRET_KEY, JWT_TOKEN_LOCATION, JWT_ACCESS_TOKEN_EXPIRES,
    JWT_HEADER_NAME, JWT_HEADER_TYPE
)


# --- Cargar .env ---
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Configurar JWT ---
def configure_jwt(app):
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
    app.config["JWT_TOKEN_LOCATION"] = JWT_TOKEN_LOCATION
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = JWT_ACCESS_TOKEN_EXPIRES
    app.config["JWT_HEADER_NAME"] = JWT_HEADER_NAME
    app.config["JWT_HEADER_TYPE"] = JWT_HEADER_TYPE
    app.url_map.strict_slashes = False
    JWTManager(app)

def register_jwt_error_handlers(app):
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'msg': 'Token faltante o inválido'}), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'msg': 'Acceso prohibido, permisos insuficientes'}), 403

# --- Crear app ---
def create_app():
    app = Flask(__name__)

    # 💡 Aquí habilitamos CORS para el frontend correcto
    CORS(app, origins=[
        "https://lonely-spooky-cemetery-69gqx5gg6ggp24456-5502.app.github.dev"
    ])

    configure_jwt(app)
    app.register_blueprint(users_bp, url_prefix='/auth')
    app.register_blueprint(biciusuario_bp, url_prefix='/biciusuarios')
    register_jwt_error_handlers(app)

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

# --- Crear tablas y ejecutar ---
create_tables()
app = create_app()

if __name__ == '__main__':
    logger.info("Iniciando servidor Flask...")
    app.run(debug=True, host='0.0.0.0', port=5200)
