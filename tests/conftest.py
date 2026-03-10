from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient

from src.database.postgres_setting import Base, get_db
from src.main.main import app


@pytest.fixture
def fake_db_session():
    return Mock()


@pytest.fixture(scope="function")
def test_client(fake_db_session):
    """Create FastAPI test client with mocked startup and database dependency."""

    def override_get_db():
        yield fake_db_session

    app.dependency_overrides[get_db] = override_get_db

    with patch.object(Base.metadata, "create_all", return_value=None):
        with TestClient(app) as client:
            yield client

    app.dependency_overrides.clear()


@pytest.fixture
def valid_user_data():
    """Sample valid user data for testing."""
    return {
        "name": "Test Usuario",
        "age": 30,
        "goals": ["Reduzir estresse", "Melhorar sono"],
        "restrictions": "Sem lactose",
        "experience_level": "intermediário"
    }


@pytest.fixture
def valid_user_data_iniciante():
    """Sample valid iniciante user data for testing."""
    return {
        "name": "Usuario Iniciante",
        "age": 25,
        "goals": ["Melhorar condicionamento"],
        "restrictions": None,
        "experience_level": "iniciante"
    }


@pytest.fixture
def sample_user(valid_user_data):
    return SimpleNamespace(
        id=1,
        name=valid_user_data["name"],
        age=valid_user_data["age"],
        goals=valid_user_data["goals"],
        restrictions=valid_user_data["restrictions"],
        experience_level=valid_user_data["experience_level"],
        created_at=datetime.now(timezone.utc),
    )
