import bcrypt
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

# CRUCIAL: Definición de la Base Declarativa
Base = declarative_base()

# ----------------------------------------------------
# 1. MODELO PRINCIPAL: User
# ----------------------------------------------------

class User(Base):
    """
    Modelo de Usuario (User) y Biciusuario principal.
    Almacena credenciales y la información básica del biciusuario.
    """
    __tablename__ = 'users' 

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False) 
    nombre_biciusuario = Column(String(255), nullable=False)

    # Relaciones. Usamos 'back_populates' para una relación bidireccional más clara.
    # Las referencias son a las CLASES definidas en este mismo archivo.
    registros = relationship(
        'RegistroBiciusuario', 
        back_populates='biciusuario', 
        cascade='all, delete-orphan'
    )
    
    bicicletas = relationship(
        'Bicicleta', 
        back_populates='propietario', 
        cascade='all, delete-orphan'
    )

    def __init__(self, username, password, nombre_biciusuario):
        self.username = username
        self.set_password(password)
        self.nombre_biciusuario = nombre_biciusuario

    def set_password(self, password):
        """Hashea y almacena la contraseña."""
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt()
        ).decode('utf-8')

    def check_password(self, password):
        """Verifica la contraseña hasheada."""
        return bcrypt.checkpw(
            password.encode('utf-8'), self.password_hash.encode('utf-8')
        )
    
    # ... (métodos __repr__)


# ----------------------------------------------------
# 2. MODELO SECUNDARIO: RegistroBiciusuario
# ----------------------------------------------------

class RegistroBiciusuario(Base):
    """Modelo para los registros de biciusuarios."""
    __tablename__ = 'registro_biciusuarios'

    id = Column(Integer, primary_key=True, index=True)
    nombre_biciusuario = Column(String(255), nullable=False)
    serial = Column(String(50), unique=True)
    biciusuario_id = Column(Integer, ForeignKey('users.id')) 

    # Definición de la relación inversa
    biciusuario = relationship('User', back_populates='registros')

    # ... (métodos __repr__)


# ----------------------------------------------------
# 3. MODELO SECUNDARIO: Bicicleta
# ----------------------------------------------------

class Bicicleta(Base):
    """Modelo para las bicicletas registradas."""
    __tablename__ = 'bicicletas'

    id = Column(Integer, primary_key=True)
    biciusuario_id = Column(Integer, ForeignKey('users.id')) 
    marca = Column(String(100))
    modelo = Column(String(100))
    color = Column(String(50))
    serial = Column(String(50), unique=True)

    # Definición de la relación inversa
    propietario = relationship('User', back_populates='bicicletas')
    
    # ... (métodos __repr__)