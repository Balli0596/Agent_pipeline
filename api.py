
from functools import lru_cache

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from agent.controller import build_agent, ask_agent

app = FastAPI(
    title="AI Agent API",
    description="Chat API for weather and stock tools",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    reply: str


@lru_cache(maxsize=1)
def get_agent():
    return build_agent()


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "AI Agent API"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    message = request.message.strip()

    if not message:
        raise HTTPException(
            status_code=422,
            detail="Message cannot be empty.",
        )

    try:
        reply = ask_agent(get_agent(), message)

        if not isinstance(reply, str):
            reply = str(reply)

        return ChatResponse(reply=reply)

    except Exception:
        # Keep API keys and internal exception details out of responses.
        raise HTTPException(
            status_code=500,
            detail="The agent could not process your request. Please try again.",
        )
