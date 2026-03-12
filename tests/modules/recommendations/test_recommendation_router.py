from datetime import datetime, timezone
from types import SimpleNamespace


class TestRecommendationRouter:
    """Test suite for recommendation router endpoints."""

    # ── POST /recommendations/ ──

    def test_post_create_recommendation_success(self, monkeypatch, test_client, valid_recommendation_data):
        """Test POST /recommendations/ successfully creates a recommendation."""
        fake_rec = SimpleNamespace(
            id=1, user_id=1, name="Teste",
            description="Recomendação de teste", duration=30.0,
            category="Exercício", reasoning="Recomendação gerada para teste",
            precautions="Sem precauções específicas",
            created_at=datetime.now(timezone.utc),
        )
        monkeypatch.setattr(
            "src.modules.recommendations.router.recommendation_router.RecommendationController.create_recommendation",
            lambda self, request: fake_rec,
        )

        response = test_client.post("/recommendations/", json=valid_recommendation_data)

        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "Recomendação criada"
        assert "response" in data
        assert len(data["response"]["activities"]) == 1
        assert data["response"]["activities"][0]["name"] == "Teste"
        assert data["response"]["activities"][0]["duration"] == 30.0
        assert data["response"]["reasoning"] == "Recomendação gerada para teste"
        assert data["response"]["precautions"] == "Sem precauções específicas"

    def test_post_create_recommendation_user_not_found(self, monkeypatch, test_client, valid_recommendation_data):
        """Test POST /recommendations/ returns 404 when user not found."""
        monkeypatch.setattr(
            "src.modules.recommendations.router.recommendation_router.RecommendationController.create_recommendation",
            lambda self, request: None,
        )

        response = test_client.post("/recommendations/", json=valid_recommendation_data)

        assert response.status_code == 404
        assert response.json()["detail"] == "Usuário não encontrado"

    def test_post_create_recommendation_validation_error(self, test_client):
        """Test POST /recommendations/ returns 422 with invalid data."""
        invalid_data = {"invalid_field": "value"}

        response = test_client.post("/recommendations/", json=invalid_data)

        assert response.status_code == 422

    def test_post_create_recommendation_missing_user_id(self, test_client):
        """Test POST /recommendations/ returns 422 when user_id missing."""
        data = {"additional_info": "Info"}

        response = test_client.post("/recommendations/", json=data)

        assert response.status_code == 422

    def test_post_create_recommendation_without_additional_info(self, monkeypatch, test_client):
        """Test POST /recommendations/ succeeds without optional additional_info."""
        fake_rec = SimpleNamespace(
            id=1, user_id=1, name="Teste",
            description="Recomendação de teste", duration=30.0,
            category="Exercício", reasoning="Recomendação gerada para teste",
            precautions="Sem precauções específicas",
        )
        monkeypatch.setattr(
            "src.modules.recommendations.router.recommendation_router.RecommendationController.create_recommendation",
            lambda self, request: fake_rec,
        )

        response = test_client.post("/recommendations/", json={"user_id": 1})

        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "Recomendação criada"

    def test_post_create_recommendation_response_structure(self, monkeypatch, test_client, valid_recommendation_data):
        """Test POST /recommendations/ response has correct nested structure."""
        fake_rec = SimpleNamespace(
            id=1, user_id=1, name="Caminhada",
            description="Caminhada leve de 30 minutos", duration=30.0,
            category="Cardio", reasoning="Perfil do usuario",
            precautions="Nenhuma",
        )
        monkeypatch.setattr(
            "src.modules.recommendations.router.recommendation_router.RecommendationController.create_recommendation",
            lambda self, request: fake_rec,
        )

        response = test_client.post("/recommendations/", json=valid_recommendation_data)

        assert response.status_code == 201
        data = response.json()
        assert "message" in data
        assert "response" in data
        resp = data["response"]
        assert "activities" in resp
        assert "reasoning" in resp
        assert "precautions" in resp
        activity = resp["activities"][0]
        assert "name" in activity
        assert "description" in activity
        assert "duration" in activity
        assert "category" in activity

    # ── POST /recommendations/{id}/feedback ──

    def test_post_create_feedback_success(self, monkeypatch, test_client, valid_feedback_data):
        """Test POST /recommendations/{id}/feedback successfully creates feedback."""
        fake_feedback = SimpleNamespace(
            id=1, recommendation_id=1,
            rating=4, comment="Gostei muito da recomendação!",
            created_at=datetime.now(timezone.utc),
        )
        monkeypatch.setattr(
            "src.modules.recommendations.router.recommendation_router.RecommendationController.create_recommendation_feedback",
            lambda self, id, request: fake_feedback,
        )

        response = test_client.post("/recommendations/1/feedback", json=valid_feedback_data)

        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "Feedback criado"
        assert data["response"]["id"] == 1
        assert data["response"]["recommendation_id"] == 1
        assert data["response"]["rating"] == 4
        assert data["response"]["comment"] == "Gostei muito da recomendação!"

    def test_post_create_feedback_recommendation_not_found(self, monkeypatch, test_client, valid_feedback_data):
        """Test POST /recommendations/{id}/feedback returns 404 when recommendation not found."""
        monkeypatch.setattr(
            "src.modules.recommendations.router.recommendation_router.RecommendationController.create_recommendation_feedback",
            lambda self, id, request: None,
        )

        response = test_client.post("/recommendations/999/feedback", json=valid_feedback_data)

        assert response.status_code == 404
        assert response.json()["detail"] == "Recomendação não encontrada"

    def test_post_create_feedback_validation_error_missing_rating(self, test_client):
        """Test POST /recommendations/{id}/feedback returns 422 when rating missing."""
        data = {"comment": "Bom"}

        response = test_client.post("/recommendations/1/feedback", json=data)

        assert response.status_code == 422

    def test_post_create_feedback_validation_error_missing_comment(self, test_client):
        """Test POST /recommendations/{id}/feedback returns 422 when comment missing."""
        data = {"rating": 4}

        response = test_client.post("/recommendations/1/feedback", json=data)

        assert response.status_code == 422

    def test_post_create_feedback_response_structure(self, monkeypatch, test_client, valid_feedback_data):
        """Test POST /recommendations/{id}/feedback response structure."""
        fake_feedback = SimpleNamespace(
            id=5, recommendation_id=3,
            rating=5, comment="Excelente!",
        )
        monkeypatch.setattr(
            "src.modules.recommendations.router.recommendation_router.RecommendationController.create_recommendation_feedback",
            lambda self, id, request: fake_feedback,
        )

        response = test_client.post("/recommendations/3/feedback", json=valid_feedback_data)

        assert response.status_code == 201
        data = response.json()
        assert "message" in data
        assert "response" in data
        resp = data["response"]
        assert "id" in resp
        assert "recommendation_id" in resp
        assert "rating" in resp
        assert "comment" in resp

    def test_post_create_feedback_different_ratings(self, monkeypatch, test_client):
        """Test feedback creation with different valid rating values."""
        for rating in [1, 2, 3, 4, 5]:
            fake_feedback = SimpleNamespace(
                id=1, recommendation_id=1,
                rating=rating, comment="Teste",
            )
            monkeypatch.setattr(
                "src.modules.recommendations.router.recommendation_router.RecommendationController.create_recommendation_feedback",
                lambda self, id, request, fb=fake_feedback: fb,
            )

            response = test_client.post(
                "/recommendations/1/feedback",
                json={"rating": rating, "comment": "Teste"},
            )

            assert response.status_code == 201
            assert response.json()["response"]["rating"] == rating

    def test_post_create_feedback_rating_out_of_range(self, test_client):
        """Test feedback with rating out of valid range (1-5) returns 422."""
        for rating in [0, 6, -1, 100]:
            response = test_client.post(
                "/recommendations/1/feedback",
                json={"rating": rating, "comment": "Teste"},
            )
            assert response.status_code == 422
