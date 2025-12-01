import pytest
from langchain_community.chat_models.fake import FakeListChatModel

from LangChain_Conversational_Agent.langchain_agent import LangChainAgent
from Pydantic_Base_Models import ConversationConfig, Role


def make_agent(responses=None, max_history_messages=20) -> LangChainAgent:
    if responses is None:
        responses = [
            "Hi!",
            "How can I help?",
            "Got it.",
            "Ok.",
        ]
    llm = FakeListChatModel(responses=responses)
    cfg = ConversationConfig(
        system_prompt="You are a test bot.",
        max_history_messages=max_history_messages,
    )
    return LangChainAgent(llm=llm, config=cfg)


def test_conversation_flow_two_turns() -> None:
    agent = make_agent()
    session_id = "flow"

    r1 = agent.send("hello", session_id=session_id)
    r2 = agent.send("second message", session_id=session_id)

    assert isinstance(r1, str)
    assert isinstance(r2, str)

    history = agent.get_history(session_id=session_id)
    assert len(history) == 4
    assert history[0].role == Role.user
    assert history[1].role == Role.assistant
    assert history[2].role == Role.user
    assert history[3].role == Role.assistant


def test_memory_persists_between_turns() -> None:
    responses = ["first answer", "second answer"]
    agent = make_agent(responses=responses)
    session_id = "memory"

    agent.send("turn one", session_id=session_id)
    agent.send("turn two", session_id=session_id)

    history = agent.get_history(session_id=session_id)

    user_contents = [m.content for m in history if m.role == Role.user]
    assistant_contents = [m.content for m in history if m.role == Role.assistant]

    assert "turn one" in user_contents
    assert "turn two" in user_contents
    assert "first answer" in assistant_contents
    assert "second answer" in assistant_contents


def test_reset_clears_history() -> None:
    agent = make_agent()
    session_id = "reset"

    agent.send("one", session_id=session_id)
    agent.send("two", session_id=session_id)
    assert len(agent.get_history(session_id=session_id)) > 0

    agent.reset(session_id=session_id)
    history = agent.get_history(session_id=session_id)
    assert history == []


def test_multiple_sessions_isolated() -> None:
    agent = make_agent()

    agent.send("hello A1", session_id="A")
    agent.send("hello A2", session_id="A")
    agent.send("hello B1", session_id="B")

    history_a = agent.get_history(session_id="A")
    history_b = agent.get_history(session_id="B")

    assert len(history_a) == 4
    assert len(history_b) == 2
    assert any(m.content == "hello A1" for m in history_a)
    assert any(m.content == "hello A2" for m in history_a)
    assert any(m.content == "hello B1" for m in history_b)
    assert not any(m.content == "hello B1" for m in history_a)


def test_empty_input_does_not_crash() -> None:
    agent = make_agent()
    out = agent.send("", session_id="empty")
    assert isinstance(out, str)


def test_long_input_does_not_crash() -> None:
    agent = make_agent()
    long_text = "x" * 10_000
    out = agent.send(long_text, session_id="long")
    assert isinstance(out, str)


def test_history_trimming_respects_max_history_messages() -> None:
    agent = make_agent(max_history_messages=4)
    session_id = "trim"

    agent.send("m1", session_id=session_id)
    agent.send("m2", session_id=session_id)
    agent.send("m3", session_id=session_id)

    history = agent.get_history(session_id=session_id)
    assert len(history) == 4

    user_messages = [m.content for m in history if m.role == Role.user]
    assert "m2" in user_messages
    assert "m3" in user_messages
    assert "m1" not in user_messages
