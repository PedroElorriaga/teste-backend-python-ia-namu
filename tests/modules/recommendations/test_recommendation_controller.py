from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import Mock

from src.modules.recommendations.controller.recommendation_controller import RecommendationController
from src.modules.recommendations.repositories.recommendation_repository import RecommendationRepository


class TestRecommendationController:
    """Test suite for RecommendationController class."""

    # ── create_recommendations ──

    def test_create_recommendations_success(self, valid_recommendation_data, sample_user):
        """Test successful recommendation creation through controller."""
        mock_repository = Mock(spec=RecommendationRepository)
        mock_repository.get_user_by_id.return_value = sample_user
        mock_repository.create_recommendations.return_value = True
        mock_service = Mock()
        expected_payload = {
            "activities": [
                {
                    "name": "Caminhada consciente",
                    "description": "Caminhada leve de 30 minutos com foco na respiração.",
                    "duration": 30.0,
                    "category": "Cardio leve",
                }
            ],
            "reasoning": "Atividade adequada para reduzir estresse sem alto impacto.",
            "precautions": "Respeite seus limites e mantenha hidratação.",
        }
        mock_service.get_recommendations.return_value = expected_payload

        controller = RecommendationController(
            mock_repository, ollama_service=mock_service)
        result = controller.create_recommendations(valid_recommendation_data)

        assert result is not None
        assert result["activities"][0]["name"] == "Caminhada consciente"
        assert result["reasoning"] == "Atividade adequada para reduzir estresse sem alto impacto."
        mock_service.get_recommendations.assert_called_once_with(
            user_profile={
                "id": 1,
                "name": sample_user.name,
                "age": sample_user.age,
                "goals": sample_user.goals,
                "restrictions": sample_user.restrictions,
                "experience_level": sample_user.experience_level,
            },
            additional_info="Estou com dor de cabeça",
        )
        mock_repository.create_recommendations.assert_called_once_with(
            user_id=1,
            activities=expected_payload["activities"],
            reasoning=expected_payload["reasoning"],
            precautions=expected_payload["precautions"],
        )

    def test_create_recommendations_user_not_found(self, valid_recommendation_data):
        """Test recommendation creation returns None when user not found."""
        mock_repository = Mock(spec=RecommendationRepository)
        mock_repository.get_user_by_id.return_value = None
        mock_service = Mock()

        controller = RecommendationController(
            mock_repository, ollama_service=mock_service)
        result = controller.create_recommendations(valid_recommendation_data)

        assert result is None
        mock_service.get_recommendations.assert_not_called()
        mock_repository.create_recommendations.assert_not_called()

    def test_create_recommendations_without_additional_info(self, sample_user):
        """Test recommendation creation without optional additional_info."""
        mock_repository = Mock(spec=RecommendationRepository)
        mock_repository.get_user_by_id.return_value = sample_user
        mock_repository.create_recommendations.return_value = True
        mock_service = Mock()
        expected_payload = {
            "activities": [
                {
                    "name": "Alongamento noturno",
                    "description": "Alongamentos leves para desacelerar o corpo.",
                    "duration": 20.0,
                    "category": "Mobilidade",
                }
            ],
            "reasoning": "Recomendação alinhada ao perfil do usuário.",
            "precautions": "Faça os movimentos sem forçar amplitude.",
        }
        mock_service.get_recommendations.return_value = expected_payload

        controller = RecommendationController(
            mock_repository, ollama_service=mock_service)
        result = controller.create_recommendations({"user_id": 1})

        assert result is not None
        mock_service.get_recommendations.assert_called_once_with(
            user_profile={
                "id": 1,
                "name": sample_user.name,
                "age": sample_user.age,
                "goals": sample_user.goals,
                "restrictions": sample_user.restrictions,
                "experience_level": sample_user.experience_level,
            },
            additional_info=None,
        )
        mock_repository.create_recommendations.assert_called_once()

    # ── get_all_recommendations_by_user_id ──

    def test_get_all_recommendations_by_user_id_success(self):
        """Test getting recommendations returns list of dicts."""
        mock_repository = Mock(spec=RecommendationRepository)
        mock_repository.get_all_recommendations_by_user_id.return_value = [
            SimpleNamespace(
                name="Caminhada", description="Caminhada leve",
                duration=30.0, category="Cardio",
                reasoning="Perfil do usuario", precautions="Nenhuma",
            ),
        ]

        controller = RecommendationController(mock_repository)
        result = controller.get_all_recommendations_by_user_id(1)

        assert len(result) == 1
        assert result[0]["name"] == "Caminhada"
        assert result[0]["duration"] == 30.0
        assert result[0]["category"] == "Cardio"
        assert result[0]["reasoning"] == "Perfil do usuario"
        assert result[0]["precautions"] == "Nenhuma"
        mock_repository.get_all_recommendations_by_user_id.assert_called_once_with(
            1)

    def test_get_all_recommendations_by_user_id_empty(self):
        """Test getting recommendations for user with no recommendations."""
        mock_repository = Mock(spec=RecommendationRepository)
        mock_repository.get_all_recommendations_by_user_id.return_value = []

        controller = RecommendationController(mock_repository)
        result = controller.get_all_recommendations_by_user_id(1)

        assert result == []

    def test_get_all_recommendations_by_user_id_multiple(self):
        """Test getting multiple recommendations returns correct dicts."""
        mock_repository = Mock(spec=RecommendationRepository)
        mock_repository.get_all_recommendations_by_user_id.return_value = [
            SimpleNamespace(
                name="Caminhada", description="Caminhada leve",
                duration=30.0, category="Cardio",
                reasoning="Perfil", precautions="Nenhuma",
            ),
            SimpleNamespace(
                name="Yoga", description="Yoga relaxante",
                duration=45.0, category="Flexibilidade",
                reasoning="Estresse", precautions="Evite posturas avançadas",
            ),
        ]

        controller = RecommendationController(mock_repository)
        result = controller.get_all_recommendations_by_user_id(1)

        assert len(result) == 2
        assert result[0]["name"] == "Caminhada"
        assert result[1]["name"] == "Yoga"

    # ── create_recommendation_feedback ──

    def test_create_feedback_success(self, valid_feedback_data, sample_feedback):
        """Test successful feedback creation through controller."""
        mock_repository = Mock(spec=RecommendationRepository)
        mock_repository.create_recommendation_feedback.return_value = sample_feedback

        controller = RecommendationController(mock_repository)
        result = controller.create_recommendation_feedback(
            1, valid_feedback_data)

        assert result is not None
        assert result.rating == 4
        assert result.comment == "Gostei muito da recomendação!"
        mock_repository.create_recommendation_feedback.assert_called_once_with(
            recommendation_id=1,
            rating=4,
            comment="Gostei muito da recomendação!",
        )

    def test_create_feedback_recommendation_not_found(self, valid_feedback_data):
        """Test feedback creation returns None when recommendation not found."""
        mock_repository = Mock(spec=RecommendationRepository)
        mock_repository.create_recommendation_feedback.return_value = None

        controller = RecommendationController(mock_repository)
        result = controller.create_recommendation_feedback(
            999, valid_feedback_data)

        assert result is None

    def test_controller_initialization(self):
        """Test controller initialization with repository."""
        mock_repository = Mock(spec=RecommendationRepository)
        controller = RecommendationController(mock_repository)
        assert controller.recommendation_repository == mock_repository
