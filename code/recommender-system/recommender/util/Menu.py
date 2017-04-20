from ..service.UserService import *
from ..service.MovieService import *
from ..service.RecommendationService import *


class Menu:
    loop = False
    current_user = None

    def initialize(self):
        self.loop = True

    def start(self):
        while self.loop:
            Menu.print_main_menu()
            choice = input("Enter a choice: ")
            if choice == 1:
                if Menu.current_user is None:
                    Menu.current_user = UserService.new_user()
                    Menu.print_register_user()
                else:
                    Menu.current_user = None
            if choice == 2:
                Menu.current_user = UserService.get_random_user()
            if choice == 3:
                Menu.print_select_specific_user()
            if choice == 4:
                Menu.print_rate_movies()
            if choice == 5:
                Menu.print_current_ratings()
            if choice == 6:
                Menu.print_recommendations()
            if choice == 7:
                self.stop()

    def stop(self):
        self.loop = False

    @staticmethod
    def print_register_user():
        print(30 * "-", "NEW USER REGISTERED", 30 * "-")
        print("YOUR ID IS: " + str(Menu.current_user.userId))
        print(67 * "-")

    @staticmethod
    def print_select_specific_user():
        print(30 * "-", "SELECT USER", 30 * "-")
        user_id = input("User Id: ")
        Menu.current_user = UserService.get_user(user_id)

    @staticmethod
    def print_rate_movies():
        print(30 * "-", "MAKE RATING", 30 * "-")
        print("Search for movie")
        title = raw_input("Input Title: ")
        if len(title) > 3:
            movies = MovieService.get_movies_like(title)
            selected_movies = Menu.print_select_movie(movies)
            for movie in selected_movies:
                print(movie.title)
                rating = input("Make a rating between 1.0 & 5.0: ")
                if float(rating) % 0.5 == 0:
                    UserService.apply_rating(Menu.current_user, movie, rating)
                else:
                    print("Not a valid rating " + str(rating) + " rating must be in the 1.0, 1.5, 2.0 format")
        else:
            print("The title should be at least 4 charactors")
        print(67 * "-")

    @staticmethod
    def print_select_movie(movies):
        selected_movies = []
        num_movies = len(movies)
        if num_movies > 0:
            for idx, movie in enumerate(movies):
                if idx % 10 == 0 and idx > 0:
                    choice = raw_input("Continue/Break").lower()
                    if choice == "break":
                        break
                    else:
                        pass
                print("Index: " + str(idx) + " title: " + movie.title)
            while True:
                try:
                    selection = raw_input("Enter a movie index: ")
                    if selection == '':
                        break
                    try:
                        int(selection)
                        selected_movies.append(movies[int(selection)])
                    except IndexError:
                        print("Not a valid index")
                except NameError as e:
                    print("Not an index number")
        else:
            print("No movies found with that title")

        return selected_movies

    @staticmethod
    def print_main_menu():
        print(30 * "-", "MAIN MENU", 30 * "-")
        if Menu.current_user is not None:
            print(30 * "-", "CURRENT USER ID: " + str(Menu.current_user.id), 30 * "-")
            print("1. Logout of User")
        else:
            print("1. Register User")
        print("2. Select Random User")
        print("3. Select Specific User")
        print("4. Make Ratings")
        print("5. Show Ratings")
        print("6. Get Recommendations")
        print("7. Exit")
        print(67 * "-")

    @staticmethod
    def print_movie_options():
        print("Continue. Displays more movies")
        print("")
        print("Exit. Terminates the application")

    @staticmethod
    def print_current_ratings():
        if Menu.current_user is not None:
            print(30 * "-", "RATINGS MADE BY: " + str(Menu.current_user.id), 30 * "-")
            ratings = UserService.get_ratings(Menu.current_user)
            for idx, rating in enumerate(ratings):
                print("Movie: " + rating.movies.title + " Rating: " + str(rating.value))

    @staticmethod
    def print_recommendations():
        print(30 * "-", "RECOMMENDATIONS", 30 * "-")
        movie_recommendations = RecommendationService.get_recommendations(Menu.current_user)
        for idx, movie_recom in enumerate(movie_recommendations):
            print("Estimated rating: " + str(movie_recom.estimated_rating) + " title: " + movie_recom.movies.title)
