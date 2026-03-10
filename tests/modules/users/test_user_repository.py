from datetime import datetime
from unittest.mock import Mock

from src.modules.users.repositories.user_repository import UserRepository


class TestUserRepository:
    """Test suite for UserRepository class."""

    def test_create_user_success(self, fake_db_session, valid_user_data):
        """Test successful user creation."""
        repository = UserRepository(fake_db_session)

        def refresh_side_effect(user):
            user.id = 1

        fake_db_session.refresh.side_effect = refresh_side_effect

        user = repository.create_user(
            name=valid_user_data["name"],
            age=valid_user_data["age"],
            goals=valid_user_data["goals"],
            restrictions=valid_user_data["restrictions"],
            experience_level=valid_user_data["experience_level"]
        )

        assert user.id is not None
        assert user.name == valid_user_data["name"]
        assert user.age == valid_user_data["age"]
        assert user.goals == valid_user_data["goals"]
        assert user.restrictions == valid_user_data["restrictions"]
        assert user.experience_level == valid_user_data["experience_level"]
        assert user.created_at is not None
        assert isinstance(user.created_at, datetime)
        fake_db_session.add.assert_called_once_with(user)
        fake_db_session.commit.assert_called_once()
        fake_db_session.refresh.assert_called_once_with(user)

    def test_create_user_with_no_restrictions(self, fake_db_session):
        """Test user creation without restrictions field."""
        repository = UserRepository(fake_db_session)

        fake_db_session.refresh.side_effect = lambda user: setattr(user, "id", 1)

        user = repository.create_user(
            name="Usuario Sem Restricoes",
            age=28,
            goals=["Ganhar massa"],
            experience_level="avançado"
        )

        assert user.restrictions is None
        assert user.name == "Usuario Sem Restricoes"

    def test_get_all_users_empty(self, fake_db_session):
        """Test getting all users from empty database."""
        repository = UserRepository(fake_db_session)
        fake_db_session.query.return_value.all.return_value = []

        users = repository.get_all_users()

        assert users == []
        assert len(users) == 0

    def test_get_all_users_multiple(self, fake_db_session, sample_user):
        """Test getting all users from database with multiple entries."""
        repository = UserRepository(fake_db_session)
        second_user = Mock(
            id=2,
            name="Usuario Iniciante",
            age=25,
            goals=["Melhorar condicionamento"],
            restrictions=None,
            experience_level="iniciante",
        )
        fake_db_session.query.return_value.all.return_value = [sample_user, second_user]

        users = repository.get_all_users()

        assert len(users) == 2
        assert sample_user in users
        assert second_user in users

    def test_create_user_calls_session_methods(self, fake_db_session, valid_user_data):
        """Test that repository uses the SQLAlchemy session correctly."""
        repository = UserRepository(fake_db_session)

        fake_db_session.refresh.side_effect = lambda user: setattr(user, "id", 1)

        user = repository.create_user(**valid_user_data)

        fake_db_session.add.assert_called_once_with(user)
        fake_db_session.commit.assert_called_once()
        fake_db_session.refresh.assert_called_once_with(user)

    def test_create_multiple_users_with_different_levels(self, fake_db_session):
        """Test getting users with different experience levels."""
        repository = UserRepository(fake_db_session)

        levels = ["iniciante", "intermediário", "avançado"]
        users = [
            Mock(experience_level="iniciante"),
            Mock(experience_level="intermediário"),
            Mock(experience_level="avançado"),
        ]
        fake_db_session.query.return_value.all.return_value = users

        all_users = repository.get_all_users()

        assert len(all_users) == 3
        for i, user in enumerate(all_users):
            assert user.experience_level == levels[i]

    def test_user_created_at_is_timezone_aware(self, fake_db_session, valid_user_data):
        """Test that created_at timestamp is timezone aware."""
        repository = UserRepository(fake_db_session)

        fake_db_session.refresh.side_effect = lambda user: setattr(user, "id", 1)

        user = repository.create_user(**valid_user_data)

        assert user.created_at.tzinfo is not None
