from datetime import datetime, timezone
from sqlalchemy.orm import Session
from src.modules.recommendations.models.recommendation_model import Recommendation, RecommendationFeedback
from src.modules.users.models.user_model import User
from typing import List, Optional


class RecommendationRepository:
    def __init__(self, db: Session):
        self.db = db

    def __user_exists(self, user_id: int) -> bool:
        return self.db.query(User).filter(User.id == user_id).first() is not None

    def __recommendation_exists(self, recommendation_id: int) -> bool:
        return self.db.query(Recommendation).filter(Recommendation.id == recommendation_id).first() is not None

    def create_recommendation(self, user_id: int, name: str, description: str, duration: float, category: str, reasoning: str, precautions: str) -> Optional[Recommendation]:
        if not self.__user_exists(user_id):
            return None
    
        recommendation = Recommendation(user_id=user_id, name=name, description=description, duration=duration,
                                        category=category, reasoning=reasoning, precautions=precautions,
                                        created_at=datetime.now(timezone.utc))
        self.db.add(recommendation)
        self.db.commit()
        self.db.refresh(recommendation)

        return recommendation
    
    def get_all_recommendations_by_user_id(self, user_id: int) -> List[Recommendation]:
        return self.db.query(Recommendation).filter(Recommendation.user_id == user_id).all()

    
    def create_recommendation_feedback(self, recommendation_id: int, rating: int, comment: str) -> Optional[RecommendationFeedback]:
        if not self.__recommendation_exists(recommendation_id):
            return None

        feedback = RecommendationFeedback(recommendation_id=recommendation_id, rating=rating, comment=comment, created_at=datetime.now(timezone.utc))
        self.db.add(feedback)
        self.db.commit()
        self.db.refresh(feedback)

        return feedback