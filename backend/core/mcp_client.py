import os
import requests

MCP_BASE_URL = os.getenv("MCP_BASE_URL", "http://mcp-server:8000")


def mcp_lookup(query: str) -> str:
    try:
        r = requests.post(f"{MCP_BASE_URL}/lookup", json={"query": query}, timeout=10)
        r.raise_for_status()
        return r.json().get("result", "")
    except Exception:
        return ""
