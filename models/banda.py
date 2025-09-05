from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Band(Base):
    __tablename__ = 'bands'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    albums = relationship('Album', back_populates='band', cascade='all, delete-orphan')

class Album(Base):
    __tablename__ = 'albums'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    band_id = Column(Integer, ForeignKey('bands.id'))
    band = relationship('Band', back_populates='albums')