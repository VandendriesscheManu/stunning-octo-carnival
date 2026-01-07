from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Demo MCP Server", version="0.1.0")


class LookupRequest(BaseModel):
    query: str


SINTERKLAAS_CONTEXT = """Feiten over Sinterklaas:
- Sinterklaas komt in België aan in november.
- Pakjesavond is op 5 december.
- Sinterklaas is vriendelijk en geeft complimentjes.
- Spreek kindjes moed in en wees positief.
"""


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/lookup")
def lookup(req: LookupRequest):
    # In een echte versie zou je hier web search / tools / vector DB doen.
    # Voor demo: altijd dezelfde context teruggeven.
    return {"result": SINTERKLAAS_CONTEXT}
