from src.modules.recommendations.repositories.recommendation_repository import RecommendationRepository
from src.modules.recommendations.dtos.recommendation_dto import RecommendationCreateRequest, RecommendationFeedbackRequest
from src.modules.recommendations.models.recommendation_model import Recommendation, RecommendationFeedback
from typing import List, Optional

class RecommendationController:
    def __init__(self, recommendation_repository: RecommendationRepository):
        self.recommendation_repository = recommendation_repository

    def create_recommendation(self, request: dict) -> Optional[Recommendation]:
        recommendation_dto = RecommendationCreateRequest(**request)

        recommendation = self.recommendation_repository.create_recommendation(
            user_id=recommendation_dto.user_id,
            name="Teste",
            description="Recomendação de teste",
            duration=30.0,
            category="Exercício",
            reasoning="Recomendação gerada para teste",
            precautions="Sem precauções específicas"
        )

        if recommendation is None:
            return None

        return recommendation
    
    def get_all_recommendations_by_user_id(self, user_id: int) -> List[dict]:
        recommendations = self.recommendation_repository.get_all_recommendations_by_user_id(user_id)
        recommendation_list = []

        for recommendation in recommendations:
            recommendation_list.append({
                "name": recommendation.name,
                "description": recommendation.description,
                "duration": recommendation.duration,
                "category": recommendation.category,
                "reasoning": recommendation.reasoning,
                "precautions": recommendation.precautions
            })

        return recommendation_list

    
    def create_recommendation_feedback(self, id: int, request: dict) -> Optional[RecommendationFeedback]:
        recommendation_dto = RecommendationFeedbackRequest(recommendation_id=id, **request)

        feedback = self.recommendation_repository.create_recommendation_feedback(
            recommendation_id=recommendation_dto.recommendation_id,
            rating=recommendation_dto.rating,
            comment=recommendation_dto.comment
        )

        if feedback is None:
            return None

        return feedback
        