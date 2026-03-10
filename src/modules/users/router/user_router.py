from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.postgres_setting import get_db
from src.modules.users.controller.user_controller import UserController
from src.modules.users.dtos.user_dto import UserCreateRequest
from src.modules.users.repositories.user_repository import UserRepository


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def read_users():
    return [{"username": "user1"}, {"username": "user2"}]


@router.post("/", status_code=201, response_model=dict)
async def create_user(request: UserCreateRequest, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    user_controller = UserController(user_repository)
    user = user_controller.create_user(request.model_dump())

    return {
        "message": "Usuario criado",
        "user": {
            "id": user.id,
            "name": user.name,
            "age": user.age,
            "goals": user.goals,
            "restrictions": user.restrictions,
            "experience_level": user.experience_level,
        },
    }
