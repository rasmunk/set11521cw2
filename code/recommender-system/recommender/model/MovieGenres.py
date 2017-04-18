from sqlalchemy import Table, Column, Integer, ForeignKey
from.Base import Base

association_table = Table('movies_genres', Base.metadata,
                          Column('movie_id', Integer, ForeignKey('movies.id')),
                          Column('genre_id', Integer, ForeignKey('genres.id'))
                          )
