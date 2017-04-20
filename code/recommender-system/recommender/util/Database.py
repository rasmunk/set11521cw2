import sys
import pandas as pd
from ..model.Genre import Genre
from ..model.Movie import Movie
from ..model.Rating import Rating
from ..model.User import User
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from recommender.model.Base import Base
from recommender.util.Search import binary_search


class Database:
    session = None

    @staticmethod
    def initialize():
        if Database.session is None:
            database_engine = create_engine('mysql+mysqldb://foo:Passw0rd!@172.18.0.2/recommendation')
            database_engine.echo = False

            ## Create model tables
            Base.metadata.create_all(database_engine)

            ## Create session
            session = sessionmaker()
            session.configure(bind=database_engine)
            Database.session = session()

    @staticmethod
    def load_data(file_name):
        data = pd.read_csv(file_name, delimiter=',')
        return data

    @staticmethod
    def setup():
        # http://docs.sqlalchemy.org/en/latest/core/engines.html
        root_path = "/opt/ml-latest-small"
        try:
            # Insert Movies
            print("Inserting Movies")
            file_name = root_path + "/movies.csv"
            data = Database.load_data(file_name)

            num_rows = len(data.values)
            for index, row in data.iterrows():
                list_genres = []
                # Check whether genre's have already been commited to the database
                genres = row['genres'].split('|')
                for genre in genres:
                    genre_object = Database.session.query(Genre).filter(Genre.name == genre).first()
                    if genre_object is None:
                        genre_object = Genre(name=genre)
                        Database.session.add(genre_object)
                        Database.session.commit()
                    list_genres.append(genre_object)

                movie = Movie(movieId=row['movieId'], title=row['title'])
                movie.genres = list_genres
                Database.session.add(movie)
                progress = (float(index) / float(num_rows)) * 100
                sys.stdout.write("Progress: %f%%    \r" % progress)
                sys.stdout.flush()

            Database.session.commit()
            movies = Database.session.query(Movie).all()

            print("Preparing movies for ratings")
            movie_ids = [movie.movieId for movie in movies]
            result = all(movie_ids[i] <= movie_ids[i + 1] for i in xrange(len(movie_ids) - 1))
            if not result:
                print("Movie ids are not sorted")
                exit(1)

            print("Finished inserting movies")
            users = []
            # ## Insert Ratings
            file_name = root_path + "/ratings.csv"
            data = Database.load_data(file_name)
            num_rows = len(data.values)

            print("Preparing Users")
            last_user_id = - 1
            ## Prep ratings insert
            for index, row in data.iterrows():
                ## New User
                if row['userId'] != last_user_id:
                    users.append(User(userId=row['userId']))

                last_user_id = row['userId']
                progress = (float(index) / float(num_rows)) * 100
                sys.stdout.write("Progress: %f%%    \r" % progress)
                sys.stdout.flush()

            Database.session.bulk_save_objects(users)
            Database.session.commit()
            users = Database.session.query(User).all()

            print("Configuring Ratings")
            ratings = []
            for index, row in data.iterrows():
                ## Find user and movie
                user = users[int(row['userId']) - 1]
                if user.userId != row['userId']:
                    print("User index didn't match up")
                    exit(1)

                movie_id = binary_search(movie_ids, int(row['movieId']))
                movie = movies[movie_id]
                if movie.movieId != row['movieId']:
                    print("Movie index didn't match up")
                    exit(1)

                ## Create new rating
                rating = Rating(value=row['rating'], timestamp=row['timestamp'], user_id=user.id, movie_id=movie.id)
                ratings.append(rating)
                progress = (float(index) / float(num_rows)) * 100
                sys.stdout.write("Progress: %f%%    \r" % progress)
                sys.stdout.flush()

            ## Because the move and user objects are queried objects the commit will automatically
            ## add the rating to the ratings table at this point
            Database.session.bulk_save_objects(ratings)
            Database.session.commit()
            print("Finished Database setup")

        except Exception as e:
            print("Unable to insert data", e)
