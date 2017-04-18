from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from .MovieGenres import association_table
from .Base import Base


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    movieId = Column(Integer)
    title = Column(Text)
    genres = relationship("Genre",
                          secondary=association_table, cascade="save-update, merge, delete")
    ratings = relationship("Rating", backref="movies")
    recommendations = relationship("Recommendation", backref="movies")
