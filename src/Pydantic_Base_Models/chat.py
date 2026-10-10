# core_models/chat.py
from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from .config import ConversationConfig

# Limit for what a person can send. Model replies are not capped: a real LLM can easily
# answer with more than 4000 characters, and rejecting its reply would crash the conversation.
MAX_USER_MESSAGE_CHARS = 4000


class Role(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"


class Message(BaseModel):
    role: Role
    content: str = Field(min_length=1)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("content")
    @classmethod
    def strip_content(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("content must not be empty")
        return v

    @model_validator(mode="after")
    def limit_user_content(self) -> "Message":
        if self.role is Role.user and len(self.content) > MAX_USER_MESSAGE_CHARS:
            raise ValueError(f"user messages are limited to {MAX_USER_MESSAGE_CHARS} characters")
        return self


class ChatTurn(BaseModel):
    user: Message
    assistant: Message


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=128)
    message: Message
    config_overrides: Optional[ConversationConfig] = None

    @field_validator("message")
    @classmethod
    def message_from_user(cls, v: Message) -> Message:
        if v.role is not Role.user:
            raise ValueError("only user messages can be sent")
        return v


class ChatResponse(BaseModel):
    session_id: str
    message: Message
    history: List[Message] = Field(default_factory=list)
