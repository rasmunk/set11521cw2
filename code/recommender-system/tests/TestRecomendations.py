import recommender
import random
import pandas as pd
import numpy as np
import sys
from recommender.model.Rating import Rating
from sklearn.metrics import mean_squared_error


class TestRecommendations:
    user_ratings = []
    training_ratings = []
    test_ratings = []

    def __init__(self):
        recommender.Database.initialize()

    # Extract 60 % of user ratings for training and 40 % for testing
    def test_recommendations(self):
        print("Preparing Recommendation Test")
        self.user_ratings = recommender.Database.session.query(Rating).all()
        num_extract = len(self.user_ratings) * 60 // 100
        indexes = random.sample(xrange(len(self.user_ratings)), num_extract)
        self.training_ratings = [self.user_ratings[i] for i in indexes]
        self.test_ratings = [self.user_ratings[i] for i in xrange(len(self.user_ratings)) if i not in indexes]

        if len(self.training_ratings) != len(indexes):
            print("Training set dosen\'t match the expected number of instances")
            exit(1)

        if len(self.test_ratings) != (len(self.user_ratings) - len(indexes)):
            print("Test set dosen\'t match the expected number of instances")
            exit(1)

        user_test_ratings = {}
        for rating in self.test_ratings:
            user_test_ratings.setdefault(rating.user_id, []).append(
                {'movie_id': rating.movie_id, 'value': rating.value})

        predicted_ratings = pd.DataFrame(columns=['user_id', 'movie_id', 'value', 'timestamp', 'predicted'])
        user_ids = pd.Series([rating.user_id for rating in self.test_ratings])
        movie_ids = pd.Series([rating.movie_id for rating in self.test_ratings])
        actual_values = pd.Series([rating.value for rating in self.test_ratings])
        timestamps = pd.Series([rating.timestamp for rating in self.test_ratings])

        predicted_ratings['user_id'] = user_ids
        predicted_ratings['movie_id'] = movie_ids
        predicted_ratings['value'] = actual_values
        predicted_ratings['timestamp'] = timestamps

        # Remove test data from database
        recommender.Database.session.query(Rating).filter(
            Rating.id.in_([rating.id for rating in self.test_ratings])).delete(synchronize_session=False)
        recommender.Database.session.commit()

        print("Running Recommendation Test")
        recom = recommender.Recommender()
        recom.sim_pearsons()
        recom.recommendations()

        # Calculate number of accurate recommendations
        estimated_rating = 0
        movie_id = 1
        predicted_recommendations = recom.recoms

        print("Parsing recommendations")
        num_rows = len(predicted_recommendations)
        print("num recom " + str(num_rows))
        index = 0

        for user, recoms in predicted_recommendations.iteritems():
            # Recommended movie is in the test set
            for item in recoms:
                if item[movie_id] in predicted_ratings.index and user.userId in predicted_ratings.user_id.values:
                    row_index = predicted_ratings.loc[(predicted_ratings['user_id'] == user.userId) & (
                    predicted_ratings['movie_id'] == item[movie_id])]
                    if row_index.empty is not True:
                        # print("Found match, inserting " + str(row_index))
                        predicted_ratings.set_value(row_index.index[0], 'predicted', item[estimated_rating])

            progress = (float(index) / float(num_rows)) * 100
            sys.stdout.write("Progress: %f%%    \r" % progress)
            sys.stdout.flush()
            index += 1

        print("Inserting TestData")
        list_new_ratings = []
        for index, row in predicted_ratings.iterrows():
            rating = Rating(value=row['value'], timestamp=row['timestamp'], user_id=row['user_id'],
                            movie_id=row['movie_id'])
            list_new_ratings.append(rating)

        print("Number new ratings " + str(len(list_new_ratings)))
        recommender.Database.session.bulk_save_objects(list_new_ratings)
        recommender.Database.session.commit()

        predicted_ratings = predicted_ratings.dropna(how='any')
        rms = np.sqrt(mean_squared_error(predicted_ratings['value'], predicted_ratings['predicted']))
        target = open('results', 'a')
        target.write(str(rms))
        target.write("\n")
        target.close()

        print("Finished Testing")
