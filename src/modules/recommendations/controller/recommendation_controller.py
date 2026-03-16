from src.modules.recommendations.repositories.recommendation_repository import RecommendationRepository
from src.modules.recommendations.dtos.recommendation_dto import RecommendationCreateRequest, RecommendationFeedbackRequest
from src.modules.recommendations.models.recommendation_model import RecommendationFeedback
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

    def create_recommendations(self, request: RecommendationCreateRequest) -> Optional[dict[str, Any]]:

        if request.additional_info and request.additional_info.strip() == "":
            request.additional_info = None

        user = self.recommendation_repository.get_user_by_id(
            request.user_id)

        if user is None:
            return None

        recommendation_payload = self.ollama_service.get_recommendations(
            user_profile=self.__build_user_profile(user),
            additional_info=request.additional_info,
        )

        self.recommendation_repository.create_recommendations(
            user_id=request.user_id,
            activities=recommendation_payload["activities"],
            reasoning=recommendation_payload["reasoning"],
            precautions=recommendation_payload["precautions"]
        )

        print(recommendation_payload["activities"])

        return recommendation_payload

    def get_user_history_recommendations_by_user_id(self, user_id: int) -> List[dict]:
        recommendations = self.recommendation_repository.get_user_history_recommendations_by_user_id(
            user_id)
        recommendation_list = []

        for recommendation in recommendations:
            recommendation_list.append({
                "id": recommendation.id,
                "name": recommendation.name,
                "description": recommendation.description,
                "duration": recommendation.duration,
                "category": recommendation.category,
                "reasoning": recommendation.reasoning,
                "precautions": recommendation.precautions
            })

        return recommendation_list

    def create_recommendation_feedback(self, id: int, request: RecommendationFeedbackRequest) -> Optional[RecommendationFeedback]:

        feedback = self.recommendation_repository.create_recommendation_feedback(
            recommendation_id=id,
            rating=request.rating,
            comment=request.comment
        )

        if feedback is None:
            return None

        return feedback
