# Streamlit Chat UI Interaction Model

## Purpose

Understand Streamlit's interaction model for chat UIs to avoid anti-patterns.

---

## Acceptance Criteria

- [x] Session state behavior documented
- [x] Streamlit chat components researched
- [x] Limitations identified (what Streamlit can't do well)
- [x] Questions asked about UX constraints
- [x] No code yet — research only

---

## 📝 Questions I Need Answered

<!-- Ask clarifying questions to the assessor here -->

### Clarifying Questions for @ArturNiklewicz:

1. **Streaming Responses:**
   - Should the chatbot stream responses token-by-token for better UX, or is full response acceptable?
   - Streamlit supports streaming, but it requires specific patterns - is this needed for Milestone 1-2?

2. **Loading States:**
   - How should we indicate that the LLM is processing? (spinner, placeholder message, etc.)
   - Should we disable input during processing to prevent duplicate requests?

3. **Error Handling UX:**
   - How should errors be displayed to users? (error message in chat, toast notification, etc.)
   - Should errors be recoverable or require page refresh?

4. **Conversation Persistence:**
   - Should conversation history persist across page refreshes, or is session-only acceptable?
   - If persisting, should we use browser storage or backend storage?

5. **Multi-User Considerations:**
   - Is this a single-user application, or do we need to handle multiple concurrent users?
   - Streamlit session state is per-browser - is this acceptable?

6. **Performance Expectations:**
   - What's the expected response time for LLM calls?
   - Should we implement request queuing or cancellation?

---

## 🔍 Research Findings

<!-- Document your research with links to official docs -->

### 1. Streamlit's Execution Model

**Key Concept:** Streamlit uses a **script rerun model**, not a traditional event-driven model.

**How It Works:**
1. User interacts with UI (clicks button, submits input)
2. Streamlit **reruns the entire script from top to bottom**
3. Script execution determines what to display
4. UI updates based on script output

**Implications for Chat UIs:**
- ⚠️ **Every interaction triggers a full script rerun**
- ⚠️ **State must be preserved in `st.session_state`**
- ⚠️ **Code runs top-to-bottom on every interaction**
- ✅ **Simple mental model** - no event handlers needed

**Official Documentation:**
- [Streamlit Execution Model](https://docs.streamlit.io/develop/concepts/architecture/)
- [How Streamlit Works](https://docs.streamlit.io/develop/concepts/architecture/execution-model)

---

### 2. Session State Behavior

**What is Session State?**
- `st.session_state` is a **per-browser-session dictionary**
- Persists across script reruns within the same browser session
- **Lost when browser tab is closed or refreshed**
- Each browser tab = separate session state

**Key Characteristics:**

#### 2.1 Initialization Pattern

**Critical:** Must check if key exists before accessing.

```python
# ✅ CORRECT: Check before accessing
if "messages" not in st.session_state:
    st.session_state.messages = []

# ❌ WRONG: Will reset on every rerun
st.session_state.messages = []  # Don't do this!
```

**Why:** Script reruns from top, so assignment would reset state.

#### 2.2 State Persistence

**What Persists:**
- ✅ Values in `st.session_state` persist across reruns
- ✅ Conversation history stored in session state
- ✅ User preferences, settings

**What Doesn't Persist:**
- ❌ State is lost on page refresh
- ❌ State is lost when browser tab closes
- ❌ State is not shared between browser tabs
- ❌ State is not shared between users

**Official Documentation:**
- [Streamlit Session State](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state)
- [Session State Guide](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)

#### 2.3 State Access Patterns

**Safe Patterns:**
```python
# Pattern 1: Check existence
if "key" not in st.session_state:
    st.session_state.key = default_value

# Pattern 2: Use .get() with default
value = st.session_state.get("key", default_value)

# Pattern 3: Initialize in one place
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.messages = []
    st.session_state.counter = 0
```

**Anti-Patterns:**
```python
# ❌ Resets on every rerun
st.session_state.messages = []

# ❌ KeyError if key doesn't exist
messages = st.session_state.messages

# ❌ Modifying during iteration (can cause issues)
for msg in st.session_state.messages:
    st.session_state.messages.append(new_msg)  # Dangerous!
```

---

### 3. Streamlit Chat Components

**Native Chat Components (Streamlit 1.24.0+):**

#### 3.1 `st.chat_message()`

**Purpose:** Display a message with role-based styling.

**Usage:**
```python
with st.chat_message("user"):
    st.write("Hello!")

with st.chat_message("assistant"):
    st.write("Hi there!")
```

**Supported Roles:**
- `"user"` - User messages (right-aligned, blue)
- `"assistant"` - AI/assistant messages (left-aligned, gray)
- `"system"` - System messages (centered)
- Custom roles also supported

**Key Features:**
- ✅ Automatic styling based on role
- ✅ Can nest other Streamlit components inside
- ✅ Supports markdown, code, images, etc.

**Official Documentation:**
- [st.chat_message()](https://docs.streamlit.io/develop/api-reference/chat/st.chat_message)

#### 3.2 `st.chat_input()`

**Purpose:** Input widget specifically designed for chat interfaces.

**Usage:**
```python
user_input = st.chat_input("Type your message...")

if user_input:
    # Process the input
    st.write(f"You said: {user_input}")
```

**Key Features:**
- ✅ Styled for chat interfaces
- ✅ Returns `None` until user submits
- ✅ Clears after submission (on next rerun)
- ✅ Placeholder text support

**Behavior:**
- Returns `None` on initial load
- Returns input string when user submits
- Automatically triggers script rerun on submit
- Input clears after processing

**Official Documentation:**
- [st.chat_input()](https://docs.streamlit.io/develop/api-reference/chat/st.chat_input)

#### 3.3 Chat UI Pattern

**Complete Pattern:**
```python
# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Get user input
if prompt := st.chat_input("What is up?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get AI response (simplified)
    response = get_ai_response(prompt)
    
    # Add AI response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Display AI response
    with st.chat_message("assistant"):
        st.write(response)
```

**Official Documentation:**
- [Build Conversational Apps](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)

---

### 4. Limitations and Constraints

#### 4.1 No True Real-Time Updates

**Limitation:** Streamlit doesn't support WebSocket connections or server-sent events.

**Impact:**
- ❌ Cannot push updates from server to client
- ❌ Cannot implement true real-time chat (like Slack, Discord)
- ❌ Must use request-response pattern
- ✅ Fine for chatbot use case (request-response is standard)

**Workaround:**
- Use `st.rerun()` to refresh UI after state changes
- Polling (not recommended - inefficient)
- Accept request-response model (recommended)

---

#### 4.2 Rerun on Every Interaction

**Limitation:** Every user interaction triggers a full script rerun.

**Impact:**
- ⚠️ **Performance:** Entire script executes on every interaction
- ⚠️ **State Management:** Must carefully manage state
- ⚠️ **Code Execution:** All code runs, even if not needed
- ✅ **Simplicity:** No event handlers needed

**Best Practices:**
- Use `@st.cache_data` for expensive computations
- Initialize state only once
- Avoid heavy computations in main script flow
- Use conditional execution based on state

**Anti-Pattern:**
```python
# ❌ BAD: Expensive operation on every rerun
for i in range(1000000):
    result = expensive_computation(i)

# ✅ GOOD: Cache expensive operations
@st.cache_data
def expensive_computation(n):
    # ... expensive code ...
    return result
```

---

#### 4.3 No Client-Side State

**Limitation:** Streamlit has no client-side JavaScript state management.

**Impact:**
- ❌ Cannot store state in browser (localStorage, sessionStorage)
- ❌ Cannot implement client-side validation
- ❌ All state must go through server (session state)
- ✅ Simpler architecture (no client/server sync issues)

**Workaround:**
- Use `st.session_state` for all state
- For persistence, use backend storage (database, file)
- Accept that state is lost on refresh (or implement persistence)

---

#### 4.4 Limited Customization

**Limitation:** Streamlit has limited UI customization compared to React/Vue.

**Impact:**
- ❌ Cannot create custom chat bubbles
- ❌ Limited CSS customization
- ❌ Cannot implement complex animations
- ✅ Pre-built components are well-designed
- ✅ Faster development

**Acceptable Trade-offs:**
- Use Streamlit's built-in chat components
- Accept default styling (it's actually quite good)
- Focus on functionality over custom styling

---

#### 4.5 Single-Threaded Execution

**Limitation:** Streamlit script runs in a single thread.

**Impact:**
- ⚠️ **Blocking:** Long-running operations block UI
- ⚠️ **No Async:** Cannot use async/await easily
- ⚠️ **LLM Calls:** Blocking LLM calls freeze UI

**Best Practices:**
- Show loading indicators during LLM calls
- Use `st.spinner()` or `st.status()` for long operations
- Consider async patterns if needed (advanced)

**Example:**
```python
with st.spinner("Thinking..."):
    response = llm_chain.invoke(user_input)
```

---

#### 4.6 Session State Not Shared

**Limitation:** Each browser session has separate session state.

**Impact:**
- ❌ Cannot share state between users
- ❌ Each user has independent conversation
- ❌ Cannot implement collaborative features
- ✅ Good for privacy (each user's data isolated)

**For Multi-User:**
- Use backend storage (database) for shared state
- Use session IDs to track users
- Consider FastAPI backend for multi-user scenarios

---

#### 4.7 No Built-in Authentication

**Limitation:** Streamlit has no built-in user authentication.

**Impact:**
- ❌ Cannot identify users easily
- ❌ Cannot implement user-specific features
- ❌ Session state is anonymous
- ✅ Fine for single-user or internal tools

**Workarounds:**
- Use `st.secrets` for simple authentication
- Implement custom auth with cookies/sessions
- Use external auth providers (OAuth, etc.)

---

### 5. Anti-Patterns to Avoid

#### 5.1 Resetting State on Rerun

**Anti-Pattern:**
```python
# ❌ BAD: Resets messages on every rerun
st.session_state.messages = []

# ✅ GOOD: Initialize only once
if "messages" not in st.session_state:
    st.session_state.messages = []
```

**Why It's Bad:**
- Loses conversation history on every interaction
- User messages disappear immediately
- Breaks chat functionality

---

#### 5.2 Not Handling None from chat_input

**Anti-Pattern:**
```python
# ❌ BAD: Crashes on initial load
user_input = st.chat_input()
process_input(user_input)  # user_input is None on first run!

# ✅ GOOD: Check for None
if user_input := st.chat_input():
    process_input(user_input)
```

**Why It's Bad:**
- Script crashes on initial page load
- `st.chat_input()` returns `None` until user submits

---

#### 5.3 Modifying State During Iteration

**Anti-Pattern:**
```python
# ❌ BAD: Modifying list during iteration
for message in st.session_state.messages:
    if should_remove(message):
        st.session_state.messages.remove(message)  # Dangerous!

# ✅ GOOD: Create new list
st.session_state.messages = [
    msg for msg in st.session_state.messages
    if not should_remove(msg)
]
```

**Why It's Bad:**
- Can cause iteration errors
- Unpredictable behavior
- Can skip or duplicate items

---

#### 5.4 Not Showing Loading States

**Anti-Pattern:**
```python
# ❌ BAD: No feedback during LLM call
response = llm_chain.invoke(user_input)  # UI freezes, user confused

# ✅ GOOD: Show loading indicator
with st.spinner("Thinking..."):
    response = llm_chain.invoke(user_input)
```

**Why It's Bad:**
- User doesn't know if app is working
- App appears frozen during LLM calls
- Poor user experience

---

#### 5.5 Storing Large Objects in Session State

**Anti-Pattern:**
```python
# ❌ BAD: Storing large objects
st.session_state.large_data = load_huge_dataset()  # Memory issues!

# ✅ GOOD: Use caching or load on demand
@st.cache_data
def get_large_data():
    return load_huge_dataset()
```

**Why It's Bad:**
- Consumes memory
- Slows down reruns
- Can cause performance issues

---

#### 5.6 Not Handling Errors Gracefully

**Anti-Pattern:**
```python
# ❌ BAD: Let errors crash the app
response = llm_chain.invoke(user_input)  # Can raise exception

# ✅ GOOD: Handle errors
try:
    response = llm_chain.invoke(user_input)
except Exception as e:
    st.error(f"Error: {e}")
    response = "I'm sorry, I encountered an error."
```

**Why It's Bad:**
- App crashes on errors
- Poor user experience
- No error recovery

---

### 6. Best Practices for Chat UIs

#### 6.1 State Initialization

**Pattern:**
```python
# Initialize all state in one place
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())
    # ... other initialization
```

**Benefits:**
- Clear initialization point
- Easy to reset state if needed
- Prevents accidental resets

---

#### 6.2 Display History Before Input

**Pattern:**
```python
# Display history first
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Then get new input
if prompt := st.chat_input():
    # Process input
```

**Benefits:**
- User sees conversation history
- New messages appear at bottom
- Natural chat flow

---

#### 6.3 Show Loading States

**Pattern:**
```python
if prompt := st.chat_input():
    # Add user message immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Show loading indicator
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = llm_chain.invoke(prompt)
    
    # Add response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Rerun to show full conversation
    st.rerun()
```

**Benefits:**
- User knows app is working
- Better UX during LLM calls
- Prevents duplicate submissions

---

#### 6.4 Error Handling

**Pattern:**
```python
try:
    response = llm_chain.invoke(prompt)
except Exception as e:
    st.error(f"Error: {e}")
    response = "I'm sorry, I encountered an error. Please try again."
    # Log error for debugging
    logger.error(f"LLM error: {e}")
```

**Benefits:**
- Graceful error handling
- User-friendly error messages
- Error logging for debugging

---

#### 6.5 Clear Input After Submission

**Pattern:**
```python
if prompt := st.chat_input():
    # Process input
    # st.chat_input() automatically clears on next rerun
    # No manual clearing needed
```

**Note:** `st.chat_input()` automatically clears after submission, so no manual clearing needed.

---

## ✅ Decision Made + Rationale

<!-- How will you handle Streamlit's constraints? -->

### Decision: Streamlit Chat UI Strategy

#### 1. ✅ Accept Request-Response Model

**Decision:** Use request-response pattern, not real-time streaming.

**Rationale:**
- Streamlit doesn't support WebSocket/SSE
- Request-response is standard for chatbots
- Simpler implementation
- Good enough UX for Milestone 1-2

**Implementation:**
- User submits message → LLM processes → Response displayed
- Use `st.spinner()` during LLM calls
- Show full response when ready

---

#### 2. ✅ Use Session State for Conversation History

**Decision:** Store conversation history in `st.session_state.messages`.

**Rationale:**
- Simple and effective
- No external storage needed for Milestone 1-2
- Each user has independent conversation
- Can add persistence later if needed

**Implementation:**
```python
# Initialize once
if "messages" not in st.session_state:
    st.session_state.messages = []

# Store messages
st.session_state.messages.append({"role": "user", "content": prompt})
st.session_state.messages.append({"role": "assistant", "content": response})
```

---

#### 3. ✅ Show Loading Indicators

**Decision:** Use `st.spinner()` or `st.status()` during LLM calls.

**Rationale:**
- Prevents user confusion during processing
- Better UX than frozen UI
- Standard practice for async operations

**Implementation:**
```python
with st.spinner("Thinking..."):
    response = llm_chain.invoke(prompt)
```

---

#### 4. ✅ Handle Errors Gracefully

**Decision:** Catch exceptions and show user-friendly error messages.

**Rationale:**
- Prevents app crashes
- Better user experience
- Allows error recovery

**Implementation:**
```python
try:
    response = llm_chain.invoke(prompt)
except Exception as e:
    st.error("Sorry, I encountered an error. Please try again.")
    logger.error(f"Error: {e}")
```

---

#### 5. ✅ Initialize State Properly

**Decision:** Use `if "key" not in st.session_state` pattern for all state.

**Rationale:**
- Prevents accidental resets
- Clear initialization point
- Standard Streamlit pattern

**Implementation:**
```python
if "messages" not in st.session_state:
    st.session_state.messages = []
```

---

#### 6. ⚠️ Accept Session-Only Persistence (For Now)

**Decision:** Conversation history lost on page refresh (for Milestone 1-2).

**Rationale:**
- Simpler implementation
- Good enough for initial development
- Can add persistence in Milestone 3+ if needed

**Future Enhancement:**
- Add database/file persistence
- Restore conversation on page load
- Implement session management

---

#### 7. ✅ Use Native Chat Components

**Decision:** Use `st.chat_message()` and `st.chat_input()`.

**Rationale:**
- Well-designed components
- Good default styling
- Faster development
- No need for custom UI

---

### Handling Streamlit's Constraints

**Constraint: Rerun on Every Interaction**
- ✅ **Solution:** Use session state to preserve data
- ✅ **Solution:** Cache expensive operations
- ✅ **Solution:** Conditional execution based on state

**Constraint: No Real-Time Updates**
- ✅ **Solution:** Accept request-response model
- ✅ **Solution:** Use `st.rerun()` to refresh UI
- ✅ **Solution:** Show loading states during processing

**Constraint: No Client-Side State**
- ✅ **Solution:** Use `st.session_state` for all state
- ✅ **Solution:** Accept session-only persistence (for now)
- ✅ **Solution:** Add backend persistence if needed later

**Constraint: Limited Customization**
- ✅ **Solution:** Use built-in chat components
- ✅ **Solution:** Accept default styling
- ✅ **Solution:** Focus on functionality over styling

**Constraint: Single-Threaded Execution**
- ✅ **Solution:** Show loading indicators
- ✅ **Solution:** Handle errors gracefully
- ✅ **Solution:** Optimize LLM calls (caching, etc.)

---

## 📎 Evidence/Proof

<!-- Screenshots, doc links proving your findings -->

### Official Documentation Links

1. **Streamlit Execution Model:**
   - [Streamlit Architecture](https://docs.streamlit.io/develop/concepts/architecture/)
   - [Execution Model](https://docs.streamlit.io/develop/concepts/architecture/execution-model)

2. **Session State:**
   - [Session State API](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state)
   - [Session State Guide](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)

3. **Chat Components:**
   - [st.chat_message()](https://docs.streamlit.io/develop/api-reference/chat/st.chat_message)
   - [st.chat_input()](https://docs.streamlit.io/develop/api-reference/chat/st.chat_input)
   - [Build Conversational Apps](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)

4. **Best Practices:**
   - [Streamlit Best Practices](https://docs.streamlit.io/develop/concepts/architecture/execution-model#data-flow)
   - [Performance Optimization](https://docs.streamlit.io/develop/concepts/architecture/execution-model#optimize-rendering)

### Key Takeaways

1. **Session State:**
   - Must initialize with `if "key" not in st.session_state`
   - Persists across reruns but not page refreshes
   - Each browser session is independent

2. **Chat Components:**
   - `st.chat_message()` for displaying messages
   - `st.chat_input()` for user input
   - Both are well-designed and easy to use

3. **Limitations:**
   - No real-time updates (request-response only)
   - Reruns on every interaction
   - No client-side state
   - Limited customization

4. **Best Practices:**
   - Initialize state properly
   - Show loading indicators
   - Handle errors gracefully
   - Use native chat components

---

## 🎯 Summary

**Streamlit Chat UI Strategy:**

1. ✅ **Use Session State** for conversation history
2. ✅ **Use Native Components** (`st.chat_message()`, `st.chat_input()`)
3. ✅ **Show Loading States** during LLM calls
4. ✅ **Handle Errors** gracefully
5. ✅ **Accept Request-Response** model (no real-time streaming)
6. ✅ **Accept Session-Only** persistence (for now)

**Key Constraints:**
- Reruns on every interaction (manage state carefully)
- No real-time updates (request-response is fine)
- Session state lost on refresh (acceptable for Milestone 1-2)

**Anti-Patterns to Avoid:**
- ❌ Resetting state on rerun
- ❌ Not handling `None` from `st.chat_input()`
- ❌ Modifying state during iteration
- ❌ Not showing loading states
- ❌ Not handling errors

---

**Research Completed:** ✅  
**Date:** December 2025  
**Status:** Ready for implementation

