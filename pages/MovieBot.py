# chatbot_page.py
import streamlit as st
from chatbot import get_response  # Your chatbot logic
st.set_page_config(page_title="Movie ChatBot", page_icon="🎙️")
st.title("🎙️ Movie ChatBot")

st.title("🎙️ Movie ChatBot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []



# 2️⃣ Chat input for new message
user_input = st.chat_input("Ask something about movies...")

if user_input:
    # Add user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get bot response
    response, updated_history = get_response(user_input, st.session_state.chat_history)
    st.session_state.chat_history = updated_history

    # Add bot message
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)