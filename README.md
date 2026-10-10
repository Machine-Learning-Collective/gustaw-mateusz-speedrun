# Personal Chatbot

A conversational chatbot built in **ML Kolektyw** (Machine Learning Collective, PJATK) by Gustaw Pluta ([@GustawP](https://github.com/GustawP)) and Mateusz ([@mmalimon](https://github.com/mmalimon)).

The project is deliberately built in stages: every technology is researched and validated before any code is written, and every component is built and tested in isolation before the pieces are connected.

## Stack

| Layer | Technology | Role |
|---|---|---|
| Conversation logic | **LangChain** | Prompt template, per-session memory, model abstraction |
| Data contracts | **Pydantic v2** | Validated models for every message crossing a component boundary |
| UI | **Streamlit** | Chat interface |
| API | **FastAPI** | HTTP layer |
| Tests | **pytest** | One test suite per component |
| Environment | **uv**, Python 3.13 | Dependency management and lock file |

## Status

| Milestone | Scope | Status |
|---|---|---|
| 1 | Research and technology validation | ✅ Done |
| 2 | Isolated components | ✅ Done |
| 3 | Integration and demo | ⏳ Next |
| 4 | Reflection and handoff | – |

The components exist and pass their tests, but are not yet connected. The agent currently runs against a scripted test model, and the UI against a mock responder; wiring them together with a real LLM is Milestone 3.

## Components

```
src/
├── Pydantic_Base_Models/            Message, ChatRequest, ChatResponse, ConversationConfig
├── LangChain_Conversational_Agent/  LangChainAgent: prompt + per-session history + trimming
├── Streamlit_Interface/             Chat UI shell with a pluggable responder
└── FastApi_Skeleton/                FastAPI app with a /health endpoint
```

**Data models.** Every message is a `Message` with a role, timestamp and validated content (1–4000 characters, whitespace-only rejected). `ConversationConfig` holds the system prompt, history length limit and locale (`en`/`pl`). Raw dicts never cross component boundaries.

**Agent.** `LangChainAgent` takes any LangChain chat model, so the provider can be swapped without touching the rest of the code. It keeps a separate history per session through `RunnableWithMessageHistory` and trims it to `max_history_messages` after each turn.

**UI.** The Streamlit shell takes the reply function as a dependency. Today that is a mock; in Milestone 3 it becomes the agent.

**API.** A FastAPI app with a typed `/health` endpoint, as the base for a `/chat` route.

## Research (Milestone 1)

Before writing code, each part of the stack was researched against official documentation and the version set was validated for conflicts. The findings and decisions are in [`docs/`](docs/):

| Document | Covers |
|---|---|
| [milestone-1-research.md](docs/milestone-1-research.md) | Overview of all decisions: LLM provider, versions, testing strategy, architecture |
| [langchain-core-abstractions.md](docs/langchain-core-abstractions.md) | Chat models, prompts, runnables, memory |
| [pydantic-message-handling.md](docs/pydantic-message-handling.md) | Message models, validation, serialization |
| [streamlit-chat-ui-interaction.md](docs/streamlit-chat-ui-interaction.md) | Chat elements, session state, rerun model |
| [version-compatibility-validation.md](docs/version-compatibility-validation.md) | Version matrix, dependency resolution, known conflicts |

The original project brief is kept in [docs/project-brief.md](docs/project-brief.md).

## Running it

```bash
uv sync

# Tests
uv run pytest

# Agent in the terminal (scripted test model, no API key needed)
uv run python -m LangChain_Conversational_Agent.cli

# Chat UI (mock responder)
uv run streamlit run src/Streamlit_Interface/app.py

# API
uv run uvicorn FastApi_Skeleton.main:app --app-dir src
```

## Team

| | Role |
|---|---|
| Gustaw Pluta | Research and technology validation (Milestone 1), project lead |
| Mateusz (@mmalimon) | Isolated components and tests (Milestone 2) |

Work happens on milestone branches and is merged through reviewed pull requests.
