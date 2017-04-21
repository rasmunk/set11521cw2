from ..model import User
from ..model import Movie
from ..model import Rating
from ..util.Database import Database
from sqlalchemy import func
from random import randint
import time


class UserService:
    @staticmethod
    def get_user(user_id):
        user = None
        try:
            user = Database.session.User.query.get(user_id)
        except Exception as e:
            print("Failed to get user: " + str(id), e)
        finally:
            return user

    @staticmethod
    def get_ratings(user):
        ratings = None
        try:
            ratings = Database.session.query(Rating).filter(Rating.user_id == user.id).all()
        except Exception as e:
            print("Failed to get ratings: ", e)
        finally:
            return ratings

    @staticmethod
    def get_all_users():
        users = Database.session.query(User).all()
        return users

    @staticmethod
    def get_random_user():
        num_users = Database.session.query(func.count(User.id)).scalar()
        rand_user_id = randint(0, num_users - 1)
        return Database.session.query(User).filter(User.id == rand_user_id).first()

    @staticmethod
    def new_user():
        last_user_id = Database.session.query(func.max(User.userId)).scalar()
        new_user = User(userId=last_user_id + 1)
        try:
            Database.session.add(new_user)
            Database.session.commit()
            return new_user
        except Exception as e:
            print("Failed to insert new user ", e)

    @staticmethod
    def apply_rating(user, movie, rating):
        current_time = int(time.time())
        try:
            db_user = Database.session.query(User).filter(User.userId == user.userId).first()
            db_movie = Database.session.query(Movie).filter(Movie.movieId == movie.movieId).first()
            new_rating = Rating(value=rating, timestamp=current_time)
            db_user.ratings.append(new_rating)
            db_movie.ratings.append(new_rating)
            Database.session.commit()
            print("New movie rating: " + str(rating) + " For movie: " + str(movie.title))
        except Exception as e:
            print("Failed to apply a new rating", e)
