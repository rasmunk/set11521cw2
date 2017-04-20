from ..util.Database import Database
from ..model.Recommendation import Recommendation


class RecommendationService:

    @staticmethod
    def get_recommendations(user):
        recommendations = None
        try:
            recommendations = Database.session.query(Recommendation).filter(Recommendation.user_id == user.id).all()
        except Exception as e:
            print("Failed to retrieve recommendations for: " + user.userId + " ", e)
        finally:
            return recommendations
