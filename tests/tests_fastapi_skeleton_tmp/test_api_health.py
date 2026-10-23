from fastapi.testclient import TestClient

from FastApi_Skeleton.main import app


client = TestClient(app)


def test_health_returns_200() -> None:
    response = client.get("/health")
    assert response.status_code == 200


def test_health_response_shape() -> None:
    response = client.get("/health")
    data = response.json()
    assert data["status"] == "ok"
    assert data["app"] == "chat-api"
    assert isinstance(data["version"], str)
    assert data["version"]
