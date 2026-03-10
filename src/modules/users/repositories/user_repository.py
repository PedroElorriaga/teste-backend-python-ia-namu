from datetime import datetime, timezone
from sqlalchemy.orm import Session
from src.modules.users.models.user_model import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, name: str, age: int, goals: list, experience_level: str, restrictions: str = None) -> User:
        user = User(name=name, age=age, restrictions=restrictions,
                    experience_level=experience_level, goals=goals,
                    created_at=datetime.now(timezone.utc))
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_all_users(self) -> list[User]:
        return self.db.query(User).all()
