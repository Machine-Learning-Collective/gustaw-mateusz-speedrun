# LangChain Core Abstractions for Chatbot Development

## Purpose

Understand LangChain's core abstractions for chatbot use before implementation.

---

## Acceptance Criteria

- [x] Key LangChain concepts documented (chains, agents, memory, etc.)
- [x] Candidate explains which abstractions apply to simple chatbot
- [x] Questions asked about ambiguities
- [x] No code yet — research only

---

## 📝 Questions I Need Answered

<!-- Ask clarifying questions to the assessor here -->

### Clarifying Questions for @ArturNiklewicz:

1. **LCEL vs Legacy Chains:**
   - Should we use LangChain Expression Language (LCEL) for building chains, or are legacy chain classes (like `ConversationChain`) acceptable?
   - LCEL is the modern approach (recommended as of December 2025), but legacy chains might be simpler for a basic chatbot.

2. **Memory Persistence:**
   - For Milestone 1-2, is in-memory conversation history sufficient, or should we plan for persistence from the start?
   - This affects architecture decisions (database vs. session state).

3. **Agent vs Chain:**
   - For a simple chatbot (no tools, no external actions), should we use a basic Chain or an Agent?
   - Agents add complexity but might be overkill for a basic conversational bot.

4. **RAG (Retrieval-Augmented Generation):**
   - Should the chatbot have document retrieval capabilities, or is it purely conversational?
   - This determines if we need Document Loaders, Text Splitters, Embeddings, VectorStores.

5. **Streaming Responses:**
   - Should the chatbot stream responses token-by-token for better UX, or is full response acceptable?
   - This affects how we integrate LangChain with Streamlit.

---

## 🔍 Research Findings

<!-- Document your research with links to official docs -->

### 1. Core LangChain Abstractions Overview

LangChain provides modular components that can be combined to build chatbot applications. Here are the key abstractions:

#### 1.1 Models and Chat Models

**Concept:**
- **LLMs:** Standardized interfaces for text-in/text-out language models
- **Chat Models:** Specialized for multi-turn conversations (what we need for chatbots)
- **Providers:** OpenAI, Anthropic, Cohere, Hugging Face, etc.

**Key Classes:**
- `ChatOpenAI` - OpenAI's chat models (GPT-3.5, GPT-4)
- `ChatAnthropic` - Anthropic's Claude models
- `ChatModel` - Base class for all chat models

**Official Documentation:**
- [LangChain Chat Models](https://python.langchain.com/docs/integrations/chat/)
- [LangChain Model I/O](https://python.langchain.com/docs/modules/model_io/)

**Relevance to Simple Chatbot:**
✅ **ESSENTIAL** - Chat models are the core of any chatbot. We'll use `ChatOpenAI` for our simple chatbot.

---

#### 1.2 Prompts and Prompt Templates

**Concept:**
- **Prompt Templates:** Reusable templates that combine variables, system messages, and user input
- **Chat Prompt Templates:** Specifically designed for conversational interfaces
- **Messages:** Structured message objects (SystemMessage, HumanMessage, AIMessage)

**Key Classes:**
- `ChatPromptTemplate` - Template for chat-style prompts
- `MessagesPlaceholder` - Placeholder for injecting conversation history
- `SystemMessage`, `HumanMessage`, `AIMessage` - Message types

**Official Documentation:**
- [LangChain Prompt Templates](https://python.langchain.com/docs/modules/model_io/prompts/)
- [Chat Prompt Templates](https://python.langchain.com/docs/modules/model_io/prompts/prompt_templates/prompt_templates_chat)

**Relevance to Simple Chatbot:**
✅ **ESSENTIAL** - We need prompt templates to structure conversations and inject chat history.

**Example Pattern:**
```
System Message: "You are a helpful assistant."
+ MessagesPlaceholder (conversation history)
+ HumanMessage (current user input)
→ Send to Chat Model
→ Get AIMessage (response)
```

---

#### 1.3 Chains

**Concept:**
- **Chains:** Sequences of calls to LLMs or other components
- **Purpose:** Combine multiple steps (prompt → LLM → output parser)
- **Types:** Sequential chains, parallel chains, custom chains

**Key Approaches (as of December 2025):**

**A. LangChain Expression Language (LCEL) - Modern Approach:**
- Declarative syntax using `|` (pipe) operator
- Type-safe, composable, supports streaming
- Recommended for new projects (as of December 2025)

**B. Legacy Chain Classes:**
- `ConversationChain` - Simple conversation chain with memory
- `LLMChain` - Basic chain for single LLM call
- Still works but LCEL is preferred

**Key Classes:**
- `Runnable` - Base interface for LCEL chains
- `ConversationChain` - Legacy chain with built-in memory
- `LLMChain` - Basic chain for LLM calls

**Official Documentation:**
- [LangChain Expression Language (LCEL)](https://python.langchain.com/docs/expression_language/)
- [LangChain Chains](https://python.langchain.com/docs/modules/chains/)
- [LCEL vs Legacy Chains](https://python.langchain.com/docs/expression_language/why)

**Relevance to Simple Chatbot:**
✅ **ESSENTIAL** - Chains orchestrate the conversation flow. We'll use either LCEL or `ConversationChain` depending on complexity.

**Decision Needed:** LCEL (modern) vs Legacy Chains (simpler)?

---

#### 1.4 Memory

**Concept:**
- **Memory:** Enables chatbots to remember previous interactions
- **Types:** Buffer (full history), Window (last N messages), Summary (summarized history)
- **Storage:** In-memory, database, file system

**Key Classes:**
- `ConversationBufferMemory` - Stores entire conversation history
- `ConversationBufferWindowMemory` - Keeps last N messages
- `ConversationSummaryMemory` - Summarizes old messages to save tokens
- `ChatMessageHistory` - Low-level message storage

**Official Documentation:**
- [LangChain Memory](https://python.langchain.com/docs/modules/memory/)
- [Memory Types](https://python.langchain.com/docs/modules/memory/types/)

**Relevance to Simple Chatbot:**
✅ **ESSENTIAL** - Without memory, each message is independent. We need memory for context-aware conversations.

**For Simple Chatbot:**
- Start with `ConversationBufferMemory` (simplest)
- Can upgrade to `ConversationBufferWindowMemory` if token limits become an issue
- `ConversationSummaryMemory` for very long conversations (probably overkill initially)

---

#### 1.5 Agents

**Concept:**
- **Agents:** LLMs that can decide which tools to use and in what order
- **Purpose:** Enable dynamic, goal-oriented workflows
- **Types:** Zero-shot, ReAct, Plan-and-execute, etc.

**Key Classes:**
- `AgentExecutor` - Runs agents with tools
- `create_react_agent` - Creates ReAct-style agent
- `Tool` - Functions agents can use

**Official Documentation:**
- [LangChain Agents](https://python.langchain.com/docs/modules/agents/)
- [Agent Types](https://python.langchain.com/docs/modules/agents/agent_types/)

**Relevance to Simple Chatbot:**
❌ **NOT NEEDED** (for basic chatbot) - Agents are for chatbots that need to:
- Use external tools (calculators, search, databases)
- Make decisions about actions
- Perform multi-step reasoning with tools

**When to Use Agents:**
- Chatbot needs to search the web
- Chatbot needs to query databases
- Chatbot needs to perform calculations
- Chatbot needs to call external APIs

**For Our Simple Chatbot:**
- No tools needed initially
- No decision-making required
- Just conversation → **Use Chains, not Agents**

---

#### 1.6 Tools (Not Needed for Simple Chatbot)

**Concept:**
- **Tools:** Functions that agents can use (calculators, search, etc.)
- **Purpose:** Extend chatbot capabilities beyond conversation

**Relevance to Simple Chatbot:**
❌ **NOT NEEDED** - Tools are only used with Agents. Since we're not using Agents for a simple chatbot, we don't need Tools.

---

#### 1.7 Document Loaders & Text Splitters (RAG Components)

**Concept:**
- **Document Loaders:** Load documents from various sources (PDFs, websites, etc.)
- **Text Splitters:** Chunk documents into manageable pieces
- **Purpose:** Enable Retrieval-Augmented Generation (RAG)

**Relevance to Simple Chatbot:**
❓ **OPTIONAL** - Only needed if chatbot should:
- Answer questions about documents
- Have knowledge beyond its training data
- Access external information sources

**For Our Simple Chatbot:**
- If purely conversational → **NOT NEEDED**
- If needs document knowledge → **NEEDED**

**Decision Needed:** Does the chatbot need RAG capabilities?

---

#### 1.8 Embeddings & VectorStores (RAG Components)

**Concept:**
- **Embeddings:** Convert text to vector representations
- **VectorStores:** Store and search embeddings (FAISS, Pinecone, etc.)
- **Purpose:** Enable semantic search for RAG

**Relevance to Simple Chatbot:**
❓ **OPTIONAL** - Only needed for RAG (see Document Loaders above).

---

#### 1.9 Output Parsers

**Concept:**
- **Output Parsers:** Convert LLM output into structured formats
- **Types:** JSON, lists, Pydantic models, etc.

**Key Classes:**
- `PydanticOutputParser` - Parse into Pydantic models
- `JsonOutputParser` - Parse JSON responses
- `CommaSeparatedListOutputParser` - Parse lists

**Official Documentation:**
- [LangChain Output Parsers](https://python.langchain.com/docs/modules/model_io/output_parsers/)

**Relevance to Simple Chatbot:**
❓ **OPTIONAL** - Only needed if:
- Responses need to be structured (JSON, lists, etc.)
- We want to validate response format
- We need to extract specific information

**For Our Simple Chatbot:**
- If responses are free-form text → **NOT NEEDED**
- If responses need structure → **NEEDED**

---

### 2. Which Abstractions Apply to Simple Chatbot?

**Essential Components (Must Have):**
1. ✅ **Chat Models** (`ChatOpenAI`) - Core LLM interface
2. ✅ **Prompt Templates** (`ChatPromptTemplate`) - Structure conversations
3. ✅ **Chains** (LCEL or `ConversationChain`) - Orchestrate flow
4. ✅ **Memory** (`ConversationBufferMemory`) - Maintain context

**Optional Components (May Need):**
5. ❓ **Output Parsers** - Only if structured responses needed
6. ❓ **Document Loaders/Text Splitters** - Only if RAG needed
7. ❓ **Embeddings/VectorStores** - Only if RAG needed

**Not Needed (For Simple Chatbot):**
8. ❌ **Agents** - Too complex for basic conversation
9. ❌ **Tools** - Only used with Agents
10. ❌ **Legacy LLM classes** - Use Chat Models instead

---

### 3. Simple Chatbot Architecture Pattern

**Recommended Pattern (as of December 2025):**

```
User Input
    ↓
ChatPromptTemplate (with system message + history placeholder)
    ↓
Chat Model (ChatOpenAI)
    ↓
AI Response
    ↓
Update Memory (ConversationBufferMemory)
    ↓
Display to User
```

**Components Needed:**
1. `ChatOpenAI` - The LLM
2. `ChatPromptTemplate` - Prompt structure
3. `ConversationBufferMemory` - Conversation history
4. `MessagesPlaceholder` - Inject history into prompt
5. Chain (LCEL or `ConversationChain`) - Connect everything

---

### 4. LCEL vs Legacy Chains Decision

**LangChain Expression Language (LCEL) - Modern (as of December 2025):**

**Pros:**
- ✅ Declarative, readable syntax
- ✅ Type-safe
- ✅ Built-in streaming support
- ✅ Composable and testable
- ✅ Recommended by LangChain team

**Cons:**
- ⚠️ Slightly more complex syntax
- ⚠️ Newer (less legacy examples)

**Example LCEL Pattern:**
```python
# Pseudo-code (not actual implementation)
chain = (
    ChatPromptTemplate.from_messages([...])
    | ChatOpenAI()
    | StrOutputParser()
)
```

**Legacy Chains - Traditional:**

**Pros:**
- ✅ Simpler for basic use cases
- ✅ More examples available
- ✅ `ConversationChain` has built-in memory

**Cons:**
- ⚠️ Less flexible
- ⚠️ Not recommended for new projects
- ⚠️ Limited streaming support

**Example Legacy Pattern:**
```python
# Pseudo-code (not actual implementation)
chain = ConversationChain(
    llm=ChatOpenAI(),
    memory=ConversationBufferMemory()
)
```

**Recommendation:**
- **For Learning/Simple Bot:** Legacy `ConversationChain` might be easier
- **For Modern Best Practices:** Use LCEL
- **Decision Needed:** Which approach should we use?

---

### 5. Memory Management for Simple Chatbot

**Options:**

1. **ConversationBufferMemory** (Recommended for Start)
   - Stores all messages
   - Simple to use
   - Good for short conversations
   - ⚠️ Can hit token limits with long conversations

2. **ConversationBufferWindowMemory**
   - Keeps last N messages
   - Prevents token limit issues
   - ⚠️ Loses older context

3. **ConversationSummaryMemory**
   - Summarizes old messages
   - Keeps context while saving tokens
   - ⚠️ More complex, may lose nuance

**For Simple Chatbot:**
- Start with `ConversationBufferMemory`
- Upgrade if token limits become an issue
- Each Streamlit session = separate memory instance

---

## ✅ Decision Made + Rationale

<!-- Which LangChain components will you use and why? -->

### Decision: Components for Simple Chatbot

**Selected Components:**

1. **Chat Models:**
   - ✅ `ChatOpenAI` (from `langchain-openai`)
   - **Rationale:** Most mature, well-documented, cost-effective for development

2. **Prompt Templates:**
   - ✅ `ChatPromptTemplate` with `MessagesPlaceholder`
   - **Rationale:** Standard way to structure conversations, supports history injection

3. **Chains:**
   - ⚠️ **DECISION NEEDED:** LCEL vs `ConversationChain`
   - **Tentative:** Start with `ConversationChain` for simplicity, can migrate to LCEL later
   - **Rationale:** Simpler for initial implementation, has built-in memory support

4. **Memory:**
   - ✅ `ConversationBufferMemory`
   - **Rationale:** Simplest option, sufficient for basic chatbot, can upgrade later

5. **Message Types:**
   - ✅ `SystemMessage`, `HumanMessage`, `AIMessage`
   - **Rationale:** Standard LangChain message structure

**Not Using (For Now):**
- ❌ Agents - Overkill for simple conversation
- ❌ Tools - Only needed with Agents
- ❌ Document Loaders - No RAG requirement initially
- ❌ Output Parsers - Free-form text responses are fine
- ❌ VectorStores - No RAG needed

### Architecture Decision:

**Simple Chatbot Flow:**
```
Streamlit UI
    ↓ (user input)
ChatPromptTemplate (system + history + user message)
    ↓
ChatOpenAI
    ↓ (AI response)
ConversationBufferMemory (store in session)
    ↓
Streamlit UI (display response)
```

**Component Structure:**
- **Chat Model:** `ChatOpenAI` instance
- **Prompt:** `ChatPromptTemplate` with system message
- **Memory:** `ConversationBufferMemory` per Streamlit session
- **Chain:** `ConversationChain` (or LCEL chain) connecting all components

---

## 📎 Evidence/Proof

<!-- Screenshots, doc links, diagrams proving your understanding -->

### Official Documentation Links

1. **Chat Models:**
   - [LangChain Chat Models Documentation](https://python.langchain.com/docs/integrations/chat/)
   - [OpenAI Chat Integration](https://python.langchain.com/docs/integrations/chat/openai)

2. **Prompt Templates:**
   - [Chat Prompt Templates](https://python.langchain.com/docs/modules/model_io/prompts/prompt_templates/prompt_templates_chat)
   - [Messages Placeholder](https://python.langchain.com/docs/modules/model_io/prompts/prompt_templates/prompt_templates_chat#messagesplaceholder)

3. **Chains:**
   - [LangChain Expression Language (LCEL)](https://python.langchain.com/docs/expression_language/)
   - [LCEL Why Use It](https://python.langchain.com/docs/expression_language/why)
   - [Legacy Chains](https://python.langchain.com/docs/modules/chains/)
   - [Conversation Chain](https://python.langchain.com/docs/modules/chains/popular/chat_vector_db)

4. **Memory:**
   - [LangChain Memory Overview](https://python.langchain.com/docs/modules/memory/)
   - [Memory Types](https://python.langchain.com/docs/modules/memory/types/)
   - [Conversation Buffer Memory](https://python.langchain.com/docs/modules/memory/types/buffer)

5. **Chatbot Tutorials:**
   - [LangChain Chatbot Quickstart](https://python.langchain.com/docs/use_cases/chatbots/)
   - [Building Chatbots with LangChain](https://python.langchain.com/docs/tutorials/chatbot/)

### Conceptual Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit UI                          │
│  ┌──────────────┐              ┌──────────────┐        │
│  │ User Input   │              │ AI Response  │        │
│  └──────┬───────┘              └──────▲───────┘        │
└─────────┼──────────────────────────────┼────────────────┘
          │                              │
          │                              │
          ▼                              │
┌─────────────────────────────────────────┐              │
│      ChatPromptTemplate                  │              │
│  ┌───────────────────────────────────┐  │              │
│  │ SystemMessage: "You are helpful"  │  │              │
│  │ MessagesPlaceholder (history)     │  │              │
│  │ HumanMessage (user input)         │  │              │
│  └───────────────────────────────────┘  │              │
└──────────────┬──────────────────────────┘              │
               │                                          │
               ▼                                          │
┌──────────────────────────────────────────┐             │
│           ChatOpenAI                      │             │
│      (GPT-3.5-turbo or GPT-4)            │             │
└──────────────┬───────────────────────────┘             │
               │                                          │
               │ AIMessage (response)                     │
               │                                          │
               ▼                                          │
┌──────────────────────────────────────────┐             │
│    ConversationBufferMemory              │             │
│  ┌────────────────────────────────────┐ │             │
│  │ [HumanMessage, AIMessage, ...]     │ │             │
│  │ (conversation history)              │ │             │
│  └────────────────────────────────────┘ │             │
└──────────────────────────────────────────┘             │
                                                          │
                    (history fed back to prompt)          │
                                                          │
                    ──────────────────────────────────────┘
```

### Key Takeaways

1. **Core Components for Simple Chatbot:**
   - Chat Model (ChatOpenAI)
   - Prompt Template (ChatPromptTemplate)
   - Memory (ConversationBufferMemory)
   - Chain (ConversationChain or LCEL)

2. **Not Needed for Simple Chatbot:**
   - Agents (too complex)
   - Tools (only with agents)
   - RAG components (unless document knowledge needed)

3. **Modern Approach (as of December 2025):**
   - LCEL is recommended but `ConversationChain` is simpler
   - Decision needed on which to use

4. **Memory Strategy:**
   - Start with `ConversationBufferMemory`
   - Upgrade if token limits become an issue

---

## 🎯 Summary

**For a simple chatbot, we need:**
1. ✅ Chat Models (`ChatOpenAI`)
2. ✅ Prompt Templates (`ChatPromptTemplate`)
3. ✅ Memory (`ConversationBufferMemory`)
4. ✅ Chains (`ConversationChain` or LCEL)

**We don't need:**
- ❌ Agents
- ❌ Tools
- ❌ RAG components (initially)

**Open Questions:**
- LCEL vs Legacy Chains?
- RAG capabilities needed?
- Structured output needed?
- Streaming responses needed?

---

**Research Completed:** ✅  
**Date:** December 2025  
**Status:** Ready for implementation decisions

