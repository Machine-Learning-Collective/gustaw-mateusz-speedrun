import pytest
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from langchain_conversational_agent.langchain_agent import LangChainAgent
from pydantic_base_models import MAX_USER_MESSAGE_CHARS, ConversationConfig, Role
from tests.conftest import FailingChatModel, RecordingChatModel


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


# Milestone 2 had "empty/long input does not crash" tests. send() did not crash, but it stored
# a message that later made get_history() raise. Invalid input is now rejected up front.
@pytest.mark.parametrize("text", ["", "   ", "x" * (MAX_USER_MESSAGE_CHARS + 1)])
def test_invalid_input_rejected_without_touching_history(text: str) -> None:
    agent = make_agent()
    agent.send("valid", session_id="s")
    with pytest.raises(ValueError):
        agent.send(text, session_id="s")
    assert len(agent.get_history(session_id="s")) == 2


def test_history_readable_after_long_model_reply() -> None:
    # A real model can answer with far more than the 4000-character limit for user messages.
    agent = make_agent(responses=["y" * 10_000])
    agent.send("write me an essay", session_id="long")
    history = agent.get_history(session_id="long")
    assert len(history[1].content) == 10_000


def test_model_receives_system_prompt_history_and_new_input(recording_llm: RecordingChatModel) -> None:
    agent = LangChainAgent(recording_llm, ConversationConfig(system_prompt="Be brief."))
    agent.send("hello", session_id="s")
    agent.send("and again", session_id="s")

    prompt = recording_llm.calls[-1]
    assert isinstance(prompt[0], SystemMessage) and prompt[0].content == "Be brief."
    assert [type(m) for m in prompt[1:]] == [HumanMessage, AIMessage, HumanMessage]
    assert [m.content for m in prompt[1:]] == ["hello", "first reply", "and again"]


def test_braces_in_system_prompt_are_not_template_variables(recording_llm: RecordingChatModel) -> None:
    agent = LangChainAgent(recording_llm, ConversationConfig(system_prompt='Reply as {"answer": ...}'))
    agent.send("hi {name}", session_id="s")
    prompt = recording_llm.calls[-1]
    assert prompt[0].content == 'Reply as {"answer": ...}'
    assert prompt[-1].content == "hi {name}"


def test_failed_model_call_leaves_history_unchanged() -> None:
    agent = LangChainAgent(FailingChatModel())
    with pytest.raises(ConnectionError):
        agent.send("hello", session_id="s")
    assert agent.get_history(session_id="s") == []


def test_agents_can_share_a_history_store(recording_llm: RecordingChatModel) -> None:
    store: dict = {}
    first = LangChainAgent(recording_llm, ConversationConfig(system_prompt="A"), history_store=store)
    second = LangChainAgent(recording_llm, ConversationConfig(system_prompt="B"), history_store=store)
    first.send("one", session_id="s")
    second.send("two", session_id="s")
    assert [m.content for m in second.get_history("s")] == ["one", "first reply", "two", "second reply"]


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
