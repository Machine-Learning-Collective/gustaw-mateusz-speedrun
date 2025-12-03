from typing import Dict, List, Optional

from langchain.agents import create_agent
from langchain.tools import BaseTool
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.language_models.chat_models import BaseChatModel

from Pydantic_Base_Models import ConversationConfig, Message, Role

class ChatModelError(Exception):
    """Raised when the underlying chat model call fails."""
    pass


class LangChainAgent:
    def __init__(
        self,
        model: BaseChatModel,
        tools: Optional[List[BaseTool]] = None,
        config: Optional[ConversationConfig] = None,
    ) -> None:
        self.config = config or ConversationConfig()
        self.model = model
        self.tools = tools or []
        self._store: Dict[str, ChatMessageHistory] = {}

        self._agent = create_agent(
            model=self.model,
            tools=self.tools,
            system_prompt=self.config.system_prompt,
        )

    # --- wewnętrzna historia LangChain ---
    def _get_history(self, session_id: str) -> ChatMessageHistory:
        if session_id not in self._store:
            self._store[session_id] = ChatMessageHistory()
        return self._store[session_id]

    # --- główna metoda: wysyłamy input, budujemy pełne messages i zapisujemy historię ---
    def send(self, user_input: str, session_id: str = "default") -> str:
        history = self._get_history(session_id)

        messages = []
        for m in history.messages:
            if m.type == "human":
                role = "user"
            elif m.type == "ai":
                role = "assistant"
            else:
                role = "system"
            messages.append({"role": role, "content": m.content})

        messages.append({"role": "user", "content": user_input})

        try:
            result = self._agent.invoke({"messages": messages})
        except Exception as e:
            raise ChatModelError("LLM call failed") from e

        reply = self._extract_reply(result)

        history.add_user_message(user_input)
        history.add_ai_message(reply)

        self._trim_history(session_id=session_id)

        return reply

    def _extract_reply(self, result) -> str:
        # typowy format: {"messages": [AIMessage(...), ...]}
        if isinstance(result, dict) and "messages" in result:
            msgs = result["messages"]
            if isinstance(msgs, list) and msgs:
                last = msgs[-1]
                if hasattr(last, "content"):
                    return last.content
                if isinstance(last, dict) and "content" in last:
                    return last["content"]

        if isinstance(result, dict) and "output" in result:
            return result["output"]

        return str(result)

    def _trim_history(self, session_id: str) -> None:
        max_messages = self.config.max_history_messages
        if max_messages <= 0:
            return
        history = self._get_history(session_id)
        messages = history.messages
        if len(messages) > max_messages:
            excess = len(messages) - max_messages
            history.messages = messages[excess:]

    # --- publiczna historia jako Pydantic List[Message] ---
    def get_history(self, session_id: str = "default") -> List[Message]:
        history = self._get_history(session_id).messages
        result: List[Message] = []
        for m in history:
            if m.type == "human":
                role = Role.user
            elif m.type == "ai":
                role = Role.assistant
            else:
                role = Role.system
            result.append(Message(role=role, content=m.content))
        return result

    def reset(self, session_id: str = "default") -> None:
        if session_id in self._store:
            self._store[session_id].clear()

    def has_session(self, session_id: str) -> bool:
        return session_id in self._store
