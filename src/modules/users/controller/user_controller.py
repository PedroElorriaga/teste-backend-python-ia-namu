from src.modules.users.repositories.user_repository import UserRepository
from src.modules.users.dtos.user_dto import UserCreateRequest


class UserController:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, request: UserCreateRequest) -> dict:

        if request.restrictions and request.restrictions.strip() == "":
            request.restrictions = None

        return self.user_repository.create_user(
            name=request.name,
            age=request.age,
            goals=request.goals,
            restrictions=request.restrictions,
            experience_level=request.experience_level
        )

    def get_all_users(self) -> dict:
        return self.user_repository.get_all_users()
