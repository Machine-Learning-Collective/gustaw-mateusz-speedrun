# Milestone 4: Reflection & Handoff

> *"Character development arc complete"*

## Timeline

| Date | Event |
|---|---|
| 21 Nov 2025 | Project brief |
| 27 Nov 2025 | Milestone 1 merged: research and version validation (5 documents) |
| 1 Dec 2025 | Milestone 2 merged: isolated components, 25 tests |
| Dec 2025 – Sep 2026 | Paused |
| Oct 2026 | Milestones 3 and 4: integration, fixes, CI, documentation |

## What worked

**Researching before coding.** Every choice in Milestone 1 was written down with its reason. Ten months later it was still possible to see why each library had been picked and to check whether that reason still held, which is exactly what Milestone 3 needed when parts of LangChain turned out to be deprecated.

**Building components in isolation.** Because each component already had a clear interface and its own tests, integration was mostly wiring. The agent accepted any LangChain chat model, so switching from the test model to OpenAI was one constructor argument.

**Pydantic at the boundaries.** Validation written once in the models gave the API correct 422 responses for free, and the same models drive the UI's error messages.

## What did not, and what we take from it

**Nobody ran the tests from a clean checkout.** For ten months, a plain `pytest` from the project root failed on all five test modules, and `uv run pytest` would have failed on a missing dependency. Everyone ran tests in an already-configured local environment, so nobody noticed.
→ *CI from the first commit. A test suite only counts if it runs somewhere other than the author's machine.*

**Tests that asserted the wrong thing.** "Empty input does not crash" passed because `send("")` returned normally; the crash came on the next `get_history()`. The test checked that an action finished, not that the system was in a valid state afterwards.
→ *After an action, assert on the resulting state, not only on the return value.*

**One rule for data with different origins.** A 4000-character limit makes sense for what a person types and none for what a model generates, but both went through the same `Message` model. It would have failed on the first long answer from a real model.
→ *Put limits where the data enters the system, and ask who produces it.*

**The lock file was ignored.** `uv.lock` was in `.gitignore`, although the brief asked for it to be committed. Ten months later the APIs chosen in Milestone 1 (`RunnableWithMessageHistory`, `InMemoryChatMessageHistory`) were deprecated, and without a lock file there was no record of which versions had actually worked.
→ *Commit the lock file. Research decisions have a shelf life; record the date and versions they were made against.*

**Research listed legacy APIs.** The Milestone 1 notes recommended `ConversationChain` and `ConversationBufferMemory`, which were already legacy in LangChain 0.3. Milestone 2 correctly used the newer composition style instead, but the research document and the code disagreed.
→ *When checking documentation, look at deprecation notices and migration guides, not only API references.*

**Git history.** Milestone 2 arrived as four commits with the same message, which makes it hard to see what changed when.
→ *One logical change per commit, with a message that describes that change.*

## Known limitations

- **History lives in memory.** It is lost when the server restarts, and the number of sessions is not bounded.
- **No authentication or rate limiting on the API.** Anyone who can reach it can spend the API budget.
- **No streaming.** Replies appear only when complete.
- **The UI calls the service directly**, not through the API, so the two run as separate processes with separate histories.
- **One provider.** OpenAI or demo.

## Handoff

**Run it:** see [README](../README.md#running-it).

**Where to change what:**

| Task | Where |
|---|---|
| Add a provider (e.g. Anthropic, a local model) | Add it to `Provider` and a branch in `build_llm()` in `src/LangChain_Conversational_Agent/llm_factory.py` |
| Persist history | Replace the `HistoryStore` dictionary passed to `LangChainAgent` by `ChatService` with a database-backed mapping |
| Change limits or validation | `src/Pydantic_Base_Models/chat.py` |
| New API endpoint | `create_app()` in `src/FastApi_Skeleton/main.py`, using `ChatService` via `Depends(get_service)` |

**Suggested next steps, in order of value:** persistent history (SQLite is enough), authentication and rate limiting on the API, streaming replies, the UI talking to the API instead of the service, a second provider.
