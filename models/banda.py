from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Biciusuario(Base):
    __tablename__ = 'biciusuario'
    id = Column(Integer, primary_key=True, index=True)
    nombre_biciusuario = Column(String(255), nullable=False)
    registros = relationship('RegistroBiciusuario', back_populates='biciusuario', cascade='all, delete-orphan')

class RegistroBiciusuario(Base):
    __tablename__ = 'registro_biciusuarios'
    id = Column(Integer, primary_key=True, index=True)
    nombre_biciusuario = Column(String(255), nullable=False)
    biciusuario_id = Column(Integer, ForeignKey('biciusuario.id'))
    serial = Column(String(50))


    biciusuario = relationship('Biciusuario', back_populates='registros')

