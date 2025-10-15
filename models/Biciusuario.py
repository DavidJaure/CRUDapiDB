from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

# Clase base declarativa para los modelos
Base = declarative_base()

class User(Base):
    """
    Modelo de Usuario (User) y Biciusuario principal.
    Almacena credenciales de acceso (username y hash de la contraseña) 
    y la información básica del biciusuario.
    """
    __tablename__ = 'users' 

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    # Importante: Cambiamos 'password' a 'password_hash' para clarificar que 
    # almacenamos la contraseña encriptada (hasheada).
    password_hash = Column(String(255), nullable=False) 
    nombre_biciusuario = Column(String(255), nullable=False)

    # Relaciones
    registros = relationship('RegistroBiciusuario', back_populates='biciusuario', cascade='all, delete-orphan')
    bicicletas = relationship('Bicicleta', back_populates='propietario', cascade='all, delete-orphan')


class RegistroBiciusuario(Base):
    """
    Modelo para los registros de biciusuarios. 
    Contiene la relación con el usuario a través de biciusuario_id.
    """
    __tablename__ = 'registro_biciusuarios'

    id = Column(Integer, primary_key=True, index=True)
    nombre_biciusuario = Column(String(255), nullable=False)
    serial = Column(String(50), unique=True)
    biciusuario_id = Column(Integer, ForeignKey('users.id')) # Clave foránea a la tabla 'users'

    biciusuario = relationship('User', back_populates='registros')


class Bicicleta(Base):
    """
    Modelo para las bicicletas registradas, asociadas a un propietario (User).
    """
    __tablename__ = 'bicicletas'

    id = Column(Integer, primary_key=True)
    biciusuario_id = Column(Integer, ForeignKey('users.id')) # Clave foránea a la tabla 'users'
    marca = Column(String(100))
    modelo = Column(String(100))
    color = Column(String(50))
    serial = Column(String(50), unique=True)

    propietario = relationship('User', back_populates='bicicletas')