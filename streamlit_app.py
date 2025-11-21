import streamlit as st
import requests
import uuid
import os

API_URL = os.environ.get("API_URL", "http://127.0.0.1:5000/chat")

st.set_page_config(page_title="Supportive Chatbot", page_icon="🧡")
st.title("Supportive Chatbot — Prototype")
st.markdown("_This is a prototype for non-clinical emotional support. Not a substitute for professional help._")

# Session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "history" not in st.session_state:
    st.session_state.history = []

# User input form
with st.form(key="input_form"):
    user_text = st.text_input("How are you feeling right now?")
    submitted = st.form_submit_button("Send")

    if submitted and user_text:
        payload = {"message": user_text, "session_id": st.session_state.session_id}
        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                bot_reply = response.json().get("reply", "")
                st.session_state.history.append({"user": user_text, "bot": bot_reply})
            else:
                st.error(f"Error: {response.status_code}")
        except Exception as e:
            st.error(f"Error connecting to API: {e}")

# Display chat history
for chat in st.session_state.history:
    st.markdown(f"**You:** {chat['user']}")
    st.markdown(f"**Bot:** {chat['bot']}")
