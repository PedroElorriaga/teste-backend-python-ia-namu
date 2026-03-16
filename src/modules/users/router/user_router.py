import pydantic_core
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.postgres_setting import get_db
from src.modules.users.controller.user_controller import UserController
from src.modules.users.dtos.user_dto import UserCreateResponse, UserResponse, UserHistoryRecommendationResponse, UserCreateRequest
from src.modules.users.repositories.user_repository import UserRepository
from src.modules.recommendations.controller.recommendation_controller import RecommendationController
from src.modules.recommendations.repositories.recommendation_repository import RecommendationRepository


router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    status_code=201,
    response_model=UserResponse,
    summary="Criar usuario",
    description="Cria um novo usuario com perfil de bem-estar.",
    responses={
        201: {"description": "Usuario criado com sucesso"},
        422: {"description": "Erro de validacao nos dados de entrada"},
    },
)
async def create_user(request: UserCreateRequest, db: Session = Depends(get_db)):
    try:
        user_repository = UserRepository(db)
        user_controller = UserController(user_repository)
        user = user_controller.create_user(
            UserCreateRequest(**request.model_dump()))

        return UserResponse(
            message="Usuario criado",
            user=UserCreateResponse(
                id=user.id,
                name=user.name,
                age=user.age,
                goals=user.goals,
                restrictions=user.restrictions,
                experience_level=user.experience_level
            )
        )
    except pydantic_core.ValidationError:
        raise HTTPException(
            status_code=422, detail="Erro de validação nos dados de entrada")


@router.get("/{user_id}/recommendations",
            status_code=200,
            summary="Obter histórico de recomendações do usuário",
            description="Retorna o histórico de recomendações para um usuário específico.",
            response_model=UserHistoryRecommendationResponse,
            responses={
                200: {"description": "Histórico de recomendações retornado com sucesso"},
                404: {"description": "Usuário não encontrado"},
                422: {"description": "Erro de validação nos dados de entrada"},
            }
            )
async def get_user_history_recommendation(user_id: int, db: Session = Depends(get_db)):
    recommendation_repository = RecommendationRepository(db)
    recommendation_controller = RecommendationController(
        recommendation_repository)
    response = recommendation_controller.get_user_history_recommendations_by_user_id(
        user_id)

    return UserHistoryRecommendationResponse(
        message=f"Histórico de recomendações do usuário {user_id}",
        recommendations=response
    )
