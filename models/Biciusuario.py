from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Biciusuario(Base):
    __tablename__ = 'biciusuario'
    id = Column(Integer, primary_key=True, index=True)
    nombre_biciusuario = Column(String(255), nullable=False)

    registros = relationship('RegistroBiciusuario', back_populates='biciusuario', cascade='all, delete-orphan')
    bicicletas = relationship('Bicicleta', back_populates='propietario', cascade='all, delete-orphan')

class RegistroBiciusuario(Base):
    __tablename__ = 'registro_biciusuarios'
    id = Column(Integer, primary_key=True, index=True)
    nombre_biciusuario = Column(String(255), nullable=False)
    biciusuario_id = Column(Integer, ForeignKey('biciusuario.id'))

    biciusuario = relationship('Biciusuario', back_populates='registros')

class Bicicleta(Base):
    __tablename__ = 'bicicletas'
    id = Column(Integer, primary_key=True)
    biciusuario_id = Column(Integer, ForeignKey('biciusuario.id'))
    marca = Column(String(100))
    modelo = Column(String(100))
    color = Column(String(50))
    serial = Column(String(50), unique=True)

    propietario = relationship('Biciusuario', back_populates='bicicletas')
