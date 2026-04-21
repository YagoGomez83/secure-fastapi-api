from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_users():
    response = client.get("/api/v1/users")
    assert response.status_code == 200