from sqlalchemy import Boolean, Column, Integer, String, DateTime
from datetime import datetime
from database import Base

"""
class GalleryModel(Base):
    __tablename__ = "galleries"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    photo = relationship('PhotoModel', backref = 'gallery')


class PhotoModel(Base):
    __tablename__ = "photos"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    # photo_url
"""

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    content = Column(String(2000))
    hidden = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    # zdjęcia + inny content
