# streamlit_app.py
import uuid
import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000/chat"


def get_session_id():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    return st.session_state.session_id


def get_messages():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    return st.session_state.messages


st.set_page_config(page_title="Chatbot", page_icon="💬")
st.title("Chatbot (FastAPI + LangChain + Streamlit)")

session_id = get_session_id()
messages = get_messages()

for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your message...")

if user_input:
    messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    payload = {
        "message": user_input,
        "session_id": session_id,
    }

    try:
        resp = requests.post(BACKEND_URL, json=payload, timeout=30)
    except Exception as e:
        with st.chat_message("assistant"):
            st.error(f"Backend error: {e}")
    else:
        if resp.status_code != 200:
            with st.chat_message("assistant"):
                st.error(f"API error {resp.status_code}: {resp.text}")
        else:
            data = resp.json()
            assistant_text = data["message"]["content"]

            messages.append({"role": "assistant", "content": assistant_text})
            with st.chat_message("assistant"):
                st.markdown(assistant_text)
