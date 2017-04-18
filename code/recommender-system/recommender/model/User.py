from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .Base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    userId = Column(Integer)
    ratings = relationship("Rating", backref="users")
    recommendations = relationship("Recommendation", backref="users")
