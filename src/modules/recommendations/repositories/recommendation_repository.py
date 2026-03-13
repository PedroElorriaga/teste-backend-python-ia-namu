from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.modules.recommendations.models.recommendation_model import Recommendation, RecommendationFeedback
from src.modules.users.models.user_model import User
from typing import List, Optional


class RecommendationRepository:
    def __init__(self, db: Session):
        self.db = db

    def __user_exists(self, user_id: int) -> bool:
        return self.get_user_by_id(user_id) is not None

    def __recommendation_exists(self, recommendation_id: int) -> bool:
        return self.db.query(Recommendation).filter(Recommendation.id == recommendation_id).first() is not None

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        statement = text("SELECT * FROM users WHERE id = :user_id")
        result = self.db.execute(statement, {"user_id": user_id}).fetchone()

        return result

    def create_recommendations(self, user_id: int, activities: list, reasoning: str, precautions: str) -> Optional[bool]:
        if not self.__user_exists(user_id):
            return None

        recommendations_tuple_list = []
        for activity in activities:
            recommendations_tuple_list.append(Recommendation(
                user_id=user_id,
                name=activity["name"],
                description=activity["description"],
                duration=activity["duration"],
                category=activity["category"],
                reasoning=reasoning,
                precautions=precautions,
                created_at=datetime.now(timezone.utc)
            ))

        self.db.add_all(recommendations_tuple_list)
        self.db.commit()

        return True

    def get_all_recommendations_by_user_id(self, user_id: int) -> List[Recommendation]:
        return self.db.query(Recommendation).filter(Recommendation.user_id == user_id).all()

    def create_recommendation_feedback(self, recommendation_id: int, rating: int, comment: str) -> Optional[RecommendationFeedback]:
        if not self.__recommendation_exists(recommendation_id):
            return None

        statement = text("""
            INSERT INTO recommendation_feedbacks (recommendation_id, rating, comment, created_at)
            VALUES (:recommendation_id, :rating, :comment, :created_at)
            RETURNING id, recommendation_id, rating, comment, created_at
        """)
        result = self.db.execute(statement, {
            "recommendation_id": recommendation_id,
            "rating": rating,
            "comment": comment,
            "created_at": datetime.now(timezone.utc),
        }).first()
        self.db.commit()

        print(result)

        if result is None:
            return None

        feedback = RecommendationFeedback(
            id=result.id,
            recommendation_id=result.recommendation_id,
            rating=result.rating,
            comment=result.comment,
            created_at=result.created_at,
        )

        return feedback
