from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.postgres_setting import get_db
from src.modules.recommendations.dtos.recommendation_dto import RecommendationResponse, RecommendationCreateRequest
from src.modules.recommendations.controller.recommendation_controller import RecommendationController
from src.modules.recommendations.repositories.recommendation_repository import RecommendationRepository


router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post(
    "/",
    status_code=201,
    response_model=RecommendationResponse,
)
async def create_recommendation(request: RecommendationCreateRequest, db: Session = Depends(get_db)):
    recommendation_repository = RecommendationRepository(db)
    recommendation_controller = RecommendationController(recommendation_repository)
    recommendation = recommendation_controller.create_recommendation(request.model_dump())

    return RecommendationResponse(response={
        "activities": [{
            "name": recommendation.name,
            "description": recommendation.description,
            "duration": recommendation.duration,
            "category": recommendation.category
        }],
        "reasoning": recommendation.reasoning,
        "precautions": recommendation.precautions
    })