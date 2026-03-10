from src.modules.users.repositories.user_repository import UserRepository
from src.modules.users.dtos.user_dto import UserCreateRequest


class UserController:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, request: dict):
        user_dto = UserCreateRequest(**request)

        return self.user_repository.create_user(
            name=user_dto.name,
            age=user_dto.age,
            goals=user_dto.goals,
            restrictions=user_dto.restrictions,
            experience_level=user_dto.experience_level
        )
