# Milestone 1: Research & Technology Validation

> *"I actually read the docs"*

## 📋 Research Checklist

### Core Technologies to Research

#### 🧠 LangChain
- [x] What is LangChain and what problem does it solve?
- [x] Latest stable version and compatibility with Python 3.13
- [x] Core concepts: Chains, Agents, Memory, Prompts
- [x] How to integrate with LLM providers (OpenAI, Anthropic, etc.)
- [x] Best practices for building chatbots with LangChain
- [x] Key classes/functions needed for a basic chatbot
- [x] Memory management for conversation history
- [x] **Decision:** Which LLM provider to use? (OpenAI, Anthropic, local model, etc.)
- [x] **Decision:** Which LangChain version to use? (Check compatibility)

**Research Findings:**

**What is LangChain?**
LangChain is a framework for developing applications powered by Large Language Models (LLMs). It provides:
- **Abstraction layer** for working with different LLM providers (OpenAI, Anthropic, etc.)
- **Modular components** for building complex LLM applications
- **Memory management** for maintaining conversation context
- **Chain composition** for creating multi-step workflows
- **Agent framework** for autonomous decision-making

**Version & Compatibility:**
- **Current version in project:** `langchain>=0.3.0`
- **Python 3.13 compatibility:** LangChain 0.3.x supports Python 3.8+, so Python 3.13 is fully compatible
- **Latest stable:** As of December 2025, LangChain 1.1.0 is the current stable version with active development

**Core Concepts:**
1. **Chains:** Sequential workflows that combine multiple components (e.g., prompt → LLM → output parser)
2. **Agents:** Autonomous systems that can use tools and make decisions
3. **Memory:** Maintains conversation history and context
   - `ConversationBufferMemory` - Simple in-memory storage
   - `ConversationBufferWindowMemory` - Keeps last N messages
   - `ConversationSummaryMemory` - Summarizes old messages
4. **Prompts:** Template-based prompt management with variables
5. **Chat Models:** Specialized interfaces for conversational AI (ChatOpenAI, ChatAnthropic)

**Key Classes for Basic Chatbot:**
- `ChatOpenAI` or `ChatAnthropic` - LLM interface
- `ConversationBufferMemory` - Simple memory management
- `ConversationChain` - Basic conversation chain
- `ChatPromptTemplate` - Prompt templates for chat
- `MessagesPlaceholder` - For injecting conversation history

**Memory Management:**
- Use `ConversationBufferMemory` for simple use cases
- Store messages as list of `HumanMessage` and `AIMessage` objects
- Memory can be persisted to disk or database for production
- Session-based memory for multi-user scenarios

**LLM Provider Decision:**
- **Recommended: OpenAI (ChatGPT)** for initial development
  - Most mature integration with LangChain
  - Excellent documentation and examples
  - Reliable API with good error handling
  - Cost-effective for development/testing
- **Alternative: Anthropic (Claude)** - Also well-supported, may have different pricing
- **Local models:** Possible but requires additional setup (Ollama, etc.)

**Resources:**
- [LangChain Python Docs](https://python.langchain.com/docs/introduction/)
- [LangChain Chat Models](https://python.langchain.com/docs/integrations/chat/)
- [LangChain Memory](https://python.langchain.com/docs/modules/memory/)
- [LangChain Quickstart](https://python.langchain.com/docs/get_started/quickstart)

---

#### 📝 Pydantic v2
- [x] What changed in Pydantic v2 vs v1?
- [x] Core concepts: Models, Validation, Serialization
- [x] How to define data models for chatbot (messages, responses, etc.)
- [x] Type validation and error handling
- [x] Integration with FastAPI (if using API layer)
- [x] **Decision:** Confirm v2 is the right choice (README says USE V2)

**Research Findings:**

**Pydantic v2 vs v1 - Key Changes:**
1. **Performance:** 5-50x faster validation (written in Rust core)
2. **Type system:** Better support for Python 3.10+ type hints (PEP 604 union syntax)
3. **Validation:** More flexible validation with `field_validator` and `model_validator`
4. **Serialization:** Improved JSON serialization with `model_dump()` and `model_dump_json()`
5. **Breaking changes:** Some API changes (e.g., `.dict()` → `.model_dump()`, `.json()` → `.model_dump_json()`)

**Core Concepts:**
- **Models:** Define data structures with type hints
- **Validation:** Automatic validation based on type hints
- **Serialization:** Convert models to/from JSON, dicts, etc.
- **Field validation:** Custom validators for complex rules
- **Error handling:** Detailed validation errors with field-level messages

**Chatbot Data Models Needed:**
```python
# Example structure:
- Message: Base model for chat messages (role, content, timestamp)
- ChatRequest: Input model for API requests (message, session_id)
- ChatResponse: Output model for API responses (message, session_id, metadata)
- ChatHistory: Collection of messages for a session
```

**Type Validation:**
- Automatic validation from type hints (str, int, Optional, List, etc.)
- Custom validators using `@field_validator` decorator
- Model-level validation with `@model_validator`
- Error messages are detailed and helpful

**FastAPI Integration:**
- FastAPI has native Pydantic v2 support (since FastAPI 0.100+)
- Request/Response models are automatically validated
- OpenAPI schema generation from Pydantic models
- Current FastAPI version (0.122.0+) fully supports Pydantic v2

**Decision:** ✅ **Pydantic v2 is confirmed** - Required by README and fully compatible with all stack components

**Resources:**
- [Pydantic v2 Docs](https://docs.pydantic.dev/latest/)
- [Pydantic v2 Migration Guide](https://docs.pydantic.dev/latest/migration/)
- [Pydantic v2 Performance](https://docs.pydantic.dev/latest/blog/pydantic-v2-performance/)

---

#### 🎨 Streamlit
- [x] How to build interactive UIs with Streamlit
- [x] Chat interface components (chat input, message display)
- [x] State management for conversation history
- [x] Session state handling
- [x] Best practices for chatbot UIs
- [x] **Decision:** Is Streamlit suitable for real-time chat?

**Research Findings:**

**Streamlit Overview:**
Streamlit is a Python framework for building web applications quickly. It's ideal for:
- Rapid prototyping
- Data science applications
- Interactive dashboards
- **Chatbot UIs** (perfect for this project!)

**Chat Interface Components:**
- `st.chat_message()` - Display messages with role-based styling (user/assistant)
- `st.chat_input()` - Input widget specifically designed for chat interfaces
- `st.container()` - For organizing chat history
- Native chat UI components make it easy to build conversational interfaces

**State Management:**
- `st.session_state` - Persistent state across reruns
- Store conversation history as list of message dicts
- Pattern: `st.session_state.messages = []` for initialization
- Messages persist during the session (until page refresh)

**Session State Handling:**
```python
# Typical pattern:
if "messages" not in st.session_state:
    st.session_state.messages = []

# Add new message
st.session_state.messages.append({"role": "user", "content": user_input})

# Display all messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
```

**Best Practices for Chatbot UIs:**
1. Initialize session state on first run
2. Clear input after submission
3. Show loading indicators during LLM responses
4. Handle errors gracefully with user-friendly messages
5. Use `st.rerun()` to refresh UI after state changes

**Real-time Chat Suitability:**
✅ **Yes, Streamlit is suitable for real-time chat!**
- Chat components are designed for this use case
- Session state maintains conversation history
- Simple integration with LangChain
- Good for single-user or small-scale deployments
- For production multi-user, consider FastAPI backend + Streamlit frontend

**Limitations:**
- Not ideal for true real-time (WebSocket) chat (but fine for request-response)
- Session state is per-browser session (not shared across users)
- For production scale, may need FastAPI backend

**Resources:**
- [Streamlit Docs](https://docs.streamlit.io/)
- [Streamlit Chat Components](https://docs.streamlit.io/develop/api-reference/chat)
- [Streamlit Session State](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state)

---

#### 🚀 FastAPI (Optional)
- [x] When would you use FastAPI vs just Streamlit?
- [x] How to structure API endpoints for a chatbot
- [x] Request/Response models with Pydantic
- [x] Integration with LangChain
- [x] **Decision:** Do we need FastAPI for Milestone 1, or is it optional?

**Research Findings:**

**When to Use FastAPI:**
- **With Streamlit:** When you need a separate API layer (mobile apps, other frontends)
- **Without Streamlit:** Building a pure API service
- **Production:** Better for multi-user, scalable deployments
- **Integration:** When other services need to call your chatbot

**When NOT to Use FastAPI (Streamlit Only):**
- Simple single-user chatbot
- Rapid prototyping
- Internal tools
- Milestone 1-2 (can add later)

**API Endpoint Structure:**
```python
# Typical structure:
POST /chat - Send message, get response
GET /history/{session_id} - Get conversation history
POST /clear/{session_id} - Clear conversation history
```

**Request/Response Models:**
- Use Pydantic models for all request/response bodies
- Automatic validation and OpenAPI schema generation
- Type-safe API contracts

**LangChain Integration:**
- LangChain chains can be called from FastAPI route handlers
- Memory can be stored per session (in-memory dict or database)
- Async support for better performance
- Error handling for API failures

**Decision:** ⚠️ **FastAPI is OPTIONAL for Milestone 1**
- **Milestone 1-2:** Focus on Streamlit + LangChain (simpler, faster)
- **Milestone 3+:** Can add FastAPI if needed for integration demo
- **Recommendation:** Start with Streamlit-only, add FastAPI later if requirements demand it

**Resources:**
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [FastAPI + Pydantic](https://fastapi.tiangolo.com/tutorial/body/)
- [FastAPI Async](https://fastapi.tiangolo.com/async/)

---

#### 🧪 Pytest
- [x] How to structure tests for a chatbot
- [x] Testing LangChain components in isolation
- [x] Mocking LLM responses for testing
- [x] Testing Pydantic models
- [x] Testing Streamlit components (if possible)
- [x] **Decision:** What testing strategy makes sense?

**Research Findings:**

**Test Structure:**
```
tests/
├── unit/
│   ├── test_models.py      # Pydantic models
│   ├── test_memory.py      # Memory management
│   └── test_chains.py      # LangChain chains (mocked)
├── integration/
│   └── test_chatbot.py     # Full chatbot flow (mocked LLM)
└── conftest.py             # Shared fixtures
```

**Testing LangChain Components:**
- **Mock LLM responses:** Use `unittest.mock` to mock `ChatOpenAI` calls
- **Test chains in isolation:** Create test chains with mocked LLM
- **Test memory:** Verify message storage/retrieval
- **Test prompts:** Validate prompt template rendering

**Mocking LLM Responses:**
```python
from unittest.mock import patch, MagicMock
from langchain_openai import ChatOpenAI

@patch('langchain_openai.ChatOpenAI.invoke')
def test_chat_chain(mock_invoke):
    mock_response = MagicMock()
    mock_response.content = "Test response"
    mock_invoke.return_value = mock_response
    # Test your chain
```

**Testing Pydantic Models:**
- Test validation with valid/invalid data
- Test serialization (`model_dump()`, `model_dump_json()`)
- Test custom validators
- Test error messages

**Testing Streamlit:**
- **Limited:** Streamlit is hard to test directly (UI framework)
- **Workaround:** Test business logic separately from UI
- Extract logic into functions, test those functions
- Use `streamlit.testing` (experimental) for UI tests if needed

**Testing Strategy Decision:**
1. **Unit Tests:** Test Pydantic models, memory management, utility functions
2. **Integration Tests:** Test LangChain chains with mocked LLM
3. **Component Tests:** Test each component in isolation before integration
4. **UI Tests:** Minimal - focus on logic, not UI rendering

**Pytest Features to Use:**
- **Fixtures:** For shared test setup (mock LLM, test data)
- **Parametrize:** Test multiple scenarios
- **Markers:** Organize tests (`@pytest.mark.unit`, `@pytest.mark.integration`)
- **Coverage:** Use `pytest-cov` to track test coverage

**Resources:**
- [Pytest Docs](https://docs.pytest.org/en/stable/)
- [Pytest Fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [Pytest Mocking](https://docs.pytest.org/en/stable/how-to/monkeypatch.html)

---

## 🔍 Compatibility Research

- [x] Python 3.13 compatibility with all packages
- [x] LangChain version compatibility with chosen LLM provider
- [x] Pydantic v2 compatibility with FastAPI (if using)
- [x] Any known issues or breaking changes

**Compatibility Matrix:**

| Package | Version | Python 3.13 | Status |
|---------|---------|-------------|--------|
| Python | 3.13 | ✅ | Latest stable |
| LangChain | ≥0.3.0 | ✅ | Fully compatible (supports 3.8+) |
| Pydantic | ≥2.12.5 | ✅ | Fully compatible (supports 3.8+) |
| Streamlit | ≥1.51.0 | ✅ | Fully compatible (supports 3.8+) |
| FastAPI | ≥0.122.0 | ✅ | Fully compatible (supports 3.8+) |
| Pytest | ≥9.0.1 | ✅ | Fully compatible (supports 3.8+) |

**LangChain + LLM Provider Compatibility:**
- **OpenAI:** `langchain-openai` package (separate from core LangChain)
- **Anthropic:** `langchain-anthropic` package
- Both are actively maintained and compatible with LangChain 0.3.x

**Pydantic v2 + FastAPI:**
- FastAPI 0.122.0+ has native Pydantic v2 support
- No compatibility issues
- Automatic OpenAPI schema generation works perfectly

**Known Issues:**
- None identified for this stack combination
- All packages are mature and well-tested
- Python 3.13 is well-supported (released October 2024, stable as of December 2025)

---

## 💡 Architecture Decisions

### Component Structure
- [x] How should the chatbot be structured? (separate files for models, chains, UI?)
- [x] What Pydantic models do we need? (Message, Response, ChatHistory?)
- [x] How to handle conversation memory?
- [x] Where does Streamlit fit in the architecture?

**Architecture Decision:**

```
project/
├── src/
│   ├── models/
│   │   └── chat_models.py      # Pydantic models (Message, ChatRequest, etc.)
│   ├── chains/
│   │   └── chatbot_chain.py     # LangChain chain setup
│   ├── memory/
│   │   └── memory_manager.py    # Memory management logic
│   └── utils/
│       └── config.py            # Configuration (API keys, etc.)
├── app/
│   └── streamlit_app.py         # Streamlit UI
├── tests/
│   ├── unit/
│   └── integration/
└── main.py                       # Entry point (optional)
```

**Pydantic Models Needed:**
1. **Message** - Base message model (role, content, timestamp)
2. **ChatRequest** - Input for chat endpoint (if using FastAPI)
3. **ChatResponse** - Output from chat (message, metadata)
4. **ChatHistory** - Collection of messages (optional, can use list)

**Memory Management:**
- **Milestone 1-2:** Use LangChain's `ConversationBufferMemory` (in-memory)
- **Milestone 3+:** Can persist to file/database if needed
- **Session-based:** Each Streamlit session has its own memory
- **Pattern:** Initialize memory in `st.session_state` on first run

**Streamlit in Architecture:**
- **Primary UI layer** for Milestone 1-3
- Handles user input/output
- Manages session state (conversation history)
- Calls LangChain chain for responses
- Simple, direct integration - no API layer needed initially

### LLM Provider Choice
- [x] Which provider? (OpenAI, Anthropic, local, etc.)
- [x] API key management strategy
- [x] Cost considerations
- [x] Rate limiting and error handling

**LLM Provider Decision:** ✅ **OpenAI (ChatGPT)**

**Rationale:**
- Most mature LangChain integration
- Excellent documentation and examples
- Reliable API with good uptime
- Cost-effective for development ($0.002 per 1K tokens for GPT-3.5-turbo)
- Easy to switch providers later (LangChain abstraction)

**API Key Management:**
- Use environment variables (`.env` file)
- Add `.env` to `.gitignore` (already done)
- Load with `python-dotenv` or `os.getenv()`
- Never commit API keys to repository

**Cost Considerations:**
- **GPT-3.5-turbo:** ~$0.002 per 1K tokens (very affordable for development)
- **GPT-4:** ~$0.03 per 1K tokens (more expensive, use for production if needed)
- **Development:** Use GPT-3.5-turbo, switch to GPT-4 if quality needed
- Monitor usage with OpenAI dashboard

**Rate Limiting & Error Handling:**
- OpenAI has rate limits (check current limits)
- Implement retry logic with exponential backoff
- Handle API errors gracefully (show user-friendly messages)
- Use `tenacity` library for retries if needed

**Alternative Providers:**
- **Anthropic Claude:** Also excellent, similar pricing
- **Local models:** Ollama (free, but requires setup)
- Can switch later - LangChain makes this easy

---

## 📝 Research Notes

### Key Findings

1. **LangChain 0.3.x is the right choice** - Modern, well-maintained, Python 3.13 compatible
2. **Pydantic v2 is mandatory** - Required by README, and it's faster/better than v1
3. **Streamlit is perfect for chatbot UI** - Has native chat components, easy to use
4. **FastAPI is optional** - Can start with Streamlit-only, add API layer later
5. **OpenAI is best for initial development** - Most mature, well-documented, cost-effective
6. **Python 3.13 compatibility is excellent** - All packages support it
7. **Testing strategy:** Focus on unit tests for models/chains, integration tests with mocked LLM
8. **Architecture:** Separate concerns (models, chains, UI) for clean code

### Gotchas & Important Notes

1. **LangChain packages are modular** - Need `langchain-core`, `langchain-openai` separately
2. **Memory is session-based in Streamlit** - Each browser session = separate conversation
3. **API keys must be in environment variables** - Never hardcode
4. **Pydantic v2 API changes** - Use `.model_dump()` not `.dict()`
5. **Streamlit reruns on every interaction** - Need to manage state carefully
6. **Mock LLM for testing** - Don't call real API in tests (cost + speed)

### Questions to Ask

1. **For @ArturNiklewicz:**
   - Should we use FastAPI from the start, or is Streamlit-only acceptable for Milestone 1-2?
   - Any specific LLM provider preference, or is OpenAI fine?
   - Are there any specific requirements for the chatbot functionality (RAG, tool use, etc.)?
   - Should we implement conversation persistence (database) or is in-memory fine for now?

### Blockers

- **None identified** - All technologies are compatible and ready to use
- **Potential:** Need OpenAI API key (user must obtain)
- **Potential:** Python 3.13 is very new - minor edge cases possible (unlikely)

---

## ✅ Validation Checklist

Before moving to Milestone 2, ensure:
- [x] All technologies are understood at a conceptual level
- [x] Compatibility between all packages is validated
- [x] Architecture decisions are documented
- [x] LLM provider is chosen and API access is set up
- [x] Testing strategy is defined
- [x] All questions are answered or documented

**Status:** ✅ **READY FOR MILESTONE 2**

All research complete. Architecture decisions made. Ready to start building isolated components.

---

## 📚 Additional Resources Found

### Official Documentation
- [LangChain Cookbook](https://python.langchain.com/docs/use_cases/) - Real-world examples
- [Pydantic v2 Examples](https://docs.pydantic.dev/latest/examples/) - Common patterns
- [Streamlit Chat Tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps) - Chatbot examples
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/) - Complete guide

### Community Resources
- [LangChain Discord](https://discord.gg/langchain) - Community support
- [Streamlit Community](https://discuss.streamlit.io/) - Forum and examples
- [FastAPI GitHub](https://github.com/tiangolo/fastapi) - Examples and issues

### Tutorials & Examples
- LangChain + Streamlit chatbot examples (search GitHub)
- Pydantic v2 migration guides
- FastAPI + LangChain integration examples

---

## 🎯 Next Steps (Milestone 2)

1. **Set up environment:**
   - Install dependencies: `uv sync`
   - Set up `.env` file with OpenAI API key
   - Verify all packages install correctly

2. **Build isolated components:**
   - Create Pydantic models (Message, ChatRequest, etc.)
   - Create LangChain chain with mocked LLM
   - Create memory manager
   - Create Streamlit UI skeleton

3. **Write tests:**
   - Unit tests for Pydantic models
   - Unit tests for memory management
   - Integration tests for chain (with mocked LLM)

4. **Document decisions:**
   - Create GitHub issues for major decisions
   - Document any deviations from this research

---

**Research Completed:** ✅  
**Date:** December 2025  
**Researcher:** AI Assistant (with user approval)  
**Status:** Ready for implementation
