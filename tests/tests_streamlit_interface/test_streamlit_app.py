from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[2] / "src" / "streamlit_interface" / "app.py")


def test_app_starts_in_demo_mode() -> None:
    at = AppTest.from_file(APP).run()
    assert not at.exception
    assert at.title[0].value == "Personal Chatbot"
    assert "demo" in at.sidebar.caption[0].value


def test_message_and_reply_are_shown() -> None:
    at = AppTest.from_file(APP).run()
    at.chat_input[0].set_value("hello").run()
    at.chat_input[0].set_value("second").run()

    contents = [m.markdown[0].value for m in at.chat_message]
    assert contents[0] == "hello"
    assert contents[1].startswith("Demo mode")
    assert contents[2] == "second"
    assert "1 earlier message " in contents[3]


def test_new_conversation_clears_chat() -> None:
    at = AppTest.from_file(APP).run()
    at.chat_input[0].set_value("hello").run()
    at.sidebar.button[0].click().run()
    assert len(at.chat_message) == 0


def test_too_long_message_shows_error() -> None:
    at = AppTest.from_file(APP).run()
    at.chat_input[0].set_value("x" * 5000).run()
    assert at.error
    assert len(at.chat_message) == 0
