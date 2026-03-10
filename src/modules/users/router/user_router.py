from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.postgres_setting import get_db
from src.modules.users.controller.user_controller import UserController
from src.modules.users.dtos.user_dto import UserCreateRequest, UserCreateResponse, UserResponse
from src.modules.users.repositories.user_repository import UserRepository
from typing import List


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/",
            summary="Listar usuarios",
            description="Retorna uma lista de usuarios com perfil de bem-estar.",
            response_model=List[UserCreateResponse],
            responses={200: {"description": "Lista de usuarios"}})
async def read_users(db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    user_controller = UserController(user_repository)
    users = user_controller.get_all_users()
    return users


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
    user_repository = UserRepository(db)
    user_controller = UserController(user_repository)
    user = user_controller.create_user(request.model_dump())

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
