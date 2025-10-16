import sys
import os
from flask import Flask
from flask_jwt_extended import JWTManager

# Ajustar el path de búsqueda para importar módulos de carpetas superiores
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 1. Importaciones de Configuración y Modelos
from config.database import engine
from config.jwt import * # Importa todas las constantes de JWT
from models.users_model import Base # Se asume que Base está definida aquí o en users_model

# 2. Importaciones de Controladores (Blueprints)
from controllers.biciusuario_bd import biciusuario_bp 
from controllers.users_controllers import users_bp # Controlador para /auth/login y /auth/register
# En src/app.py, después de inicializar JWTManager
from controllers.users_controllers import register_jwt_error_handlers
register_jwt_error_handlers(app)

def create_tables():
    """Crea todas las tablas definidas en los modelos de SQLAlchemy si no existen."""
    print("Verificando y creando tablas de base de datos si es necesario...")
    Base.metadata.create_all(bind=engine)
    print("Tablas listas.")

# 3. Inicialización de la Aplicación
app = Flask(__name__)

# --- CONFIGURACIÓN DE SEGURIDAD (JWT) ---
# Se asignan las configuraciones de JWT importadas desde config/jwt.py
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_TOKEN_LOCATION'] = JWT_TOKEN_LOCATION
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES
app.config['JWT_HEADER_NAME'] = JWT_HEADER_NAME
app.config['JWT_HEADER_TYPE'] = JWT_HEADER_TYPE

# Inicializa JWT
jwt = JWTManager(app)
# ----------------------------------------

# 4. Registro de Blueprints
# Asegúrate de registrar AMBOS controladores: el de datos y el de autenticación.
app.register_blueprint(biciusuario_bp, url_prefix='/biciusuarios')
app.register_blueprint(users_bp, url_prefix='/auth') 


# 5. Punto de arranque
if __name__ == '__main__':
    create_tables()
    app.run(debug=True, host='0.0.0.0')

