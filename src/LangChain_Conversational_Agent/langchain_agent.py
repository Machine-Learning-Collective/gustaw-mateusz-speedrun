from typing import Dict, List, Optional

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

from Pydantic_Base_Models import ConversationConfig, Message, Role


class LangChainAgent:
    def __init__(
        self,
        llm: BaseChatModel,
        config: Optional[ConversationConfig] = None,
    ) -> None:
        self.config = config or ConversationConfig()
        self.llm = llm
        self._store: Dict[str, ChatMessageHistory] = {}

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.config.system_prompt),
                MessagesPlaceholder(self.config.memory_key),
                ("human", "User: {" + self.config.input_key + "}"),
            ]
        )

        chain = prompt | self.llm

        self._chain = RunnableWithMessageHistory(
            chain,
            self._get_history,
            input_messages_key=self.config.input_key,
            history_messages_key=self.config.memory_key,
        )

    def _get_history(self, session_id: str) -> ChatMessageHistory:
        if session_id not in self._store:
            self._store[session_id] = ChatMessageHistory()
        return self._store[session_id]

    def send(self, user_input: str, session_id: str = "default") -> str:
        result = self._chain.invoke(
            {self.config.input_key: user_input},
            config={"configurable": {"session_id": session_id}},
        )
        self._trim_history(session_id=session_id)
        return result.content

    def _trim_history(self, session_id: str) -> None:
        max_messages = self.config.max_history_messages
        if max_messages <= 0:
            return
        history = self._get_history(session_id)
        messages = history.messages
        if len(messages) > max_messages:
            excess = len(messages) - max_messages
            history.messages = messages[excess:]

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


if __name__ == "__main__":
    from langchain_community.chat_models.fake import FakeListChatModel

    responses = [
        "Hello, how can I help you?",
        "I see.",
        "Can you tell me more?",
        "Thanks for sharing.",
    ]
    llm = FakeListChatModel(responses=responses)
    agent = LangChainAgent(llm=llm, config=ConversationConfig())

    session_id = "cli"
    print("Type 'exit' to quit.")
    while True:
        try:
            text = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye")
            break
        if text.lower() in {"exit", "quit"}:
            print("bye")
            break
        if not text:
            print("agent> Please say something.")
            continue
