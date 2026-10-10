import sys
import uuid
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from pydantic import ValidationError

# `streamlit run` puts only this file's folder on the import path; add src/ so sibling packages import.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Chat_Service import ChatService  # noqa: E402
from LangChain_Conversational_Agent.llm_factory import LLMSettings  # noqa: E402
from Pydantic_Base_Models import ChatRequest, ConversationConfig, Message, Role  # noqa: E402

DEFAULT_SYSTEM_PROMPT = ConversationConfig().system_prompt


@st.cache_resource
def get_service() -> ChatService:
    """One service per server process; each browser tab gets its own session id within it."""
    load_dotenv()
    return ChatService.from_settings(LLMSettings.from_env())


def session_id() -> str:
    if "session_id" not in st.session_state:
        st.session_state.session_id = f"streamlit-{uuid.uuid4()}"
    return st.session_state.session_id


def config_from_sidebar(service: ChatService) -> ConversationConfig | None:
    with st.sidebar:
        st.subheader("Settings")
        st.caption(f"Model: **{service.llm_description}**")
        if service.llm_description == "demo":
            st.info("Demo mode. Set OPENAI_API_KEY in a .env file to talk to a real model.")

        system_prompt = st.text_area("System prompt", value=DEFAULT_SYSTEM_PROMPT, height=120).strip()

        if st.button("New conversation", width="stretch"):
            service.reset(session_id())

    if not system_prompt or system_prompt == DEFAULT_SYSTEM_PROMPT:
        return None
    return ConversationConfig(system_prompt=system_prompt)


def main() -> None:
    st.set_page_config(page_title="Personal Chatbot")
    st.title("Personal Chatbot")

    service = get_service()
    overrides = config_from_sidebar(service)

    error: str | None = None
    if prompt := st.chat_input("Type your message"):
        try:
            request = ChatRequest(
                session_id=session_id(),
                message=Message(role=Role.user, content=prompt),
                config_overrides=overrides,
            )
            service.chat(request)
        except ValidationError as exc:
            error = exc.errors()[0]["msg"]
        except Exception:
            error = "The language model request failed. Try again in a moment."

    for message in service.get_history(session_id()):
        with st.chat_message("user" if message.role is Role.user else "assistant"):
            st.markdown(message.content)

    if error:
        st.error(error)


if __name__ == "__main__":
    main()
