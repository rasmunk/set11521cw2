from sqlalchemy import Column, Integer, String
from .Base import Base


class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
