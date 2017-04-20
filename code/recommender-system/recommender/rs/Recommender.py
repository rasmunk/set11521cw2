import pandas as pd
import sys
from scipy.stats import pearsonr
from ..model.Recommendation import Recommendation
from ..model.Movie import Movie
from ..model.Rating import Rating
from ..model.User import User
from ..util.Database import Database


class Recommender:
    users_ratings_similarities = None
    users = None
    ratings = None
    movies = None
    recoms = None

    def __init__(self):
        Database.initialize()
        self.users = Database.session.query(User).all()
        self.ratings = Database.session.query(Rating).all()
        self.movies = Database.session.query(Movie).all()
        self.recoms = {}

    # Calculate recommendations for each user
    def start(self):
        self.collaborative_filtering()

    def collaborative_filtering(self):
        self.sim_pearsons()
        self.recommendations()
        self.persist_recommendations()

    # https://books.google.dk/books?id=w84wDgAAQBAJ&pg=PA172&lpg=PA172&dq=sim+pearson+python&source=bl&ots=zR5gRVW8Sh&sig=swdFBvTh8oPaVl_3VfT-eFp_wxw&hl=da&sa=X&ved=0ahUKEwjVyp6TvKbTAhXIBsAKHSsyA_sQ6AEIRDAE#v=onepage&q=sim%20pearson%20python&f=false
    def sim_pearsons(self):
        print("Preparing Similarities")
        df_movies_rated = pd.DataFrame()
        for idx, user_x in enumerate(self.users):
            df_movies_rated[user_x.id] = pd.Series([rating.movie_id for rating in user_x.ratings])

        df_similarities = pd.DataFrame(index=[u.id for u in self.users], columns=[u.id for u in self.users])
        print("Calculating Similarities")
        num_rows = len(self.users)
        for idx, user_x in enumerate(self.users):
            for idy, user_y in enumerate(self.users):
                # Similarity has not been found yet
                if pd.isnull(df_similarities[user_x.id][user_y.id]):
                    # Other user, find shared movie ratings
                    if user_x.id != user_y.id:
                        intersection = pd.Series(
                            list(set(df_movies_rated[user_x.id]) & set(df_movies_rated[user_y.id])))
                        # Users share atleast 5, calc similarity
                        if len(intersection) >= 5:
                            # Convert to integers -> make comparable
                            intersection = map(int, intersection)

                            x_ratings = [rating.value for rating in user_x.ratings if
                                         int(rating.movie_id) in intersection]
                            y_ratings = [rating.value for rating in user_y.ratings if
                                         int(rating.movie_id) in intersection]
                            pearson = pearsonr(x_ratings, y_ratings)
                            df_similarities.set_value(user_x.id, user_y.id, pearson[0])
                            df_similarities.set_value(user_y.id, user_x.id, pearson[0])

            progress = (float(idx) / float(num_rows)) * 100
            sys.stdout.write("Progress: %f%%    \r" % progress)
            sys.stdout.flush()
        self.users_ratings_similarities = df_similarities

    # Programming collective chapter 2
    def recommendations(self):
        print("Finding Movie Recommendations")
        weighted_sum = {}
        similarity_sum = {}
        num_rows = len(self.users)
        for index, user in enumerate(self.users):
            # Remove users that don't share ratings
            df_similar_users = self.users_ratings_similarities[user.id]
            df_similar_users = df_similar_users.dropna()
            user_movies = [rating.movie_id for rating in user.ratings]
            # Other users ratings, positive similarity -> weight what else they have seen
            for idx, sim in df_similar_users.iteritems():
                if sim > 0:
                    target_user = self.users[idx - 1]
                    if target_user.id != idx:
                        print("User id\'s dosen\'t match up, idx: " + str(idx) + " target user: " + str(target_user.id))
                        exit(1)
                    for rating in target_user.ratings:
                        # user has not seen this movie -> calculate score
                        if rating.movie_id not in user_movies:
                            # Similarity and Score
                            weighted_sum.setdefault(rating.movie_id, 0)
                            weighted_sum[rating.movie_id] += (rating.value * sim)
                            ## Sum of similarity of people who rated it
                            similarity_sum.setdefault(rating.movie_id, 0)
                            similarity_sum[rating.movie_id] += sim

            # Normalise -> people who agree with me more, their oppinions matter most
            rankings = [(w_score / similarity_sum[item], item) for item, w_score in weighted_sum.items()]
            rankings.sort()
            rankings.reverse()
            self.recoms[user] = rankings[:100]

            progress = (float(index) / float(num_rows)) * 100
            sys.stdout.write("Progress: %f%%    \r" % progress)
            sys.stdout.flush()

    def persist_recommendations(self):
        print("Saving Recommendations")
        num_rows = len(self.recoms)
        index = 0
        estimated_rating = 0
        movie_id = 1
        recommendations = []
        for user, recoms in self.recoms.iteritems():
            # Persist 20 ratings for each user.
            amount_recoms = 0
            for item in recoms:
                if Database.session.query(Recommendation).filter(Recommendation.user_id == user.id).filter(
                                Recommendation.movie_id == item[movie_id]).first() is None:
                    recom = Recommendation(user_id=user.id, movie_id=item[movie_id],
                                           estimated_rating=item[estimated_rating])
                    recommendations.append(recom)
                    amount_recoms += 1
                    if amount_recoms % 20 == 0:
                        break
            progress = (float(index) / float(num_rows)) * 100
            sys.stdout.write("Progress: %f%%    \r" % progress)
            sys.stdout.flush()
            index += 1

        Database.session.bulk_save_objects(recommendations)
        Database.session.commit()
