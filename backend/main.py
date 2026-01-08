import os
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from core.db import init_db, save_message, get_history
from core.agents import run_sinterklaas_agent

app = FastAPI(title="Sinterklaas Chat API", version="0.1.0")

# Leest API key uit .env (of lege string als je geen key wil)
API_KEY = os.getenv("API_KEY", "")


def require_api_key(x_api_key: str = Header(default="")):
    """
    Simpele beveiliging:
    - Als API_KEY leeg is: geen check (dev mode)
    - Als API_KEY gezet is: client moet X-API-KEY header meesturen
    """
    if API_KEY and x_api_key != API_KEY:
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

        assistant = run_sinterklaas_agent(
            user_message=req.user_message,
            history=history_msgs,
        )

        save_message(req.session_id, role="assistant", content=assistant)

        return ChatResponse(session_id=req.session_id, assistant_message=assistant)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
