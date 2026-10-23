import os
from typing import Any, List, Optional

# Tests must never call a paid API, even if a developer has OPENAI_API_KEY in their .env.
# load_dotenv() does not override variables that are already set, so this wins.
os.environ["LLM_PROVIDER"] = "demo"

import pytest  # noqa: E402
from langchain_core.language_models.chat_models import BaseChatModel  # noqa: E402
from langchain_core.messages import AIMessage, BaseMessage  # noqa: E402
from langchain_core.outputs import ChatGeneration, ChatResult  # noqa: E402


class RecordingChatModel(BaseChatModel):
    """Returns scripted replies in turn and records every prompt it receives."""

    responses: List[str] = ["ok"]
    calls: List[List[BaseMessage]] = []
    index: int = 0

    @property
    def _llm_type(self) -> str:
        return "recording"

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> ChatResult:
        self.calls.append(list(messages))
        text = self.responses[self.index % len(self.responses)]
        self.index += 1
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=text))])


class FailingChatModel(BaseChatModel):
    """Simulates a provider outage."""

    @property
    def _llm_type(self) -> str:
        return "failing"

    def _generate(self, messages: List[BaseMessage], stop=None, run_manager=None, **kwargs: Any) -> ChatResult:
        raise ConnectionError("provider unavailable")


@pytest.fixture
def recording_llm() -> RecordingChatModel:
    return RecordingChatModel(responses=["first reply", "second reply", "third reply"], calls=[])
