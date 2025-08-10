# chatbot_page.py
import streamlit as st
from chatbot import agent  # Your chatbot logic
from langchain_core.messages import HumanMessage

st.set_page_config(page_title="Movie ChatBot", page_icon="🎙️")
st.title("🎙️ Movie ChatBot")


CONFIG = {"configurable": {"thread_id": "1"}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])



# 2️⃣ Chat input for new message
user_input = st.chat_input("Ask something about movies...")

if user_input:

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    response = agent.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)
    
    ai_message = response['messages'][-1].content
    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    with st.chat_message('assistant'):
        st.text(ai_message)