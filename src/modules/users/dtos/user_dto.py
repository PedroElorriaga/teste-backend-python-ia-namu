from pydantic import BaseModel, Field
from typing import List, Optional


class UserCreateRequest(BaseModel):
    name: str
    age: int
    goals: List[str]
    restrictions: Optional[str] = None
    experience_level: str


class UserCreateResponse(BaseModel):
    id: int = Field(..., examples=[1])
    name: str = Field(..., examples=["Memphis Depay"])
    age: int = Field(..., examples=[28])
    goals: List[str] = Field(..., examples=[
                             ["Perder peso", "Construir massa muscular"]])
    restrictions: Optional[str] = Field(..., examples=["Sem laticínios"])
    experience_level: str = Field(..., examples=["Intermediário"])


class UserResponse(BaseModel):
    message: str = Field(..., examples=["Usuario criado"])
    user: UserCreateResponse
