from Pydantic_Base_Models import (
    Role,
    Message,
    ChatResponse,
    ConversationConfig,
    ChatRequest,
)


def test_message_roundtrip_dict_and_json() -> None:
    m = Message(role=Role.user, content="hello")
    data = m.model_dump()
    m2 = Message.model_validate(data)
    assert m2 == m

    json_str = m.model_dump_json()
    m3 = Message.model_validate_json(json_str)
    assert m3 == m


def test_chat_response_roundtrip() -> None:
    msg = Message(role=Role.assistant, content="ok")
    history = [
        Message(role=Role.user, content="hi"),
        Message(role=Role.assistant, content="ok"),
    ]
    resp = ChatResponse(session_id="s1", message=msg, history=history)
    dumped = resp.model_dump()
    resp2 = ChatResponse.model_validate(dumped)
    assert resp2 == resp


def test_conversation_config_roundtrip_json() -> None:
    cfg = ConversationConfig(
        system_prompt="Test prompt",
        memory_key="mem",
        input_key="inp",
        max_history_messages=10,
        locale="en",
    )
    json_str = cfg.model_dump_json()
    cfg2 = ConversationConfig.model_validate_json(json_str)
    assert cfg2 == cfg
