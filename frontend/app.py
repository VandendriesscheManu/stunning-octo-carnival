import os
import uuid
import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8001")

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
        r = requests.post(
            f"{API_BASE_URL}/chat",
            json={"session_id": st.session_state.session_id, "user_message": prompt},
            timeout=60,
        )
        r.raise_for_status()
        assistant = r.json()["assistant_message"]
    except Exception as e:
        assistant = f"Er ging iets mis met de API: {e}"

    st.session_state.messages.append({"role": "assistant", "content": assistant})
    with st.chat_message("assistant"):
        st.write(assistant)
