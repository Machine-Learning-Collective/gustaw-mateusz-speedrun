import os
from http.client import HTTPException

from fastapi import FastAPI
from dotenv import load_dotenv

from Pydantic_Base_Models import (
    ConversationConfig,
    ChatRequest,
    ChatResponse,
    Message,
    Role,
)
from Pydantic_Base_Models.models import HealthResponse
from langchain_openai import ChatOpenAI
from LangChain_Conversational_Agent import LangChainAgent
from LangChain_Conversational_Agent.langchain_agent import ChatModelError

load_dotenv()
app = FastAPI(title="Chat API", version="0.1.0")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")

chat_model = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model=OPENAI_MODEL_NAME,
    temperature=0.2,
)

config = ConversationConfig(
    max_history_messages=20,
    locale="en",
    enable_memory=True,
    temperature=0.2,
    model_name=OPENAI_MODEL_NAME,
    mode="llm",
    system_prompt="be helpful",
    input_key="messages",
    memory_key="messages",
)

agent = LangChainAgent(
    model=chat_model,
    # tools=[],  # future feature
    config=config,
)

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    session_id = req.session_id or "default"


    try:
        reply_text = agent.send(req.message, session_id=session_id)
    except ChatModelError:
        raise HTTPException(
            status_code=502,
            detail="Upstream LLM/model error, please try again later.",
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unexpected server error.",
        )

    history = agent.get_history(session_id=session_id)
    reply_msg = Message(role=Role.assistant, content=reply_text)

    return ChatResponse(
        session_id=session_id,
        message=reply_msg,
        history=history,
    )

@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        app="chat-api",
        version=app.version or "0.1.0",
    )
