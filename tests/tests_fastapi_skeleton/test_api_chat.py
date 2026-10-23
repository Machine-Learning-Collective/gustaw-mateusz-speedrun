from fastapi.testclient import TestClient

from chat_service import ChatService
from fastapi_skeleton.main import create_app
from pydantic_base_models import MAX_USER_MESSAGE_CHARS
from tests.conftest import FailingChatModel, RecordingChatModel


def client_with(llm) -> TestClient:
    return TestClient(create_app(ChatService(llm, llm_description="test")))


def chat_body(text: str, session_id: str = "s", role: str = "user") -> dict:
    return {"session_id": session_id, "message": {"role": role, "content": text}}


def test_chat_round_trip(recording_llm: RecordingChatModel) -> None:
    client = client_with(recording_llm)
    first = client.post("/chat", json=chat_body("hello"))
    second = client.post("/chat", json=chat_body("again"))

    assert first.status_code == 200
    assert first.json()["message"] == {**first.json()["message"], "role": "assistant", "content": "first reply"}
    assert [m["content"] for m in second.json()["history"]] == ["hello", "first reply", "again", "second reply"]


def test_invalid_messages_rejected_with_422(recording_llm: RecordingChatModel) -> None:
    client = client_with(recording_llm)
    for body in (
        chat_body(""),
        chat_body("x" * (MAX_USER_MESSAGE_CHARS + 1)),
        chat_body("hi", role="assistant"),
        chat_body("hi", session_id=""),
    ):
        assert client.post("/chat", json=body).status_code == 422
    assert recording_llm.calls == []


def test_provider_failure_returns_502_without_details() -> None:
    response = client_with(FailingChatModel()).post("/chat", json=chat_body("hello"))
    assert response.status_code == 502
    assert "provider unavailable" not in response.text


def test_session_history_and_delete(recording_llm: RecordingChatModel) -> None:
    client = client_with(recording_llm)
    assert client.get("/sessions/s/messages").status_code == 404

    client.post("/chat", json=chat_body("hello"))
    messages = client.get("/sessions/s/messages").json()
    assert [m["role"] for m in messages] == ["user", "assistant"]

    assert client.delete("/sessions/s").status_code == 204
    assert client.get("/sessions/s/messages").status_code == 404


def test_health_reports_provider(recording_llm: RecordingChatModel) -> None:
    assert client_with(recording_llm).get("/health").json()["llm_provider"] == "test"


def test_default_app_runs_in_demo_mode_without_key() -> None:
    from fastapi_skeleton.main import app

    client = TestClient(app)
    assert client.get("/health").json()["llm_provider"] == "demo"
    reply = client.post("/chat", json=chat_body("ping", session_id="demo")).json()["message"]["content"]
    assert reply.startswith("Demo mode")
