from fastapi import FastAPI

from Pydantic_Base_Models.models import HealthResponse

app = FastAPI(title="Chat API", version="0.1.0")


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        app="chat-api",
        version=app.version or "0.1.0",

    )
