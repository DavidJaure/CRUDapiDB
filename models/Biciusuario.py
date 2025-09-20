from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'  # Define el nombre de la tabla

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    nombre_biciusuario = Column(String(255), nullable=False)

    # Relaciones
    registros = relationship('RegistroBiciusuario', back_populates='biciusuario', cascade='all, delete-orphan')
    bicicletas = relationship('Bicicleta', back_populates='propietario', cascade='all, delete-orphan')


class RegistroBiciusuario(Base):
    __tablename__ = 'registro_biciusuarios'

    id = Column(Integer, primary_key=True, index=True)
    nombre_biciusuario = Column(String(255), nullable=False)
    serial = Column(String(50), unique=True)
    biciusuario_id = Column(Integer, ForeignKey('users.id'))  # Se relaciona con 'users.id'

    biciusuario = relationship('User', back_populates='registros')


class Bicicleta(Base):
    __tablename__ = 'bicicletas'

    id = Column(Integer, primary_key=True)
    biciusuario_id = Column(Integer, ForeignKey('users.id'))  # Se relaciona con 'users.id'
    marca = Column(String(100))
    modelo = Column(String(100))
    color = Column(String(50))
    serial = Column(String(50), unique=True)

    propietario = relationship('User', back_populates='bicicletas')



#original
#class user():
 #   __tablename__ = 'users'
   # id = Column(Integer,Primary_key=True, inter=True)
  #  username = Column(String(50), unique=True, index=True, nullable=False)
  #  password = Column(String(255), nullable=False)

#class Biciusuario(Base):
 #   __tablename__ = 'biciusuario'
  #  id = Column(Integer, primary_key=True, index=True)
   # nombre_biciusuario = Column(String(255), nullable=False)
    #registros = relationship('RegistroBiciusuario', back_populates='biciusuario', cascade='all, delete-orphan')
    #bicicletas = relationship('Bicicleta', back_populates='propietario', cascade='all, delete-orphan')

