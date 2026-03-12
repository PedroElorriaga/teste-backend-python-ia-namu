from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import Mock

from src.modules.recommendations.repositories.recommendation_repository import RecommendationRepository
from src.modules.recommendations.models.recommendation_model import Recommendation, RecommendationFeedback
from src.modules.users.models.user_model import User


class TestRecommendationRepository:
    """Test suite for RecommendationRepository class."""

    # ── create_recommendation ──

    def test_create_recommendation_success(self, fake_db_session, sample_recommendation):
        """Test successful recommendation creation when user exists."""
        repository = RecommendationRepository(fake_db_session)

        # user exists
        fake_db_session.query.return_value.filter.return_value.first.return_value = Mock(id=1)

        def refresh_side_effect(rec):
            rec.id = 1

        fake_db_session.refresh.side_effect = refresh_side_effect

        result = repository.create_recommendation(
            user_id=1,
            name="Caminhada",
            description="Caminhada leve de 30 minutos",
            duration=30.0,
            category="Cardio",
            reasoning="Perfil do usuario",
            precautions="Nenhuma",
        )

        assert result is not None
        assert result.name == "Caminhada"
        assert result.duration == 30.0
        assert result.user_id == 1
        fake_db_session.add.assert_called_once()
        fake_db_session.commit.assert_called_once()
        fake_db_session.refresh.assert_called_once()

    def test_create_recommendation_user_not_found(self, fake_db_session):
        """Test recommendation creation returns None when user does not exist."""
        repository = RecommendationRepository(fake_db_session)

        fake_db_session.query.return_value.filter.return_value.first.return_value = None

        result = repository.create_recommendation(
            user_id=999,
            name="Teste",
            description="Desc",
            duration=30.0,
            category="Cat",
            reasoning="Reason",
            precautions="Prec",
        )

        assert result is None
        fake_db_session.add.assert_not_called()
        fake_db_session.commit.assert_not_called()

    def test_create_recommendation_sets_created_at(self, fake_db_session):
        """Test that created_at is set with timezone-aware datetime."""
        repository = RecommendationRepository(fake_db_session)

        fake_db_session.query.return_value.filter.return_value.first.return_value = Mock(id=1)
        fake_db_session.refresh.side_effect = lambda rec: setattr(rec, "id", 1)

        result = repository.create_recommendation(
            user_id=1,
            name="Yoga",
            description="Yoga leve",
            duration=45.0,
            category="Flexibilidade",
            reasoning="Reduz estresse",
            precautions="Nenhuma",
        )

        assert result.created_at is not None
        assert result.created_at.tzinfo is not None

    # ── get_all_recommendations_by_user_id ──

    def test_get_all_recommendations_by_user_id_empty(self, fake_db_session):
        """Test getting recommendations for user with no recommendations."""
        repository = RecommendationRepository(fake_db_session)
        fake_db_session.query.return_value.filter.return_value.all.return_value = []

        result = repository.get_all_recommendations_by_user_id(1)

        assert result == []

    def test_get_all_recommendations_by_user_id_multiple(self, fake_db_session):
        """Test getting multiple recommendations for a user."""
        repository = RecommendationRepository(fake_db_session)

        rec1 = SimpleNamespace(id=1, user_id=1, name="Caminhada")
        rec2 = SimpleNamespace(id=2, user_id=1, name="Yoga")
        fake_db_session.query.return_value.filter.return_value.all.return_value = [rec1, rec2]

        result = repository.get_all_recommendations_by_user_id(1)

        assert len(result) == 2
        assert result[0].name == "Caminhada"
        assert result[1].name == "Yoga"

    # ── create_recommendation_feedback ──

    def test_create_feedback_success(self, fake_db_session):
        """Test successful feedback creation when recommendation exists."""
        repository = RecommendationRepository(fake_db_session)

        # recommendation exists
        fake_db_session.query.return_value.filter.return_value.first.return_value = Mock(id=1)
        fake_db_session.refresh.side_effect = lambda fb: setattr(fb, "id", 1)

        result = repository.create_recommendation_feedback(
            recommendation_id=1,
            rating=4,
            comment="Muito bom!",
        )

        assert result is not None
        assert result.rating == 4
        assert result.comment == "Muito bom!"
        assert result.recommendation_id == 1
        fake_db_session.add.assert_called_once()
        fake_db_session.commit.assert_called_once()
        fake_db_session.refresh.assert_called_once()

    def test_create_feedback_recommendation_not_found(self, fake_db_session):
        """Test feedback creation returns None when recommendation does not exist."""
        repository = RecommendationRepository(fake_db_session)

        fake_db_session.query.return_value.filter.return_value.first.return_value = None

        result = repository.create_recommendation_feedback(
            recommendation_id=999,
            rating=3,
            comment="Razoável",
        )

        assert result is None
        fake_db_session.add.assert_not_called()
        fake_db_session.commit.assert_not_called()

    def test_create_feedback_sets_created_at(self, fake_db_session):
        """Test that feedback created_at is set with timezone-aware datetime."""
        repository = RecommendationRepository(fake_db_session)

        fake_db_session.query.return_value.filter.return_value.first.return_value = Mock(id=1)
        fake_db_session.refresh.side_effect = lambda fb: setattr(fb, "id", 1)

        result = repository.create_recommendation_feedback(
            recommendation_id=1,
            rating=5,
            comment="Excelente!",
        )

        assert result.created_at is not None
        assert result.created_at.tzinfo is not None

    def test_create_feedback_rating_values(self, fake_db_session):
        """Test feedback with boundary rating values."""
        repository = RecommendationRepository(fake_db_session)

        fake_db_session.query.return_value.filter.return_value.first.return_value = Mock(id=1)
        fake_db_session.refresh.side_effect = lambda fb: setattr(fb, "id", 1)

        result = repository.create_recommendation_feedback(
            recommendation_id=1,
            rating=1,
            comment="Não gostei",
        )
        assert result.rating == 1

        fake_db_session.reset_mock()
        fake_db_session.query.return_value.filter.return_value.first.return_value = Mock(id=1)
        fake_db_session.refresh.side_effect = lambda fb: setattr(fb, "id", 2)

        result = repository.create_recommendation_feedback(
            recommendation_id=1,
            rating=5,
            comment="Perfeito!",
        )
        assert result.rating == 5
