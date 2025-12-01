from __future__ import annotations

from typing import Callable, Dict, List

from Pydantic_Base_Models import Message, Role


ResponderFn = Callable[[List[Message], str], str]


class ChatUIShell:
    def __init__(self, responder: ResponderFn) -> None:
        self._responder = responder
        self._sessions: Dict[str, List[Message]] = {}

    def _get_session_history(self, session_id: str) -> List[Message]:
        if session_id not in self._sessions:
            self._sessions[session_id] = []
        return self._sessions[session_id]

    def send(self, user_input: str, session_id: str = "default") -> Message:
        history = self._get_session_history(session_id)
        user_msg = Message(role=Role.user, content=user_input)
        history.append(user_msg)
        reply_text = self._responder(history, user_input)
        assistant_msg = Message(role=Role.assistant, content=reply_text)
        history.append(assistant_msg)
        return assistant_msg

    def get_history(self, session_id: str = "default") -> List[Message]:
        return list(self._get_session_history(session_id))

    def reset(self, session_id: str = "default") -> None:
        if session_id in self._sessions:
            self._sessions[session_id] = []


def mock_responder(history: List[Message], user_input: str) -> str:
    return f"mock reply: {user_input[::-1]}"
