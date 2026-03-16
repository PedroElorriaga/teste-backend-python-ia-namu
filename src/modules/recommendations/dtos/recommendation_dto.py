from pydantic import BaseModel, Field
from typing import Optional


class RecommendationCreateRequest(BaseModel):
    user_id: int = Field(..., examples=[1])
    additional_info: Optional[str] = Field(None, examples=[
                                           "Opicional: informações adicionais sobre o usuário ou preferências específicas."])


class RecommendationFeedbackRequest(BaseModel):
    rating: int = Field(..., ge=1, le=5, examples=[4])
    comment: str = Field(..., examples=["Gostei muito da recomendação!"])


class RecommendationFeedbackResponse(BaseModel):
    message: str = Field(..., examples=["Feedback criado"])
    response: dict = Field(..., examples=[{
        "id": 1,
        "recommendation_id": 1,
        "rating": 4,
        "comment": "Gostei muito da recomendação!"
    }])


class ActivityResponse(BaseModel):
    name: str = Field(..., examples=["Caminhada"])
    description: str = Field(..., examples=["Caminhada leve de 30 minutos"])
    duration: float = Field(..., examples=[30])
    category: str = Field(..., examples=["Cardio"])


class RecommendationCreateResponse(BaseModel):
    activities: list[ActivityResponse]
    reasoning: str = Field(..., examples=[
                           "A atividade foi escolhida pelo perfil do usuario."])
    precautions: str = Field(..., examples=[
                             "Evite impacto por causa das restricoes informadas."])


class RecommendationHistoryResponse(BaseModel):
    id: int = Field(..., examples=[1])
    name: str = Field(..., examples=["Caminhada"])
    description: str = Field(..., examples=["Caminhada leve de 30 minutos"])
    duration: float = Field(..., examples=[30])
    category: str = Field(..., examples=["Cardio"])
    reasoning: str = Field(..., examples=[
                           "A atividade foi escolhida pelo perfil do usuario."])
    precautions: str = Field(..., examples=[
                             "Evite impacto por causa das restricoes informadas."])


class RecommendationResponse(BaseModel):
    message: str = Field(..., examples=["Recomendações geradas com sucesso"])
    response: RecommendationCreateResponse
