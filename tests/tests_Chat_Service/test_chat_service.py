import threading

import pytest

from Chat_Service import ChatService
from Pydantic_Base_Models import ChatRequest, ConversationConfig, Message, Role
from tests.conftest import RecordingChatModel


def request(text: str, session_id: str = "s", **kwargs) -> ChatRequest:
    return ChatRequest(session_id=session_id, message=Message(role=Role.user, content=text), **kwargs)


def test_chat_returns_reply_and_full_history(recording_llm: RecordingChatModel) -> None:
    service = ChatService(recording_llm)
    service.chat(request("hello"))
    response = service.chat(request("again"))

    assert response.session_id == "s"
    assert response.message.role is Role.assistant
    assert response.message.content == "second reply"
    assert [m.role for m in response.history] == [Role.user, Role.assistant, Role.user, Role.assistant]


def test_sessions_are_isolated(recording_llm: RecordingChatModel) -> None:
    service = ChatService(recording_llm)
    service.chat(request("for A", session_id="A"))
    service.chat(request("for B", session_id="B"))
    assert [m.content for m in service.get_history("A") if m.role is Role.user] == ["for A"]
    assert [m.content for m in service.get_history("B") if m.role is Role.user] == ["for B"]


def test_reset_forgets_session(recording_llm: RecordingChatModel) -> None:
    service = ChatService(recording_llm)
    service.chat(request("hello"))
    service.reset("s")
    assert not service.has_session("s")
    assert service.get_history("s") == []


def test_config_override_changes_prompt_but_keeps_history(recording_llm: RecordingChatModel) -> None:
    service = ChatService(recording_llm, ConversationConfig(system_prompt="Default prompt."))
    service.chat(request("one"))
    service.chat(request("two", config_overrides=ConversationConfig(system_prompt="Pirate mode.")))

    last_prompt = recording_llm.calls[-1]
    assert last_prompt[0].content == "Pirate mode."
    assert [m.content for m in last_prompt[1:]] == ["one", "first reply", "two"]


def test_only_user_messages_can_be_sent() -> None:
    with pytest.raises(ValueError):
        ChatRequest(session_id="s", message=Message(role=Role.assistant, content="hi"))


def test_concurrent_turns_in_one_session_do_not_interleave() -> None:
    service = ChatService(RecordingChatModel(responses=["r"], calls=[]))
    threads = [threading.Thread(target=service.chat, args=(request(f"m{i}"),)) for i in range(20)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    history = service.get_history("s")
    assert len(history) == 20  # trimmed to the default limit of 20
    assert [m.role for m in history] == [Role.user, Role.assistant] * 10
