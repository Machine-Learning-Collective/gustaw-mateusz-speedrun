# Pydantic in Chatbot Message Handling

## Purpose

Determine how Pydantic fits into chatbot message handling.

---

## Acceptance Criteria

- [x] Documented proposal for where validation occurs in the flow
- [x] Pydantic v1 vs v2 differences understood and documented
- [x] LangChain's native typing approach researched
- [x] Questions asked about edge cases
- [x] No code yet — research only

---

## 📝 Questions I Need Answered

<!-- Ask clarifying questions to the assessor here -->

### Clarifying Questions for @ArturNiklewicz:

1. **Validation Boundaries:**
   - Should we validate user input before it reaches LangChain, or rely on LangChain's internal validation?
   - Where should validation errors be caught and handled?

2. **Message Type Conversion:**
   - Should we create custom Pydantic models for messages, or use LangChain's native message types (`HumanMessage`, `AIMessage`) directly?
   - Do we need a translation layer between our Pydantic models and LangChain's message types?

3. **API Layer (FastAPI):**
   - If we add FastAPI later, should all request/response validation use Pydantic models?
   - Should we validate at the API boundary and then convert to LangChain types?

4. **Conversation History Storage:**
   - Should conversation history be stored as Pydantic models or as LangChain message objects?
   - How do we serialize/deserialize conversation history for persistence?

5. **Error Handling:**
   - How should Pydantic validation errors be handled in the chatbot flow?
   - Should validation errors be user-facing or logged internally?

6. **Streamlit Integration:**
   - Does Streamlit need Pydantic models, or can we work directly with LangChain message types?
   - Should we validate Streamlit session state with Pydantic?

---

## 🔍 Research Findings

<!-- Document your research with links to official docs -->

### 1. LangChain's Native Message Types

**Key Finding:** LangChain has its own message classes that are built on Pydantic internally.

**LangChain Message Classes:**
- `BaseMessage` - Base class for all messages
- `HumanMessage` - User messages
- `AIMessage` - Assistant/AI responses
- `SystemMessage` - System instructions
- `ChatMessage` - Generic chat message with role

**Important:** These are **LangChain's own classes**, not standard Pydantic models we define. They inherit from Pydantic `BaseModel` internally but are part of LangChain's abstraction.

**Official Documentation:**
- [LangChain Messages](https://python.langchain.com/docs/modules/model_io/prompts/prompt_templates/prompt_templates_chat)
- [BaseMessage Class](https://python.langchain.com/docs/modules/model_io/prompts/messages/)

**Structure:**
```python
# LangChain's message structure (internal)
class BaseMessage(BaseModel):  # Inherits from Pydantic
    content: str
    additional_kwargs: dict = {}
    # ... other fields
```

**Implications:**
- LangChain messages are already Pydantic models (internally)
- We can use LangChain message types directly in chains
- We may need custom Pydantic models for API boundaries

---

### 2. Where Validation Should Occur in Chatbot Flow

**Proposed Validation Points:**

#### 2.1 API Boundary (FastAPI - If Used)

**Location:** FastAPI request/response handlers

**Purpose:**
- Validate incoming user input from external clients
- Validate outgoing responses before sending to clients
- Ensure API contract compliance

**Pydantic Models Needed:**
- `ChatRequest` - Validates incoming chat requests
- `ChatResponse` - Validates outgoing chat responses
- `ErrorResponse` - Validates error responses

**Flow:**
```
External Client
    ↓ (JSON request)
FastAPI Endpoint
    ↓ (Pydantic validation)
ChatRequest (validated)
    ↓ (convert to LangChain)
HumanMessage (LangChain type)
    ↓
LangChain Chain
    ↓
AIMessage (LangChain type)
    ↓ (convert to Pydantic)
ChatResponse (validated)
    ↓ (JSON response)
External Client
```

**Rationale:**
- API boundaries need strict validation
- FastAPI automatically validates using Pydantic
- Provides clear error messages to API clients

---

#### 2.2 Streamlit Input Validation (Optional)

**Location:** Streamlit UI input handling

**Purpose:**
- Validate user input before sending to LangChain
- Provide immediate feedback for invalid input
- Prevent invalid data from reaching LangChain

**Pydantic Models Needed:**
- `UserInput` - Validates user text input
- Optional: `ChatMessage` - For structured message validation

**Flow:**
```
Streamlit UI (user types message)
    ↓
UserInput (Pydantic validation)
    ↓ (if valid, convert to LangChain)
HumanMessage (LangChain type)
    ↓
LangChain Chain
    ↓
AIMessage (LangChain type)
    ↓ (display in Streamlit)
Streamlit UI
```

**Rationale:**
- Streamlit doesn't require Pydantic (can work with raw strings)
- Optional validation for better UX and error handling
- Can catch issues before expensive LLM calls

---

#### 2.3 Conversation History Storage (If Persisting)

**Location:** Memory/persistence layer

**Purpose:**
- Validate conversation history structure
- Ensure data integrity when loading/saving history
- Type safety for serialization/deserialization

**Pydantic Models Needed:**
- `ConversationHistory` - Validates entire conversation
- `StoredMessage` - Validates individual stored messages

**Flow:**
```
LangChain Memory (in-memory)
    ↓ (when persisting)
ConversationHistory (Pydantic validation)
    ↓ (serialize to JSON/database)
Storage (file/database)
    ↓ (when loading)
ConversationHistory (Pydantic validation)
    ↓ (convert to LangChain)
LangChain Memory (restored)
```

**Rationale:**
- Ensures data integrity across sessions
- Validates structure when loading from storage
- Prevents corruption of conversation history

---

#### 2.4 LangChain Internal (No Custom Validation Needed)

**Location:** Inside LangChain chain execution

**Purpose:**
- LangChain handles its own message validation
- No need for additional Pydantic validation here

**Flow:**
```
HumanMessage (LangChain type)
    ↓ (LangChain internal validation)
ChatPromptTemplate
    ↓
ChatOpenAI
    ↓ (LangChain internal validation)
AIMessage (LangChain type)
```

**Rationale:**
- LangChain messages are already Pydantic models internally
- LangChain handles validation of its own types
- Adding extra validation here is redundant

---

### 3. Pydantic v1 vs v2 Differences

**Critical for Chatbot Development:**

#### 3.1 Serialization Methods (Breaking Changes)

**Pydantic v1:**
```python
model.dict()        # Convert to dictionary
model.json()        # Convert to JSON string
model.dict(exclude_unset=True)  # Exclude unset fields
```

**Pydantic v2:**
```python
model.model_dump()           # Convert to dictionary (replaces .dict())
model.model_dump_json()      # Convert to JSON string (replaces .json())
model.model_dump(exclude_unset=True)  # Exclude unset fields
```

**Impact on Chatbot:**
- ⚠️ **Breaking Change:** Must use `.model_dump()` not `.dict()`
- ⚠️ **Breaking Change:** Must use `.model_dump_json()` not `.json()`
- ✅ All existing code using v1 methods will break

**Official Documentation:**
- [Pydantic v2 Migration Guide](https://docs.pydantic.dev/latest/migration/)
- [Pydantic v2 Serialization](https://docs.pydantic.dev/latest/concepts/serialization/)

---

#### 3.2 Validation Performance

**Pydantic v1:**
- Python-based validation
- Slower performance

**Pydantic v2:**
- Rust-based core (pydantic-core)
- **5-50x faster** validation
- Better performance for high-throughput chatbots

**Impact on Chatbot:**
- ✅ Faster request/response validation
- ✅ Better performance for API endpoints
- ✅ Lower latency in message processing

---

#### 3.3 Type System Improvements

**Pydantic v1:**
- Basic type hints support
- Limited union syntax

**Pydantic v2:**
- Better Python 3.10+ type hint support
- PEP 604 union syntax (`str | int` instead of `Union[str, int]`)
- More flexible validation

**Impact on Chatbot:**
- ✅ More expressive type hints
- ✅ Better IDE support
- ✅ Cleaner code

---

#### 3.4 Validation Decorators

**Pydantic v1:**
```python
@validator('field_name')
def validate_field(cls, v):
    return v
```

**Pydantic v2:**
```python
@field_validator('field_name')
@classmethod
def validate_field(cls, v):
    return v
```

**Impact on Chatbot:**
- ⚠️ **Breaking Change:** Validator decorators changed
- Must update custom validators if migrating from v1

---

#### 3.5 Model Configuration

**Pydantic v1:**
```python
class Config:
    allow_population_by_field_name = True
```

**Pydantic v2:**
```python
model_config = ConfigDict(
    populate_by_name=True
)
```

**Impact on Chatbot:**
- ⚠️ **Breaking Change:** Config syntax changed
- Must update model configurations

---

### 4. LangChain's Native Typing Approach

**Key Finding:** LangChain uses Pydantic internally but has its own type system.

#### 4.1 LangChain Message Types

**LangChain's Approach:**
- Uses Pydantic `BaseModel` internally for message classes
- Provides its own message types (`HumanMessage`, `AIMessage`, etc.)
- Messages are validated by LangChain, not by our custom Pydantic models

**Example:**
```python
from langchain_core.messages import HumanMessage, AIMessage

# These are LangChain's Pydantic models (internal)
user_msg = HumanMessage(content="Hello")
ai_msg = AIMessage(content="Hi there!")

# LangChain validates these internally
# We don't need to create our own Pydantic models for these
```

**Official Documentation:**
- [LangChain Messages](https://python.langchain.com/docs/modules/model_io/prompts/messages/)
- [LangChain Core Messages](https://python.langchain.com/docs/modules/model_io/prompts/prompt_templates/prompt_templates_chat)

---

#### 4.2 When to Use Custom Pydantic Models vs LangChain Types

**Use LangChain Types Directly:**
- ✅ Inside LangChain chains
- ✅ When working with LangChain memory
- ✅ When passing messages to LangChain components

**Use Custom Pydantic Models:**
- ✅ At API boundaries (FastAPI request/response)
- ✅ For conversation history persistence
- ✅ For metadata and configuration
- ✅ For Streamlit input validation (optional)

**Example Pattern:**
```python
# API Layer (Custom Pydantic)
class ChatRequest(BaseModel):
    message: str
    session_id: str

# Convert to LangChain type
langchain_msg = HumanMessage(content=request.message)

# Use in LangChain chain
response = chain.invoke(langchain_msg)

# Convert back to Pydantic for API response
class ChatResponse(BaseModel):
    message: str
    session_id: str

return ChatResponse(
    message=response.content,
    session_id=request.session_id
)
```

---

### 5. Validation Flow Diagram

**Complete Chatbot Flow with Validation Points:**

```
┌─────────────────────────────────────────────────────────────┐
│                    EXTERNAL BOUNDARY                        │
│  (FastAPI Request / Streamlit Input)                        │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │   VALIDATION POINT #1          │
        │   Custom Pydantic Models       │
        │   - ChatRequest                 │
        │   - UserInput (optional)        │
        └───────────────┬───────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │   CONVERSION LAYER              │
        │   Pydantic → LangChain          │
        │   ChatRequest → HumanMessage    │
        └───────────────┬───────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │   LANGCHAIN INTERNAL            │
        │   (No custom validation)       │
        │   - HumanMessage (validated)    │
        │   - ChatPromptTemplate          │
        │   - ChatOpenAI                  │
        │   - AIMessage (validated)       │
        └───────────────┬───────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │   CONVERSION LAYER              │
        │   LangChain → Pydantic          │
        │   AIMessage → ChatResponse      │
        └───────────────┬───────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │   VALIDATION POINT #2            │
        │   Custom Pydantic Models        │
        │   - ChatResponse                │
        └───────────────┬───────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    EXTERNAL BOUNDARY                        │
│  (FastAPI Response / Streamlit Output)                       │
└─────────────────────────────────────────────────────────────┘
```

---

### 6. Edge Cases and Considerations

#### 6.1 Message Content Validation

**Question:** Should we validate message content (length, format, etc.)?

**Considerations:**
- LangChain accepts any string content
- API clients might send invalid data
- Should validate at API boundary, not in LangChain

**Recommendation:**
- Validate content length, format at API boundary
- Use Pydantic validators for content rules
- Let LangChain handle its own internal validation

---

#### 6.2 Empty Messages

**Question:** How should empty messages be handled?

**Considerations:**
- Empty strings might be valid in some contexts
- Should we reject empty messages?
- Where should this validation occur?

**Recommendation:**
- Validate at API boundary (Pydantic model)
- Use `Field(min_length=1)` to reject empty messages
- Or handle in business logic before LangChain

---

#### 6.3 Special Characters and Encoding

**Question:** Should we validate encoding and special characters?

**Considerations:**
- LangChain handles UTF-8 strings
- API might send invalid encoding
- Should validate at boundary

**Recommendation:**
- Pydantic automatically handles string validation
- FastAPI handles encoding
- Additional validation only if needed

---

#### 6.4 Conversation History Serialization

**Question:** How to serialize/deserialize conversation history?

**Considerations:**
- LangChain messages need conversion for storage
- Should we store as Pydantic models or LangChain types?
- How to handle version changes?

**Recommendation:**
- Store as Pydantic models (more stable)
- Convert LangChain messages to Pydantic for storage
- Convert back to LangChain when loading

---

#### 6.5 Error Handling

**Question:** How should Pydantic validation errors be handled?

**Considerations:**
- Validation errors at API boundary should be user-facing
- Validation errors in internal code should be logged
- Need clear error messages

**Recommendation:**
- API: Return 400 Bad Request with error details
- Internal: Log errors, handle gracefully
- Use Pydantic's detailed error messages

---

## ✅ Decision Made + Rationale

<!-- Where will Pydantic be used and why? -->

### Decision: Pydantic Usage Strategy

**Where Pydantic Will Be Used:**

#### 1. ✅ API Boundary (FastAPI - If Used)

**Models:**
- `ChatRequest` - Validates incoming chat requests
- `ChatResponse` - Validates outgoing chat responses
- `ErrorResponse` - Validates error responses

**Rationale:**
- FastAPI requires Pydantic models for request/response validation
- Provides automatic API documentation (OpenAPI)
- Ensures API contract compliance
- Clear error messages for API clients

---

#### 2. ✅ Conversation History Persistence (If Needed)

**Models:**
- `StoredMessage` - Individual message for storage
- `ConversationHistory` - Full conversation for storage

**Rationale:**
- Validates data structure when saving/loading
- Ensures data integrity across sessions
- Type-safe serialization/deserialization
- Prevents corruption of conversation history

---

#### 3. ⚠️ Streamlit Input (Optional)

**Models:**
- `UserInput` - Optional validation for user input

**Rationale:**
- Streamlit doesn't require Pydantic (works with raw strings)
- Optional for better UX and early error detection
- Can catch issues before expensive LLM calls
- **Decision Needed:** Is this worth the complexity?

---

#### 4. ❌ Inside LangChain Chain (Not Needed)

**Rationale:**
- LangChain messages are already Pydantic models internally
- LangChain handles its own validation
- Adding extra validation is redundant
- Would add unnecessary conversion overhead

---

### Pydantic v2 Migration Strategy

**Key Changes to Remember:**
1. ✅ Use `.model_dump()` instead of `.dict()`
2. ✅ Use `.model_dump_json()` instead of `.json()`
3. ✅ Use `@field_validator` instead of `@validator`
4. ✅ Use `model_config = ConfigDict(...)` instead of `class Config`
5. ✅ All models must inherit from Pydantic v2 `BaseModel`

**Impact:**
- All code must use v2 syntax from the start
- No migration needed (starting fresh)
- Follow v2 best practices

---

### Conversion Strategy: Pydantic ↔ LangChain

**Pattern:**
```python
# API Request → LangChain
def pydantic_to_langchain(request: ChatRequest) -> HumanMessage:
    return HumanMessage(content=request.message)

# LangChain → API Response
def langchain_to_pydantic(
    ai_message: AIMessage, 
    session_id: str
) -> ChatResponse:
    return ChatResponse(
        message=ai_message.content,
        session_id=session_id
    )
```

**Rationale:**
- Clear separation of concerns
- API layer uses Pydantic
- LangChain layer uses LangChain types
- Conversion functions handle translation

---

## 📎 Evidence/Proof

<!-- Screenshots, doc links proving your findings -->

### Official Documentation Links

1. **Pydantic v2:**
   - [Pydantic v2 Documentation](https://docs.pydantic.dev/latest/)
   - [Pydantic v2 Migration Guide](https://docs.pydantic.dev/latest/migration/)
   - [Pydantic v2 Serialization](https://docs.pydantic.dev/latest/concepts/serialization/)

2. **LangChain Messages:**
   - [LangChain Messages Documentation](https://python.langchain.com/docs/modules/model_io/prompts/messages/)
   - [BaseMessage Class](https://python.langchain.com/docs/modules/model_io/prompts/messages/)

3. **FastAPI + Pydantic:**
   - [FastAPI Request Body](https://fastapi.tiangolo.com/tutorial/body/)
   - [FastAPI Response Model](https://fastapi.tiangolo.com/tutorial/response-model/)

4. **Pydantic Validation:**
   - [Pydantic Validators](https://docs.pydantic.dev/latest/concepts/validators/)
   - [Pydantic Field Validation](https://docs.pydantic.dev/latest/concepts/fields/)

### Key Findings Summary

1. **LangChain Uses Pydantic Internally:**
   - LangChain message types (`HumanMessage`, `AIMessage`) are Pydantic models
   - No need for custom Pydantic models inside LangChain chains
   - LangChain handles its own validation

2. **Pydantic at Boundaries:**
   - Use Pydantic models at API boundaries (FastAPI)
   - Use Pydantic models for persistence (conversation history)
   - Convert between Pydantic and LangChain types at boundaries

3. **Pydantic v2 Breaking Changes:**
   - `.dict()` → `.model_dump()`
   - `.json()` → `.model_dump_json()`
   - `@validator` → `@field_validator`
   - `class Config` → `model_config = ConfigDict()`

4. **Validation Flow:**
   - Validate at API boundary (FastAPI)
   - Optional validation at Streamlit input
   - No validation needed inside LangChain (handles internally)
   - Validate when persisting conversation history

---

## 🎯 Summary

**Pydantic Usage in Chatbot:**

1. **API Boundaries (FastAPI):** ✅ Use Pydantic models for request/response validation
2. **Persistence Layer:** ✅ Use Pydantic models for conversation history storage
3. **Streamlit Input:** ⚠️ Optional - can use Pydantic for validation
4. **LangChain Internal:** ❌ Not needed - LangChain handles its own validation

**Key Principles:**
- Validate at boundaries, not in the middle
- Use Pydantic v2 syntax from the start
- Convert between Pydantic and LangChain types at boundaries
- Let LangChain handle its own internal validation

**Open Questions:**
- Streamlit input validation: needed or optional?
- Conversation history persistence: in-memory or persisted?
- Error handling strategy: user-facing or internal?

---

**Research Completed:** ✅  
**Date:** December 2025  
**Status:** Ready for implementation decisions

