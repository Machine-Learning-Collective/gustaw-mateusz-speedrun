from typing import Dict, List, Optional

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from Pydantic_Base_Models import ConversationConfig, Message, Role

# session_id -> messages of that session, oldest first
HistoryStore = Dict[str, List[Message]]


def to_langchain(message: Message) -> BaseMessage:
    if message.role is Role.user:
        return HumanMessage(content=message.content)
    if message.role is Role.assistant:
        return AIMessage(content=message.content)
    return SystemMessage(content=message.content)


class LangChainAgent:
    """Conversational agent with per-session memory.

    History is kept as the project's own Pydantic `Message` objects, so it is validated when a
    message is created rather than when it is read back, and converted to LangChain messages only
    for the model call. (LangChain's `RunnableWithMessageHistory` and `InMemoryChatMessageHistory`,
    used in Milestone 2, are deprecated as of langchain-core 1.6.)

    Several agents can share one `history_store`, which lets a session keep its history when a
    request switches to a different configuration.
    """

    def __init__(
        self,
        llm: BaseChatModel,
        config: Optional[ConversationConfig] = None,
        history_store: Optional[HistoryStore] = None,
    ) -> None:
        self.config = config or ConversationConfig()
        self.llm = llm
        self._store: HistoryStore = history_store if history_store is not None else {}

        # The system prompt is passed as a message object, not a template string, so braces
        # typed into it (e.g. "Answer in {JSON}") are not mistaken for template variables.
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=self.config.system_prompt),
                MessagesPlaceholder(self.config.memory_key),
                ("human", "{" + self.config.input_key + "}"),
            ]
        )
        self._chain = prompt | self.llm

    def _get_history(self, session_id: str) -> List[Message]:
        return self._store.setdefault(session_id, [])

    def send(self, user_input: str, session_id: str = "default") -> str:
        """Sends a user message and returns the model's reply.

        Raises `ValueError` (a pydantic `ValidationError`) for empty or over-long input, before the
        model is called and without touching the history. If the model call fails, the history is
        left unchanged too, so a retry does not duplicate the user's message.
        """
        user_message = Message(role=Role.user, content=user_input)
        history = self._get_history(session_id)

        result = self._chain.invoke(
            {
                self.config.input_key: user_message.content,
                self.config.memory_key: [to_langchain(m) for m in history],
            }
        )

        reply_text = result.text.strip() if isinstance(result, BaseMessage) else str(result).strip()
        if not reply_text:
            raise RuntimeError("the language model returned an empty reply")
        reply = Message(role=Role.assistant, content=reply_text)

        history.extend([user_message, reply])
        self._trim_history(session_id)
        return reply.content

    def _trim_history(self, session_id: str) -> None:
        max_messages = self.config.max_history_messages
        if max_messages <= 0:
            return
        history = self._get_history(session_id)
        if len(history) > max_messages:
            del history[: len(history) - max_messages]

    def get_history(self, session_id: str = "default") -> List[Message]:
        return list(self._store.get(session_id, []))

    def reset(self, session_id: str = "default") -> None:
        if session_id in self._store:
            self._store[session_id].clear()

    def has_session(self, session_id: str) -> bool:
        return session_id in self._store
