# core_models/chat.py
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from .config import ConversationConfig


class Role(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"


class Message(BaseModel):
    role: Role
    content: str = Field(min_length=1, max_length=4000)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("content")
    @classmethod
    def strip_content(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("content must not be empty")
        return v


class ChatTurn(BaseModel):
    user: Message
    assistant: Message


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=128)
    message: Message
    config_overrides: Optional[ConversationConfig] = None


class ChatResponse(BaseModel):
    session_id: str
    message: Message
    history: List[Message] = Field(default_factory=list)
