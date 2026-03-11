from src.modules.recommendations.repositories.recommendation_repository import RecommendationRepository
from src.modules.recommendations.dtos.recommendation_dto import RecommendationCreateRequest

class RecommendationController:
    def __init__(self, recommendation_repository: RecommendationRepository):
        self.recommendation_repository = recommendation_repository

    def create_recommendation(self, request: dict) -> dict:
        recommendation_dto = RecommendationCreateRequest(**request)

        return self.recommendation_repository.create_recommendation(
            user_id=recommendation_dto.user_id,
            name="Teste",
            description="Recomendação de teste",
            duration=30.0,
            category="Exercício",
            reasoning="Recomendação gerada para teste",
            precautions="Sem precauções específicas"
        )