from core.mcp_client import mcp_lookup
from core.ollama_client import ollama_chat


SYSTEM_PROMPT = """You are a professional marketing consultant AI assistant. Your role is to create comprehensive marketing plans based on product details provided by users.

When generating a marketing plan, include:
1. Executive Summary - Brief overview of the product and marketing strategy
2. Target Audience - Demographics, psychographics, and customer personas
3. Unique Selling Proposition (USP) - What makes this product stand out
4. Marketing Channels - Recommended channels (social media, email, content marketing, paid ads, etc.)
5. Content Strategy - Types of content to create and distribution plan
6. Budget Recommendations - Suggested budget allocation across channels
7. Timeline - Phased rollout plan with milestones
8. Key Metrics - KPIs to track success

Be professional, thorough, and actionable. Tailor your recommendations to the specific product details provided.
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


def run_marketing_plan_agent(user_message: str, history: list[dict]) -> str:
    mcp_context = mcp_lookup(query=user_message)
    messages = _to_ollama_messages(history, user_message, mcp_context)
    return ollama_chat(messages)
