from datetime import datetime, timezone
from types import SimpleNamespace


class TestUserRouter:
    """Test suite for user router endpoints."""

    def test_post_create_user_success(self, monkeypatch, test_client, valid_user_data):
        """Test POST /users endpoint successfully creates a user."""
        fake_user = SimpleNamespace(
            id=1,
            name=valid_user_data["name"],
            age=valid_user_data["age"],
            goals=valid_user_data["goals"],
            restrictions=valid_user_data["restrictions"],
            experience_level=valid_user_data["experience_level"],
            created_at=datetime.now(timezone.utc),
        )
        monkeypatch.setattr(
            "src.modules.users.router.user_router.UserController.create_user",
            lambda self, request: fake_user,
        )

        response = test_client.post("/users/", json=valid_user_data)

        assert response.status_code == 201
        data = response.json()

        assert "user" in data
        assert data["user"]["name"] == valid_user_data["name"]
        assert data["user"]["age"] == valid_user_data["age"]
        assert data["user"]["goals"] == valid_user_data["goals"]
        assert data["user"]["restrictions"] == valid_user_data["restrictions"]
        assert data["user"]["experience_level"] == valid_user_data["experience_level"]
        assert data["user"]["id"] is not None

    def test_post_create_user_returns_user_with_id(self, monkeypatch, test_client, valid_user_data):
        """Test that created user has an ID."""
        monkeypatch.setattr(
            "src.modules.users.router.user_router.UserController.create_user",
            lambda self, request: SimpleNamespace(
                id=10,
                name=valid_user_data["name"],
                age=valid_user_data["age"],
                goals=valid_user_data["goals"],
                restrictions=valid_user_data["restrictions"],
                experience_level=valid_user_data["experience_level"],
            ),
        )

        response = test_client.post("/users/", json=valid_user_data)

        assert response.status_code == 201
        user_id = response.json()["user"]["id"]

        assert user_id is not None
        assert isinstance(user_id, int)
        assert user_id > 0

    def test_post_create_user_without_restrictions(self, monkeypatch, test_client):
        """Test creating user without restrictions field."""
        user_data = {
            "name": "Usuario Sem Restricoes",
            "age": 30,
            "goals": ["Melhorar"],
            "experience_level": "intermediário"
        }
        monkeypatch.setattr(
            "src.modules.users.router.user_router.UserController.create_user",
            lambda self, request: SimpleNamespace(
                id=1,
                name=user_data["name"],
                age=user_data["age"],
                goals=user_data["goals"],
                restrictions=None,
                experience_level=user_data["experience_level"],
            ),
        )

        response = test_client.post("/users/", json=user_data)

        assert response.status_code == 201
        data = response.json()
        assert data["user"]["restrictions"] is None

    def test_post_create_user_invalid_missing_name(self, test_client):
        """Test POST /users with missing name field returns 422."""
        invalid_data = {
            "age": 30,
            "goals": ["test"],
            "experience_level": "intermediário"
        }

        response = test_client.post("/users/", json=invalid_data)

        assert response.status_code == 422

    def test_post_create_user_invalid_missing_age(self, test_client):
        """Test POST /users with missing age field returns 422."""
        invalid_data = {
            "name": "Usuario",
            "goals": ["test"],
            "experience_level": "intermediário"
        }

        response = test_client.post("/users/", json=invalid_data)

        assert response.status_code == 422

    def test_post_create_user_invalid_missing_goals(self, test_client):
        """Test POST /users with missing goals field returns 422."""
        invalid_data = {
            "name": "Usuario",
            "age": 30,
            "experience_level": "intermediário"
        }

        response = test_client.post("/users/", json=invalid_data)

        assert response.status_code == 422

    def test_post_create_user_invalid_missing_experience_level(self, test_client):
        """Test POST /users with missing experience_level returns 422."""
        invalid_data = {
            "name": "Usuario",
            "age": 30,
            "goals": ["test"]
        }

        response = test_client.post("/users/", json=invalid_data)

        assert response.status_code == 422

    def test_get_all_users_empty(self, monkeypatch, test_client):
        """Test GET /users returns empty list when no users exist."""
        monkeypatch.setattr(
            "src.modules.users.router.user_router.UserController.get_all_users",
            lambda self: [],
        )

        response = test_client.get("/users/")

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)
        assert len(data) == 0

    def test_get_all_users_after_creation(self, monkeypatch, test_client, valid_user_data):
        """Test GET /users returns created users."""
        second_user_data = valid_user_data.copy()
        second_user_data["name"] = "Outro Usuario"
        monkeypatch.setattr(
            "src.modules.users.router.user_router.UserController.get_all_users",
            lambda self: [
                {
                    "id": 1,
                    "name": valid_user_data["name"],
                    "age": valid_user_data["age"],
                    "goals": valid_user_data["goals"],
                    "restrictions": valid_user_data["restrictions"],
                    "experience_level": valid_user_data["experience_level"],
                },
                {
                    "id": 2,
                    "name": second_user_data["name"],
                    "age": second_user_data["age"],
                    "goals": second_user_data["goals"],
                    "restrictions": second_user_data["restrictions"],
                    "experience_level": second_user_data["experience_level"],
                },
            ],
        )

        response = test_client.get("/users/")

        assert response.status_code == 200
        users = response.json()

        assert len(users) == 2
        assert users[0]["name"] == valid_user_data["name"]
        assert users[1]["name"] == second_user_data["name"]

    def test_post_create_user_with_multiple_goals(self, monkeypatch, test_client):
        """Test creating user with multiple goals."""
        user_data = {
            "name": "Usuario Multi Goals",
            "age": 35,
            "goals": ["Perder peso", "Melhorar sono", "Reduzir estresse", "Ganhar flexibilidade"],
            "restrictions": "Sem gluten",
            "experience_level": "intermediário"
        }
        monkeypatch.setattr(
            "src.modules.users.router.user_router.UserController.create_user",
            lambda self, request: SimpleNamespace(
                id=1,
                name=user_data["name"],
                age=user_data["age"],
                goals=user_data["goals"],
                restrictions=user_data["restrictions"],
                experience_level=user_data["experience_level"],
            ),
        )

        response = test_client.post("/users/", json=user_data)

        assert response.status_code == 201
        data = response.json()
        assert len(data["user"]["goals"]) == 4
        assert data["user"]["goals"] == user_data["goals"]

    def test_post_create_user_response_structure(self, monkeypatch, test_client, valid_user_data):
        """Test that created user response follows the documented schema."""
        monkeypatch.setattr(
            "src.modules.users.router.user_router.UserController.create_user",
            lambda self, request: SimpleNamespace(
                id=1,
                name=valid_user_data["name"],
                age=valid_user_data["age"],
                goals=valid_user_data["goals"],
                restrictions=valid_user_data["restrictions"],
                experience_level=valid_user_data["experience_level"],
            ),
        )

        response = test_client.post("/users/", json=valid_user_data)

        assert response.status_code == 201
        data = response.json()

        assert data["message"] == "Usuario criado"
        assert "user" in data
        assert "id" in data["user"]

    def test_post_create_user_all_experience_levels(self, monkeypatch, test_client):
        """Test creating users with all valid experience levels."""
        levels = ["iniciante", "intermediário", "avançado"]

        for i, level in enumerate(levels):
            user_data = {
                "name": f"Usuario {level}",
                "age": 25 + i,
                "goals": ["test"],
                "experience_level": level
            }
            monkeypatch.setattr(
                "src.modules.users.router.user_router.UserController.create_user",
                lambda self, request, user_data=user_data: SimpleNamespace(
                    id=1,
                    name=user_data["name"],
                    age=user_data["age"],
                    goals=user_data["goals"],
                    restrictions=user_data.get("restrictions"),
                    experience_level=user_data["experience_level"],
                ),
            )

            response = test_client.post("/users/", json=user_data)

            assert response.status_code == 201
            data = response.json()
            assert data["user"]["experience_level"] == level

    def test_router_endpoint_exists(self, monkeypatch, test_client):
        """Test that /users endpoint exists and responds."""
        monkeypatch.setattr(
            "src.modules.users.router.user_router.UserController.get_all_users",
            lambda self: [],
        )

        response = test_client.get("/users/")

        assert response.status_code == 200

    def test_post_create_user_response_contains_message(self, monkeypatch, test_client, valid_user_data):
        """Test that POST response from router includes message."""
        monkeypatch.setattr(
            "src.modules.users.router.user_router.UserController.create_user",
            lambda self, request: SimpleNamespace(
                id=1,
                name=valid_user_data["name"],
                age=valid_user_data["age"],
                goals=valid_user_data["goals"],
                restrictions=valid_user_data["restrictions"],
                experience_level=valid_user_data["experience_level"],
            ),
        )

        response = test_client.post("/users/", json=valid_user_data)

        assert response.status_code == 201
        data = response.json()

        assert data["message"] == "Usuario criado"
        assert "user" in data
