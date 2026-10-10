import sys
from pathlib import Path

import streamlit as st

# `streamlit run` puts only this file's folder on the import path; add src/ so sibling packages import.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Pydantic_Base_Models import Message, Role
from Streamlit_Interface.ui_shell import ChatUIShell, mock_responder


SESSION_ID = "streamlit-session"


def get_shell() -> ChatUIShell:
    if "ui_shell" not in st.session_state:
        st.session_state.ui_shell = ChatUIShell(responder=mock_responder)
    return st.session_state.ui_shell


def render_history(shell: ChatUIShell) -> None:
    history = shell.get_history(SESSION_ID)
    for msg in history:
        if msg.role is Role.user:
            with st.chat_message("user"):
                st.markdown(msg.content)
        elif msg.role is Role.assistant:
            with st.chat_message("assistant"):
                st.markdown(msg.content)


def main() -> None:
    st.title("Streamlit Chat Interface")

    shell = get_shell()
    render_history(shell)

    if prompt := st.chat_input("Type your message"):
        reply = shell.send(prompt, session_id=SESSION_ID)
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            st.markdown(reply.content)


if __name__ == "__main__":
    main()
