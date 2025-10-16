import os
from datetime import timedelta

# Clave secreta para firmar los tokens. 
# ¡IMPORTANTE: Usar variables de entorno en producción!
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'super-clave-secreta-para-biciusuarios-2025')

# Configuración de ubicación y expiración del Token
JWT_TOKEN_LOCATION = ["headers"]
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30) 

# Configuración del nombre del encabezado HTTP y su tipo
JWT_HEADER_NAME = "Authorization"
JWT_HEADER_TYPE = "Bearer"

# Configuración de JWT
#import os
#WT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
# JWT_TOKEN_LOCATION = ["headers"]
# JWT_ACCESS_TOKEN_EXPIRES = 3600
# JWT_HEADER_NAME = "Authorization"
# JWT_HEADER_TYPE = "Bearer"