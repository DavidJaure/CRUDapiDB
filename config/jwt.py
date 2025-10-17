import os
from datetime import timedelta

# --- Configuración Base para Flask-JWT-Extended ---

# CRUCIAL: La clave secreta se lee directamente del entorno (loaded desde .env en app.py).
# Usamos os.getenv y añadimos un mensaje de error claro como fallback de seguridad.
JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY", 
    "BICI_USUARIOS_CLAVE_53134993.env"
)

# Configuración de ubicación y expiración del Token
JWT_TOKEN_LOCATION = ["headers"]
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30) 

# Configuración del nombre del encabezado HTTP y su tipo
JWT_HEADER_NAME = "Authorization"
JWT_HEADER_TYPE = "Bearer"
 

