from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import Mock

from src.modules.recommendations.repositories.recommendation_repository import RecommendationRepository
from src.modules.recommendations.models.recommendation_model import Recommendation, RecommendationFeedback
from src.modules.users.models.user_model import User


class TestRecommendationRepository:
    """Test suite for RecommendationRepository class."""

    def test_get_user_by_id_success(self, fake_db_session):
        """Test fetching user by id returns the user when present."""
        repository = RecommendationRepository(fake_db_session)
        expected_user = Mock(spec=User)
        fake_db_session.execute.return_value.fetchone.return_value = expected_user

        result = repository.get_user_by_id(1)

        assert result == expected_user

    def test_get_user_by_id_not_found(self, fake_db_session):
        """Test fetching user by id returns None when absent."""
        repository = RecommendationRepository(fake_db_session)
        fake_db_session.execute.return_value.fetchone.return_value = None

        result = repository.get_user_by_id(999)

        assert result is None

    # ── create_recommendations ──

    def test_create_recommendations_success(self, fake_db_session):
        """Test successful bulk recommendation creation when user exists."""
        repository = RecommendationRepository(fake_db_session)

        # user exists (get_user_by_id uses raw SQL)
        fake_db_session.execute.return_value.fetchone.return_value = Mock(id=1)

        activities = [
            {"name": "Caminhada", "description": "Caminhada leve de 30 minutos",
                "duration": 30.0, "category": "Cardio"},
        ]

        result = repository.create_recommendations(
            user_id=1,
            activities=activities,
            reasoning="Perfil do usuario",
            precautions="Nenhuma",
        )

        assert result is True
        fake_db_session.add_all.assert_called_once()
        fake_db_session.commit.assert_called_once()

    def test_create_recommendations_user_not_found(self, fake_db_session):
        """Test recommendation creation returns None when user does not exist."""
        repository = RecommendationRepository(fake_db_session)

        fake_db_session.execute.return_value.fetchone.return_value = None

        result = repository.create_recommendations(
            user_id=999,
            activities=[{"name": "Teste", "description": "Desc",
                         "duration": 30.0, "category": "Cat"}],
            reasoning="Reason",
            precautions="Prec",
        )

        assert result is None
        fake_db_session.add_all.assert_not_called()
        fake_db_session.commit.assert_not_called()

    def test_create_recommendations_sets_created_at(self, fake_db_session):
        """Test that created_at is set with timezone-aware datetime."""
        repository = RecommendationRepository(fake_db_session)

        fake_db_session.execute.return_value.fetchone.return_value = Mock(id=1)

        result = repository.create_recommendations(
            user_id=1,
            activities=[{"name": "Yoga", "description": "Yoga leve",
                         "duration": 45.0, "category": "Flexibilidade"}],
            reasoning="Reduz estresse",
            precautions="Nenhuma",
        )

        assert result is True
        args = fake_db_session.add_all.call_args[0][0]
        assert args[0].created_at is not None
        assert args[0].created_at.tzinfo is not None

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
        fake_db_session.query.return_value.filter.return_value.all.return_value = [
            rec1, rec2]

        result = repository.get_all_recommendations_by_user_id(1)

        assert len(result) == 2
        assert result[0].name == "Caminhada"
        assert result[1].name == "Yoga"

    # ── create_recommendation_feedback ──

    def test_create_feedback_success(self, fake_db_session):
        """Test successful feedback creation when recommendation exists."""
        repository = RecommendationRepository(fake_db_session)

        # recommendation exists (__recommendation_exists uses ORM query)
        fake_db_session.query.return_value.filter.return_value.first.return_value = Mock(
            id=1)

        # mock raw SQL insert result
        now = datetime.now(timezone.utc)
        fake_result = SimpleNamespace(
            id=1, recommendation_id=1, rating=4, comment="Muito bom!", created_at=now)
        fake_db_session.execute.return_value.first.return_value = fake_result

        result = repository.create_recommendation_feedback(
            recommendation_id=1,
            rating=4,
            comment="Muito bom!",
        )

        assert result is not None
        assert result.rating == 4
        assert result.comment == "Muito bom!"
        assert result.recommendation_id == 1
        fake_db_session.execute.assert_called()
        fake_db_session.commit.assert_called_once()

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
        fake_db_session.commit.assert_not_called()

    def test_create_feedback_sets_created_at(self, fake_db_session):
        """Test that feedback created_at is set with timezone-aware datetime."""
        repository = RecommendationRepository(fake_db_session)

        fake_db_session.query.return_value.filter.return_value.first.return_value = Mock(
            id=1)

        now = datetime.now(timezone.utc)
        fake_result = SimpleNamespace(
            id=1, recommendation_id=1, rating=5, comment="Excelente!", created_at=now)
        fake_db_session.execute.return_value.first.return_value = fake_result

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

        fake_db_session.query.return_value.filter.return_value.first.return_value = Mock(
            id=1)

        now = datetime.now(timezone.utc)
        fake_result = SimpleNamespace(
            id=1, recommendation_id=1, rating=1, comment="Não gostei", created_at=now)
        fake_db_session.execute.return_value.first.return_value = fake_result

        result = repository.create_recommendation_feedback(
            recommendation_id=1,
            rating=1,
            comment="Não gostei",
        )
        assert result.rating == 1

        fake_db_session.reset_mock()
        fake_db_session.query.return_value.filter.return_value.first.return_value = Mock(
            id=1)

        fake_result2 = SimpleNamespace(
            id=2, recommendation_id=1, rating=5, comment="Perfeito!", created_at=now)
        fake_db_session.execute.return_value.first.return_value = fake_result2

        result = repository.create_recommendation_feedback(
            recommendation_id=1,
            rating=5,
            comment="Perfeito!",
        )
        assert result.rating == 5
