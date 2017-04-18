from sqlalchemy import Column, Integer, Float, ForeignKey
from .Base import Base


class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True)
    value = Column(Float)
    timestamp = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_id = Column(Integer, ForeignKey('movies.id'))
