from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.db import init_db, save_message, get_history
from core.agents import run_sinterklaas_agent

app = FastAPI(title="Sinterklaas Chat API", version="0.1.0")


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
def history(session_id: str):
    return {"session_id": session_id, "messages": get_history(session_id)}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        history_msgs = get_history(req.session_id)

        save_message(req.session_id, role="user", content=req.user_message)

        assistant = run_sinterklaas_agent(
            user_message=req.user_message,
            history=history_msgs,
        )

        save_message(req.session_id, role="assistant", content=assistant)

        return ChatResponse(session_id=req.session_id, assistant_message=assistant)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
