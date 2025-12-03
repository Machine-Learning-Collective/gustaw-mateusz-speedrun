# tests/test_chat_api.py
from fastapi.testclient import TestClient
from FastApi_Skeleton.main import app, agent


client = TestClient(app)


def test_chat_success(monkeypatch):
    # stubujemy agenta, żeby nie wołać prawdziwego OpenAI
    def fake_send(msg: str, session_id: str = "default") -> str:
        return "Hello from fake agent"

    monkeypatch.setattr(agent, "send", fake_send)

    payload = {"message": "hi", "session_id": "test-session"}

    resp = client.post("/chat", json=payload)

    assert resp.status_code == 200
    data = resp.json()
    assert data["session_id"] == "test-session"
    assert data["message"]["content"] == "Hello from fake agent"
    assert isinstance(data["history"], list)
