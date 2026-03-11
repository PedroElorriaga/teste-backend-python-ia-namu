from datetime import datetime, timezone
from sqlalchemy.orm import Session
from src.modules.recommendations.models.recommendation_model import Recommendation


class RecommendationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_recommendation(self, user_id: int, name: str, description: str, duration: float, category: str, reasoning: str, precautions: str) -> Recommendation:
        recommendation = Recommendation(user_id=user_id, name=name, description=description, duration=duration,
                                        category=category, reasoning=reasoning, precautions=precautions,
                                        created_at=datetime.now(timezone.utc))
        self.db.add(recommendation)
        self.db.commit()
        self.db.refresh(recommendation)

        return recommendation
    