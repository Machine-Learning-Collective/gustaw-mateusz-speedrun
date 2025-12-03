# agent_models.py / pydantic_models.py

from typing import Literal
from pydantic import BaseModel, Field


class ConversationConfig(BaseModel):
    system_prompt: str = Field(
        default="You are a helpful conversational assistant.",
        min_length=1,
        max_length=4000,
    )
    locale: Literal["en", "pl"] = "en"

    memory_key: str = Field(default="history", min_length=1, max_length=64)
    input_key: str = Field(default="input", min_length=1, max_length=64)
    max_history_messages: int = Field(default=20, ge=0, le=500)

    model_name: str = Field(default="gpt-4o-mini", min_length=1, max_length=128)
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    enable_memory: bool = True
    mode: Literal["llm", "rag", "tools"] = "llm"
