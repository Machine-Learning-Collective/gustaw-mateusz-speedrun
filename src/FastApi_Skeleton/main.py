import logging
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status

from Chat_Service import ChatService
from LangChain_Conversational_Agent.llm_factory import LLMSettings
from Pydantic_Base_Models import ChatRequest, ChatResponse, HealthResponse, Message

APP_VERSION = "1.0.0"

logger = logging.getLogger(__name__)


def create_app(service: Optional[ChatService] = None) -> FastAPI:
    """Builds the API. Tests pass their own service; otherwise one is built from the environment."""
    if service is None:
        load_dotenv()
        service = ChatService.from_settings(LLMSettings.from_env())

    app = FastAPI(title="Chat API", version=APP_VERSION)
    app.state.chat_service = service

    def get_service(request: Request) -> ChatService:
        return request.app.state.chat_service

    @app.get("/health", response_model=HealthResponse)
    def health(chat: ChatService = Depends(get_service)) -> HealthResponse:
        return HealthResponse(
            status="ok", app="chat-api", version=APP_VERSION, llm_provider=chat.llm_description
        )

    @app.post("/chat", response_model=ChatResponse)
    def post_chat(body: ChatRequest, chat: ChatService = Depends(get_service)) -> ChatResponse:
        try:
            return chat.chat(body)
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc
        except Exception as exc:
            # Provider errors (timeouts, rate limits, invalid key) are not the client's fault,
            # and their details should not leak to the client either.
            logger.exception("Language model request failed")
            raise HTTPException(
                status.HTTP_502_BAD_GATEWAY, "The language model request failed. Try again."
            ) from exc

    @app.get("/sessions/{session_id}/messages", response_model=List[Message])
    def session_messages(session_id: str, chat: ChatService = Depends(get_service)) -> List[Message]:
        if not chat.has_session(session_id):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Unknown session")
        return chat.get_history(session_id)

    @app.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_session(session_id: str, chat: ChatService = Depends(get_service)) -> Response:
        chat.reset(session_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return app


app = create_app()
