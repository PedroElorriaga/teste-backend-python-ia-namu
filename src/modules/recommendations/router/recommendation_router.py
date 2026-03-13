import pydantic_core
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.postgres_setting import get_db
from src.modules.recommendations.dtos.recommendation_dto import RecommendationResponse, RecommendationFeedbackResponse
from src.modules.recommendations.controller.recommendation_controller import RecommendationController
from src.modules.recommendations.repositories.recommendation_repository import RecommendationRepository


router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post(
    "/",
    status_code=201,
    summary="Criar recomendação",
    description="Cria uma nova recomendação personalizada para um usuário específico.",
    response_model=RecommendationResponse,
    responses={
        201: {"description": "Recomendação criada com sucesso"},
        422: {"description": "Erro de validação nos dados de entrada"},
        404: {"description": "Usuário não encontrado"},
    },
)
async def create_recommendations(request: dict, db: Session = Depends(get_db)):
    try:
        recommendation_repository = RecommendationRepository(db)
        recommendation_controller = RecommendationController(
            recommendation_repository)
        recommendation = recommendation_controller.create_recommendations(
            request)

        if recommendation is None:
            raise HTTPException(
                status_code=404, detail="Usuário não encontrado")

        return RecommendationResponse(
            message="Recomendação criada",
            response={
                "activities": recommendation["activities"],
                "reasoning": recommendation["reasoning"],
                "precautions": recommendation["precautions"]
            })
    except pydantic_core.ValidationError:
        raise HTTPException(
            status_code=422, detail="Erro de validação nos dados de entrada")


@router.post("/{id}/feedback",
             status_code=201,
             summary="Criar feedback para recomendação",
             description="Cria um feedback para uma recomendação específica.",
             response_model=RecommendationFeedbackResponse,
             responses={
                 201: {"description": "Feedback criado com sucesso"},
                 404: {"description": "Recomendação não encontrada"},
                 422: {"description": "Erro de validação nos dados de entrada"},
             }
             )
async def create_recommendation_feedback(id: int, request: dict, db: Session = Depends(get_db)):
    try:
        recommendation_repository = RecommendationRepository(db)
        recommendation_controller = RecommendationController(
            recommendation_repository)
        response = recommendation_controller.create_recommendation_feedback(
            id, request)

        if response is None:
            raise HTTPException(
                status_code=404, detail="Recomendação não encontrada")

        return RecommendationFeedbackResponse(
            message="Feedback criado",
            response={
                "id": response.id,
                "recommendation_id": response.recommendation_id,
                "rating": response.rating,
                "comment": response.comment
            }
        )
    except pydantic_core.ValidationError:
        raise HTTPException(
            status_code=422, detail="Erro de validação nos dados de entrada")
