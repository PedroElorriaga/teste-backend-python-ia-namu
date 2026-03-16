from difflib import get_close_matches
import re
import unicodedata
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from src.modules.recommendations.dtos.recommendation_dto import RecommendationHistoryResponse


VALID_EXPERIENCE_LEVELS = {
    "iniciante": "iniciante",
    "intermediario": "intermediário",
    "avancado": "avançado",
}


def normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    without_accents = "".join(
        ch for ch in normalized if not unicodedata.combining(ch))
    return re.sub(r"[^a-z]", "", without_accents.lower())


class UserCreateRequest(BaseModel):
    name: str = Field(..., examples=["Memphis Depay"])
    age: int = Field(..., examples=[28])
    goals: List[str] = Field(..., examples=[
                             ["Perder peso", "Construir massa muscular"]])
    restrictions: Optional[str] = Field(
        None, examples=["Opicional: restrições alimentares, lesões ou outras limitações."])
    experience_level: str = Field(..., examples=[
                                  "iniciante ou intermediário ou avançado"])

    @field_validator("experience_level", mode="before")
    @classmethod
    def validate_and_normalize_experience_level(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("experience_level deve ser uma string.")

        normalized_value = normalize_text(value)

        if normalized_value in VALID_EXPERIENCE_LEVELS:
            return VALID_EXPERIENCE_LEVELS[normalized_value]

        possible_match = get_close_matches(
            normalized_value,
            VALID_EXPERIENCE_LEVELS.keys(),
            n=1,
            cutoff=0.7,
        )
        if possible_match:
            return VALID_EXPERIENCE_LEVELS[possible_match[0]]

        raise ValueError(
            "experience_level inválido. Use: iniciante, intermediário ou avançado."
        )


class UserCreateResponse(BaseModel):
    id: int = Field(..., examples=[1])
    name: str = Field(..., examples=["Memphis Depay"])
    age: int = Field(..., examples=[28])
    goals: List[str] = Field(..., examples=[
                             ["Perder peso", "Construir massa muscular"]])
    restrictions: Optional[str] = Field(..., examples=["Sem laticínios"])
    experience_level: str = Field(..., examples=[
                                  "iniciante ou intermediário ou avançado"])


class UserHistoryRecommendationResponse(BaseModel):
    message: str = Field(..., examples=[
                         "Histórico de recomendações do usuário USER_ID"])
    recommendations: List[RecommendationHistoryResponse]


class UserResponse(BaseModel):
    message: str = Field(..., examples=["Usuario criado"])
    user: UserCreateResponse
