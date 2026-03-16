from pydantic import BaseModel, Field
from typing import List, Optional
from src.modules.recommendations.dtos.recommendation_dto import RecommendationHistoryResponse


class UserCreateRequest(BaseModel):
    name: str = Field(..., examples=["Memphis Depay"])
    age: int = Field(..., examples=[28])
    goals: List[str] = Field(..., examples=[
                             ["Perder peso", "Construir massa muscular"]])
    restrictions: Optional[str] = Field(
        None, examples=["Opicional: restrições alimentares, lesões ou outras limitações."])
    experience_level: str = Field(..., examples=["Intermediário"])


class UserCreateResponse(BaseModel):
    id: int = Field(..., examples=[1])
    name: str = Field(..., examples=["Memphis Depay"])
    age: int = Field(..., examples=[28])
    goals: List[str] = Field(..., examples=[
                             ["Perder peso", "Construir massa muscular"]])
    restrictions: Optional[str] = Field(..., examples=["Sem laticínios"])
    experience_level: str = Field(..., examples=["Intermediário"])


class UserHistoryRecommendationResponse(BaseModel):
    message: str = Field(..., examples=[
                         "Histórico de recomendações do usuário USER_ID"])
    recommendations: List[RecommendationHistoryResponse]


class UserResponse(BaseModel):
    message: str = Field(..., examples=["Usuario criado"])
    user: UserCreateResponse
