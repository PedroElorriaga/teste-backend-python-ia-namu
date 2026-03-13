from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, func
from src.database.postgres_setting import Base


class Recommendation(Base):
    __tablename__ = 'recommendations'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)
    duration = Column(Float, nullable=False)
    category = Column(String(64), nullable=False)
    reasoning = Column(String(255), nullable=False)
    precautions = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


class RecommendationFeedback(Base):
    __tablename__ = 'recommendation_feedbacks'

    id = Column(Integer, primary_key=True)
    recommendation_id = Column(Integer, ForeignKey('recommendations.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)