from pydantic import BaseModel
from typing import List, Optional


class UserCreateRequest(BaseModel):
    name: str
    age: int
    goals: List[str]
    restrictions: Optional[str] = None
    experience_level: str
