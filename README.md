# set11521cw2
Data Wrangling CW2, A Movie Recommendation System

Docker build support, use the script in code/docker/recommender-system.sh to build 2 containers
  - A MySQL container which holds holds the data (movies, users, ratings)
  - A debian container that runs the recommendation system
  
Note!!, the mysql container has to be running before the recommender-system. i.e. the recommender-system intializes the database content upon boot.
