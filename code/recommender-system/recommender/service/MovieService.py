from ..model import Movie
from ..util.Database import Database


class MovieService:
    @staticmethod
    def get_movies_like(title):
        print("Find title: " + title)
        movies = Database.session.query(Movie).filter(Movie.title.like('%' + title + '%')).all()
        return movies
