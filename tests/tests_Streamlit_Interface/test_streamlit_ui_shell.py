from Pydantic_Base_Models import Message, Role
from Streamlit_Interface.ui_shell import ChatUIShell


def echo_responder(history: list[Message], user_input: str) -> str:
    return f"echo: {user_input}"


def test_ui_shell_basic_flow() -> None:
    shell = ChatUIShell(responder=echo_responder)
    session_id = "s1"

    r1 = shell.send("hello", session_id=session_id)
    r2 = shell.send("world", session_id=session_id)

    assert r1.content == "echo: hello"
    assert r2.content == "echo: world"

    history = shell.get_history(session_id=session_id)
    assert len(history) == 4
    assert history[0].role is Role.user
    assert history[1].role is Role.assistant
    assert history[2].role is Role.user
    assert history[3].role is Role.assistant


def test_ui_shell_session_state_isolated() -> None:
    shell = ChatUIShell(responder=echo_responder)

    shell.send("hi A", session_id="A")
    shell.send("hi B", session_id="B")

    history_a = shell.get_history("A")
    history_b = shell.get_history("B")

    assert any(m.content == "hi A" for m in history_a if m.role is Role.user)
    assert any(m.content == "hi B" for m in history_b if m.role is Role.user)
    assert not any(m.content == "hi B" for m in history_a if m.role is Role.user)


def test_ui_shell_reset_clears_session() -> None:
    shell = ChatUIShell(responder=echo_responder)
    session_id = "reset"

    shell.send("msg1", session_id=session_id)
    assert len(shell.get_history(session_id)) > 0

    shell.reset(session_id)
    history = shell.get_history(session_id)
    assert history == []


def test_ui_shell_empty_history_for_new_session() -> None:
    shell = ChatUIShell(responder=echo_responder)
    history = shell.get_history("new-session")
    assert history == []
