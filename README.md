# set11521cw2
Data Wrangling CW2, A Movie Recommendation System
user-based collaborative filtering with pearson correlation similarity.

Docker build support, use the script in code/docker/recommender-system.sh to build 2 containers
  - A MySQL container which holds holds the data (movies, users, ratings)
  - A debian container that runs the recommendation system
  
# TO RUN
On the recommender-system
  - execute "SetupDatabase" to insert the MovieLens dataset into the database.
  - Run "RunRecommendationSystem" to start the recommender
