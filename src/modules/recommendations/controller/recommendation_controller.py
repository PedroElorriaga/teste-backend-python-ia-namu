from src.modules.recommendations.repositories.recommendation_repository import RecommendationRepository
from src.modules.recommendations.dtos.recommendation_dto import RecommendationCreateRequest, RecommendationFeedbackRequest
from src.modules.recommendations.models.recommendation_model import Recommendation, RecommendationFeedback
from src.modules.recommendations.services.ollama_recommendation_service import OllamaRecommendationService
from src.modules.users.models.user_model import User
from typing import List, Optional, Any


class RecommendationController:
    def __init__(self, recommendation_repository: RecommendationRepository, ollama_service: Optional[OllamaRecommendationService] = None):
        self.recommendation_repository = recommendation_repository
        self.ollama_service = ollama_service or OllamaRecommendationService()

    def __build_user_profile(self, user: User) -> dict:
        return {
            "id": user.id,
            "name": user.name,
            "age": user.age,
            "goals": list(user.goals or []),
            "restrictions": user.restrictions,
            "experience_level": user.experience_level,
        }

    def create_recommendations(self, request: dict) -> Optional[dict[str, Any]]:
        recommendation_dto = RecommendationCreateRequest(**request)
        user = self.recommendation_repository.get_user_by_id(
            recommendation_dto.user_id)

        if user is None:
            return None

        recommendation_payload = self.ollama_service.get_recommendations(
            user_profile=self.__build_user_profile(user),
            additional_info=recommendation_dto.additional_info,
        )

        self.recommendation_repository.create_recommendations(
            user_id=recommendation_dto.user_id,
            activities=recommendation_payload["activities"],
            reasoning=recommendation_payload["reasoning"],
            precautions=recommendation_payload["precautions"]
        )

        print(recommendation_payload["activities"])

        return recommendation_payload

    def get_all_recommendations_by_user_id(self, user_id: int) -> List[dict]:
        recommendations = self.recommendation_repository.get_all_recommendations_by_user_id(
            user_id)
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
        recommendation_dto = RecommendationFeedbackRequest(
            recommendation_id=id, **request)

        feedback = self.recommendation_repository.create_recommendation_feedback(
            recommendation_id=recommendation_dto.recommendation_id,
            rating=recommendation_dto.rating,
            comment=recommendation_dto.comment
        )

        if feedback is None:
            return None

        return feedback
