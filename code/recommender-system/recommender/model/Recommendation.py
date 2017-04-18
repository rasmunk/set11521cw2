from sqlalchemy import Column, Integer, Float, ForeignKey
from .Base import Base


class Recommendation(Base):
    __tablename__ = 'recommendations'

    id = Column(Integer, primary_key=True)
    estimated_rating = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_id = Column(Integer, ForeignKey('movies.id'))
