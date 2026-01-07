from core.mcp_client import mcp_lookup
from core.ollama_client import ollama_chat


SYSTEM_PROMPT = """Je bent Sinterklaas en je chat met kindjes.
Regels:
- Wees vriendelijk, vrolijk en eenvoudig (korte zinnen).
- Vraag nooit naar adres, telefoonnummer, school of andere persoonlijke gegevens.
- Als een kind persoonlijke info geeft: zeg vriendelijk dat dat niet nodig is.
- Geen enge of volwassen onderwerpen. Geen geweld. Geen illegale tips.
- Als je iets niet weet: zeg eerlijk dat je het niet zeker weet.
- Je mag vragen stellen zoals: "Wat hoop je te krijgen?" maar hou het veilig.
"""


def _to_ollama_messages(history: list[dict], user_message: str, mcp_context: str) -> list[dict]:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if mcp_context:
        messages.append({"role": "system", "content": f"Extra context (MCP):\n{mcp_context}"})

    # neem laatste 12 berichten max (om context klein te houden)
    for m in history[-12:]:
        role = m.get("role", "user")
        content = m.get("content", "")
        if role in ("user", "assistant", "system") and content:
            messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": user_message})
    return messages


def run_sinterklaas_agent(user_message: str, history: list[dict]) -> str:
    mcp_context = mcp_lookup(query=user_message)
    messages = _to_ollama_messages(history, user_message, mcp_context)
    return ollama_chat(messages)
