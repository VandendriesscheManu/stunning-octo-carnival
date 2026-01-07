import os
import requests

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")


def ollama_chat(messages: list[dict]) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
    }
    r = requests.post(f"{OLLAMA_BASE_URL}/api/chat", json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()
    return data["message"]["content"]
