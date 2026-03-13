import pytest
from unittest.mock import Mock, MagicMock
from src.modules.users.controller.user_controller import UserController
from src.modules.users.repositories.user_repository import UserRepository
from src.modules.users.models.user_model import User
from datetime import datetime, timezone


class TestUserController:
    """Test suite for UserController class."""

    def test_create_user_success(self, valid_user_data):
        """Test successful user creation through controller."""
        mock_repository = Mock(spec=UserRepository)
        mock_user = Mock(spec=User)
        mock_user.id = 1
        mock_user.name = valid_user_data["name"]
        mock_user.age = valid_user_data["age"]
        mock_user.goals = valid_user_data["goals"]
        mock_user.restrictions = valid_user_data["restrictions"]
        mock_user.experience_level = valid_user_data["experience_level"]
        mock_user.created_at = datetime.now(timezone.utc)

        mock_repository.create_user.return_value = mock_user

        controller = UserController(mock_repository)
        result = controller.create_user(valid_user_data)

        assert result.id == 1
        assert result.name == valid_user_data["name"]
        assert result.age == valid_user_data["age"]
        mock_repository.create_user.assert_called_once_with(
            name=valid_user_data["name"],
            age=valid_user_data["age"],
            goals=valid_user_data["goals"],
            restrictions=valid_user_data["restrictions"],
            experience_level=valid_user_data["experience_level"]
        )

    def test_create_user_calls_repository_with_correct_params(self, valid_user_data):
        """Test that controller calls repository with correct parameters."""
        mock_repository = Mock(spec=UserRepository)
        mock_repository.create_user.return_value = Mock()

        controller = UserController(mock_repository)
        controller.create_user(valid_user_data)

        mock_repository.create_user.assert_called_once()
        call_kwargs = mock_repository.create_user.call_args[1]

        assert call_kwargs["name"] == valid_user_data["name"]
        assert call_kwargs["age"] == valid_user_data["age"]
        assert call_kwargs["goals"] == valid_user_data["goals"]
        assert call_kwargs["experience_level"] == valid_user_data["experience_level"]

    def test_get_all_users_success(self):
        """Test successful retrieval of all users."""
        mock_repository = Mock(spec=UserRepository)
        mock_users = [
            Mock(id=1, name="Usuario 1"),
            Mock(id=2, name="Usuario 2")
        ]
        mock_repository.get_all_users.return_value = mock_users

        controller = UserController(mock_repository)
        result = controller.get_all_users()

        assert result == mock_users
        assert len(result) == 2
        mock_repository.get_all_users.assert_called_once()

    def test_get_all_users_empty(self):
        """Test retrieval of all users when database is empty."""
        mock_repository = Mock(spec=UserRepository)
        mock_repository.get_all_users.return_value = []

        controller = UserController(mock_repository)
        result = controller.get_all_users()

        assert result == []
        assert len(result) == 0

    def test_create_user_with_optional_restrictions(self):
        """Test creating user with optional restrictions field."""
        mock_repository = Mock(spec=UserRepository)
        mock_user = Mock(spec=User)
        mock_repository.create_user.return_value = mock_user

        controller = UserController(mock_repository)

        request_data = {
            "name": "Usuario",
            "age": 25,
            "goals": ["test"],
            "restrictions": None,
            "experience_level": "iniciante"
        }

        controller.create_user(request_data)

        mock_repository.create_user.assert_called_once()
        call_kwargs = mock_repository.create_user.call_args[1]
        assert call_kwargs["restrictions"] is None

    def test_controller_initialization(self):
        """Test controller initialization with repository."""
        mock_repository = Mock(spec=UserRepository)

        controller = UserController(mock_repository)

        assert controller.user_repository == mock_repository
