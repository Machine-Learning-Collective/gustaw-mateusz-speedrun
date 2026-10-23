"""Choosing and building the language model from configuration.

Provider selection, in order:
1. `LLM_PROVIDER` if set (`openai` or `demo`)
2. `openai` if `OPENAI_API_KEY` is set
3. `demo` otherwise, so the app always starts, even without an API key
"""
import os
from typing import Any, List, Literal, Mapping, Optional

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from pydantic import BaseModel, Field

Provider = Literal["openai", "demo"]

DEFAULT_OPENAI_MODEL = "gpt-5-mini"


class LLMSettings(BaseModel):
    provider: Provider = "demo"
    model: str = Field(default=DEFAULT_OPENAI_MODEL, min_length=1)
    # None means "use the model's default". Some OpenAI models (the GPT-5 family among them)
    # accept only their default temperature and reject any explicit value.
    temperature: Optional[float] = Field(default=None, ge=0, le=2)
    timeout_seconds: float = Field(default=60, gt=0)

    @classmethod
    def from_env(cls, env: Optional[Mapping[str, str]] = None) -> "LLMSettings":
        env = os.environ if env is None else env
        provider = env.get("LLM_PROVIDER", "").strip().lower()
        if not provider:
            provider = "openai" if env.get("OPENAI_API_KEY") else "demo"

        values: dict[str, Any] = {"provider": provider}
        if env.get("OPENAI_MODEL"):
            values["model"] = env["OPENAI_MODEL"].strip()
        if env.get("LLM_TEMPERATURE"):
            values["temperature"] = float(env["LLM_TEMPERATURE"])
        if env.get("LLM_TIMEOUT_SECONDS"):
            values["timeout_seconds"] = float(env["LLM_TIMEOUT_SECONDS"])
        return cls(**values)

    def describe(self) -> str:
        return f"openai ({self.model})" if self.provider == "openai" else "demo"


class DemoChatModel(BaseChatModel):
    """Stand-in model for running the app without an API key.

    It does not generate language; it repeats the last message and reports how much of the
    conversation it received, which shows that history is passed to the model on every turn.
    """

    @property
    def _llm_type(self) -> str:
        return "demo"

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> ChatResult:
        user_messages = [m for m in messages if isinstance(m, HumanMessage)]
        last = user_messages[-1].text if user_messages else ""
        earlier = len(user_messages) - 1
        text = (
            f'Demo mode, no language model connected. You said: "{last}". '
            f"I can see {earlier} earlier message{'' if earlier == 1 else 's'} from you in this conversation."
        )
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=text))])


def build_llm(settings: LLMSettings, env: Optional[Mapping[str, str]] = None) -> BaseChatModel:
    env = os.environ if env is None else env
    if settings.provider == "demo":
        return DemoChatModel()

    api_key = env.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("LLM_PROVIDER is 'openai' but OPENAI_API_KEY is not set")

    from langchain_openai import ChatOpenAI

    kwargs: dict[str, Any] = {
        "model": settings.model,
        "api_key": api_key,
        "timeout": settings.timeout_seconds,
        "max_retries": 2,
    }
    if settings.temperature is not None:
        kwargs["temperature"] = settings.temperature
    return ChatOpenAI(**kwargs)
