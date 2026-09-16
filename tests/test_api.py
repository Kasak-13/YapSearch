import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.search_core import search_core

client = TestClient(app)

class TestApiEndpoints:
    """Integration tests for FastAPI REST endpoints."""

    def test_root_endpoint_html(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "YapSearch" in response.text

    def test_health_endpoint(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "messages_indexed" in data
        assert "model_name" in data
        assert "reference_date" in data

    def test_search_empty_query_400(self):
        response = client.post("/search", json={"query": "   "})
        assert response.status_code == 400
        assert "cannot be empty" in response.json()["detail"]

    def test_search_valid_query_structure(self):
        response = client.post("/search", json={"query": "What did Priya say about the budget?", "top_k": 3})
        assert response.status_code == 200
        data = response.json()
        assert data["query"] == "What did Priya say about the budget?"
        assert data["parsed"]["speaker"] == "Priya"
        assert isinstance(data["results"], list)
        assert len(data["results"]) <= 3

        if data["results"]:
            first = data["results"][0]
            assert "message_id" in first
            assert "sender" in first
            assert "similarity" in first
            assert 0.0 <= first["similarity"] <= 1.0
            assert "context" in first
