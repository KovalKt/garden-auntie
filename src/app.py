import sys
import os
import streamlit as st
from src.retriever import get_answer


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Garden Auntie",
    page_icon="🌱",
    layout="centered",
)

# ── Simple styling ─────────────────────────────────────────────────────────────
st.markdown("""
    <style>
        .source-pill {
            display: inline-block;
            background: #e8f5e9;
            color: #2e7d32;
            border-radius: 12px;
            padding: 2px 10px;
            font-size: 0.78rem;
            margin: 2px;
        }
    </style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.title("🌱 Garden Auntie")
st.caption("Твоя розумна помічниця з садівництва")
st.divider()

# ── Chat history ───────────────────────────────────────────────────────────────
# st.session_state persists data between Streamlit reruns (every interaction).
# Without this, the chat history would reset on every message.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render all previous messages from history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # Re-render source pills if this was an assistant message
        if msg["role"] == "assistant" and msg.get("sources"):
            pills = " ".join(
                f'<span class="source-pill">📄 {os.path.basename(s)}</span>'
                for s in msg["sources"]
            )
            st.markdown(pills, unsafe_allow_html=True)

# ── Input ──────────────────────────────────────────────────────────────────────
# st.chat_input renders the message box pinned to the bottom of the page.
# It returns the typed text when the user hits Enter, otherwise None.
if question := st.chat_input("Запитай мене про садівництво..."):

    # Show the user's message immediately in the chat
    with st.chat_message("user"):
        st.markdown(question)

    # Save it to history
    st.session_state.messages.append({"role": "user", "content": question})

    # Get answer from RAG pipeline, show a spinner while waiting
    with st.chat_message("assistant"):
        with st.spinner("Думаю..."):
            result = get_answer(question, history=st.session_state.messages)

        answer = result["answer"]
        sources = result["sources"]

        # Display the answer
        st.markdown(answer)

        # Display source pills below the answer
        if sources:
            pills = " ".join(
                f'<span class="source-pill">📄 {os.path.basename(s)}</span>'
                for s in sources
            )
            st.markdown(pills, unsafe_allow_html=True)

    # Save assistant response + sources to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
    })
