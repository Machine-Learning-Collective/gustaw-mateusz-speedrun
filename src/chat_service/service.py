import threading
from typing import Dict, List, Optional

from langchain_core.language_models.chat_models import BaseChatModel

from langchain_conversational_agent.langchain_agent import HistoryStore, LangChainAgent
from langchain_conversational_agent.llm_factory import LLMSettings, build_llm
from pydantic_base_models import ChatRequest, ChatResponse, ConversationConfig, Message


class ChatService:
    """The single entry point that both the API and the UI talk to.

    Speaks only in Pydantic models (`ChatRequest` in, `ChatResponse` out), so no raw dicts cross
    component boundaries. One agent is kept per distinct configuration, and all agents share one
    history store, so a session keeps its history when a request overrides the configuration.
    """

    def __init__(
        self,
        llm: BaseChatModel,
        default_config: Optional[ConversationConfig] = None,
        llm_description: str = "custom",
    ) -> None:
        self.llm = llm
        self.default_config = default_config or ConversationConfig()
        self.llm_description = llm_description
        self._history: HistoryStore = {}
        self._agents: Dict[str, LangChainAgent] = {}
        self._agents_lock = threading.Lock()
        self._session_locks: Dict[str, threading.Lock] = {}
        self._session_locks_guard = threading.Lock()

    @classmethod
    def from_settings(
        cls, settings: LLMSettings, default_config: Optional[ConversationConfig] = None
    ) -> "ChatService":
        return cls(build_llm(settings), default_config, settings.describe())

    def _agent_for(self, config: ConversationConfig) -> LangChainAgent:
        key = config.model_dump_json()
        with self._agents_lock:
            if key not in self._agents:
                self._agents[key] = LangChainAgent(self.llm, config, history_store=self._history)
            return self._agents[key]

    def _lock_for(self, session_id: str) -> threading.Lock:
        with self._session_locks_guard:
            return self._session_locks.setdefault(session_id, threading.Lock())

    def chat(self, request: ChatRequest) -> ChatResponse:
        agent = self._agent_for(request.config_overrides or self.default_config)
        # Turns of one session run one at a time, so two concurrent requests cannot
        # interleave their messages; different sessions still run in parallel.
        with self._lock_for(request.session_id):
            agent.send(request.message.content, session_id=request.session_id)
            history = agent.get_history(request.session_id)
        return ChatResponse(session_id=request.session_id, message=history[-1], history=history)

    def has_session(self, session_id: str) -> bool:
        return session_id in self._history

    def get_history(self, session_id: str) -> List[Message]:
        return list(self._history.get(session_id, []))

    def reset(self, session_id: str) -> None:
        with self._lock_for(session_id):
            self._history.pop(session_id, None)
