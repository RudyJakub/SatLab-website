from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class Gallery(Base):
    __tablename__ = "galleries"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    photo = relationship('Photo', backref = 'gallery')


class Photo(Base):
    __tablename__ = "photos"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    # photo_url


class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    # zdjęcia + inny content
