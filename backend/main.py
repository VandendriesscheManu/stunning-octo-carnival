import os
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from core.db import init_db, save_message, get_history
from core.agents import run_marketing_plan_agent

app = FastAPI(title="Marketing Plan Generator API", version="0.1.0")

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY is not set. Set API_KEY in your .env file.")


def require_api_key(x_api_key: str = Header(default="")):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


class ChatRequest(BaseModel):
    session_id: str
    user_message: str


class ChatResponse(BaseModel):
    session_id: str
    assistant_message: str


@app.on_event("startup")
def _startup():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/history/{session_id}")
def history(session_id: str, _: None = Depends(require_api_key)):
    return {"session_id": session_id, "messages": get_history(session_id)}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, _: None = Depends(require_api_key)):
    try:
        history_msgs = get_history(req.session_id)

        save_message(req.session_id, role="user", content=req.user_message)

        assistant = run_marketing_plan_agent(
            user_message=req.user_message,
            history=history_msgs,
        )

        save_message(req.session_id, role="assistant", content=assistant)

        return ChatResponse(session_id=req.session_id, assistant_message=assistant)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
