from unittest.mock import Mock

import requests

from src.modules.recommendations.services.ollama_recommendation_service import OllamaRecommendationService


class TestOllamaRecommendationService:
    def test_get_recommendations_parses_valid_json_response(self, monkeypatch):
        service = OllamaRecommendationService()
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "message": {
                "content": '{"activities":[{"name":"Caminhada","description":"Caminhada leve de 30 minutos","duration":30,"category":"Cardio"}],"reasoning":"Boa opção para reduzir estresse.","precautions":"Mantenha hidratação."}'
            }
        }

        monkeypatch.setattr(
            "src.modules.recommendations.services.ollama_recommendation_service.requests.post",
            lambda *args, **kwargs: response,
        )

        result = service.get_recommendations(
            user_profile={
                "name": "Ana",
                "age": 28,
                "goals": ["reduzir estresse"],
                "restrictions": "Nenhuma",
                "experience_level": "iniciante",
            },
            additional_info="Dor leve nas costas",
        )

        assert result["activities"][0]["name"] == "Caminhada"
        assert result["activities"][0]["duration"] == 30.0
        assert result["reasoning"] == "Boa opção para reduzir estresse."
        assert result["precautions"] == "Mantenha hidratação."
