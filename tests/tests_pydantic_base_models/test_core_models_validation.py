import pytest
from pydantic import ValidationError

from pydantic_base_models import (
    Role,
    Message,
    ChatTurn,
    ChatRequest,
    ChatResponse,
    ConversationConfig,
)


def test_message_valid_minimal() -> None:
    m = Message(role=Role.user, content="hello")
    assert m.role is Role.user
    assert m.content == "hello"
    assert m.created_at is not None


def test_message_trims_content() -> None:
    m = Message(role=Role.user, content="  hi  ")
    assert m.content == "hi"


def test_message_empty_after_strip_invalid() -> None:
    with pytest.raises(ValidationError):
        Message(role=Role.user, content="   ")


def test_message_max_length_boundary() -> None:
    text = "x" * 4000
    m = Message(role=Role.user, content=text)
    assert len(m.content) == 4000


def test_message_too_long_invalid() -> None:
    text = "x" * 4001
    with pytest.raises(ValidationError):
        Message(role=Role.user, content=text)


def test_message_invalid_role_string() -> None:
    with pytest.raises(ValidationError):
        Message(role="unknown", content="hi")  # type: ignore[arg-type]


def test_chat_turn_valid() -> None:
    user = Message(role=Role.user, content="u")
    assistant = Message(role=Role.assistant, content="a")
    turn = ChatTurn(user=user, assistant=assistant)
    assert turn.user.role is Role.user
    assert turn.assistant.role is Role.assistant


def test_chat_request_valid() -> None:
    msg = Message(role=Role.user, content="hello")
    req = ChatRequest(session_id="sess-1", message=msg)
    assert req.session_id == "sess-1"
    assert req.message is msg
    assert req.config_overrides is None


def test_assistant_message_may_exceed_user_limit() -> None:
    # Real model replies can be long; only what a person sends is capped.
    m = Message(role=Role.assistant, content="x" * 10_000)
    assert len(m.content) == 10_000


def test_created_at_is_timezone_aware() -> None:
    m = Message(role=Role.user, content="hi")
    assert m.created_at.tzinfo is not None
