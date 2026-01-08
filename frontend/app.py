import os
import uuid
import requests
import streamlit as st

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://chip-drilling-sky-conditioning.trycloudflare.com",
)

# Lees API key uit env (Streamlit Cloud Secrets)
API_KEY = os.getenv("API_KEY", "")

st.set_page_config(page_title="Sinterklaas Chat", page_icon="🎁")

st.title("🎁 Sinterklaas Chat")
st.caption("Een simpele demo: Streamlit → FastAPI → MCP → Ollama → Postgres")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.subheader("Instellingen")
    st.write("API:", API_BASE_URL)
    st.write("Session:", st.session_state.session_id)

    # Toon niet de volledige key in UI
    st.write("API key:", "✅ ingesteld" if API_KEY else "⚠️ niet ingesteld")

    if st.button("Nieuwe chat"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

# Toon berichten
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

prompt = st.chat_input("Typ hier je bericht aan Sinterklaas...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        headers = {}
        if API_KEY:
            headers["X-API-KEY"] = API_KEY

        r = requests.post(
            f"{API_BASE_URL}/chat",
            json={"session_id": st.session_state.session_id, "user_message": prompt},
            headers=headers,
            timeout=60,
        )

        # Specifieke error handling voor auth
        if r.status_code == 401:
            raise Exception("Unauthorized (401) — controleer API_KEY in Streamlit Secrets en in je .env op de server.")

        r.raise_for_status()
        assistant = r.json().get("assistant_message", "")

        if not assistant:
            assistant = "Ik kreeg een leeg antwoord terug van de API."

    except Exception as e:
        assistant = f"Er ging iets mis met de API: {e}"

    st.session_state.messages.append({"role": "assistant", "content": assistant})
    with st.chat_message("assistant"):
        st.write(assistant)
