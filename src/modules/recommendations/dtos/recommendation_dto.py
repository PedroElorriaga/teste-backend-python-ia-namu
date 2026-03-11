from pydantic import BaseModel, Field
from typing import Optional


class RecommendationCreateRequest(BaseModel):
    user_id: int = Field(..., examples=[1])
    additional_info: Optional[str] = Field(None, examples=["Estou com dor de cabeça"])

class RecommendationCreateResponse(BaseModel):
    response: dict = Field(..., examples=[{
        "activities": [{
            "name": "Caminhada",
            "description": "Caminhada leve de 30 minutos",
            "duration": 30,
            "category": "Cardio"
        }],
        "reasoning": "A caminhada leve é uma atividade de baixo impacto que pode ajudar a melhorar a saúde cardiovascular, aumentar a resistência e promover o bem-estar geral. É uma ótima opção para iniciantes ou para aqueles que buscam uma atividade física suave.",
        "precautions": "Certifique-se de usar calçados confortáveis e adequados para caminhada. Mantenha-se hidratado e evite caminhar em condições climáticas extremas. Se sentir dor ou desconforto, pare a atividade e consulte um profissional de saúde."
    }])

class RecommendationResponse(BaseModel):
    message: str = Field(..., examples=["Recomendações geradas com sucesso"])
    response: RecommendationCreateResponse
