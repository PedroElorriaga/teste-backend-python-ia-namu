import json
import os
from typing import Any

import requests


class OllamaRecommendationService:
    def __init__(self):
        self.ollama_url = (os.getenv("OLLAMA_BASE_URL")
                           or "http://localhost:11434").rstrip("/")
        self.model = os.getenv("OLLAMA_MODEL") or "llama3.2"
        self.timeout = 60

    def __build_messages(self, user_profile: dict[str, Any], additional_info: str | None) -> list[dict[str, str]]:
        user_message = json.dumps(
            {
                "system_message": "Gerar recomendação personalizada de bem-estar.",
                "perfil_usuario": user_profile,
                "additional_info": additional_info or "Não informado",
            },
            ensure_ascii=False,
            indent=2,
        )

        # print(user_message)

        return [
            {"role": "system", "content": (
                "Você é um assistente de bem-estar de nome Namu Assistent. Responda somente com JSON válido, sem markdown, "
                "sem explicações extras e sem texto fora do objeto JSON. "
                "O JSON deve seguir exatamente este formato: "
                '{"activities":[{"name":"string","description":"string","duration":30,"category":"string"}],'
                '"reasoning":"string","precautions":"string"}. '
                "Gere atividades seguras, realistas e adequadas ao perfil informado."
                "Gere ao menos duas atividades, mas não mais do que quatro. "
            )},
            {"role": "user", "content": user_message},
        ]

    def __parse_response(self, content: str) -> dict[str, Any]:
        dict_content = json.loads(content)
        activities = dict_content.get("activities")
        # activities = dict_content['activities']
        # print(activities)

        normalized_activities = []
        for activity in activities:
            if not isinstance(activity, dict):
                continue

            normalized_activities.append(
                {
                    "name": activity.get("name", "atividade sem nome"),
                    "description": activity.get("description", "descrição não fornecida"),
                    "duration": activity.get("duration", 0),
                    "category": activity.get("category", "categoria não fornecida")
                }
            )

        return {
            "activities": normalized_activities,
            "reasoning": dict_content.get("reasoning", "raciocínio não fornecido"),
            "precautions": dict_content.get("precautions", "precauções não fornecidas"),
        }

    def get_recommendations(self, user_profile: dict[str, Any], additional_info: str | None = None) -> dict[str, Any]:
        payload = {
            "model": self.model,
            "stream": False,
            "format": "json",
            "messages": self.__build_messages(user_profile, additional_info),
        }

        response = requests.post(
            f"{self.ollama_url}/api/chat",
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()

        content = response.json()["message"]["content"]
        return self.__parse_response(content)
