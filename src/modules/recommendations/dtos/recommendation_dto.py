from pydantic import BaseModel, Field
from typing import Optional


class RecommendationCreateRequest(BaseModel):
    user_id: int = Field(..., examples=[1])
    additional_info: Optional[str] = Field(None, examples=["Estou com dor de cabeça"])


class ActivityResponse(BaseModel):
    name: str = Field(..., examples=["Caminhada"])
    description: str = Field(..., examples=["Caminhada leve de 30 minutos"])
    duration: float = Field(..., examples=[30])
    category: str = Field(..., examples=["Cardio"])


class RecommendationCreateResponse(BaseModel):
    activities: list[ActivityResponse]
    reasoning: str = Field(..., examples=["A atividade foi escolhida pelo perfil do usuario."])
    precautions: str = Field(..., examples=["Evite impacto por causa das restricoes informadas."])


class RecommendationResponse(BaseModel):
    message: str = Field(..., examples=["Recomendações geradas com sucesso"])
    response: RecommendationCreateResponse
