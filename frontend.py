from database import save_message, load_messages
from database import get_all_messages
import streamlit as st
import time
import uuid
from backend import stream_ai_response
st.set_page_config(page_title="LangGraph Chatbot", layout="wide")
st.title("🤖 LangGraph Chatbot")

# ================= SIDEBAR =================
with st.sidebar:
    st.header("💬 My Conversations")

    # init chat storage
    if "chats" not in st.session_state:
        st.session_state.chats = {}

    if "current_chat" not in st.session_state:
        new_id = str(uuid.uuid4())
        st.session_state.current_chat = new_id
        st.session_state.chats[new_id] = []

    # -------- NEW CHAT BUTTON --------
    if st.button("➕ New Chat"):
        new_id = str(uuid.uuid4())
        st.session_state.current_chat = new_id
        st.session_state.chats[new_id] = []
        st.rerun()

    st.divider()

    # -------- CHAT LIST --------
    for chat_id in st.session_state.chats.keys():
        if st.button(chat_id[:8], key=chat_id):
            st.session_state.current_chat = chat_id
            st.rerun()

# ================= CURRENT CHAT =================
current_chat_id = st.session_state.current_chat
if current_chat_id not in st.session_state.chats:
    st.session_state.chats[current_chat_id] = []

messages = st.session_state.chats[current_chat_id]

# Load from DB if empty
if not messages:
    db_messages = load_messages(current_chat_id)
    for role, content in db_messages:
        messages.append({"role": role, "content": content})

# -------- DISPLAY OLD MESSAGES --------
for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ================= INPUT =================
user_input = st.chat_input("Type your message...")

if user_input:
    # save user message
    messages.append({"role": "user", "content": user_input})
    save_message(current_chat_id, "user", user_input)

    with st.chat_message("user"):
        st.markdown(user_input)

    # -------- STREAMING RESPONSE --------
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        for token in stream_ai_response(user_input, current_chat_id):
            full_response += token
            message_placeholder.markdown(full_response + "▌")
            time.sleep(0.01)

        message_placeholder.markdown(full_response)

    # save assistant message
    messages.append({"role": "assistant", "content": full_response})
    save_message(current_chat_id, "assistant", full_response)


st.divider()
st.subheader("📊 Stored Conversations (Database View)")

if st.button("Show All Messages"):
    data = get_all_messages()

    import pandas as pd
    df = pd.DataFrame(
        data,
        columns=["ID", "Thread ID", "Role", "Message", "Timestamp"]
    )

    st.dataframe(df, use_container_width=True)