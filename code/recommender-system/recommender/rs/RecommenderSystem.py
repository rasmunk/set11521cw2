from recommender.rs.Recommender import Recommender
from recommender.util.Menu import Menu

class RecommenderSystem:
    recommender = None
    menu = None

    def __init__(self):
        self.recommender = Recommender()
        self.menu = Menu()

    def start_recommender(self):
        self.recommender.start()

    def start_menu(self):
        self.menu.initialize()
        self.menu.start()
