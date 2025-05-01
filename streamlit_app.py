import os
import streamlit as st
from dotenv import load_dotenv

# Import the new OpenAI v1 client
from openai import OpenAI

# Load API key
load_dotenv()
api_key = os.getenv("https://github.com/imaduhu1/chatbot/blob/main/streamlit_app.py")

# Instantiate v1 client
client = OpenAI(api_key=api_key)

# Page config
st.set_page_config(
    page_title="SarahGPT 🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Sidebar
st.sidebar.title("Settings")
model = st.sidebar.selectbox("Model", ["gpt-4o-mini", "gpt-3.5-turbo"])
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)

# Chat history init
if "history" not in st.session_state:
    st.session_state.history = []

# Header
st.title("SarahGPT")
st.markdown("Ask anything — Sarah is here to help!")

# Input box
prompt = st.text_input("You:", placeholder="Type your question here…")

# On Send…
if st.button("Send") and prompt:
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.spinner("Sarah is thinking..."):
        # ← v1 client call
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": "You are Sarah, a friendly assistant."}]
                     + st.session_state.history,
            temperature=temperature,
        )
    answer = response.choices[0].message.content
    st.session_state.history.append({"role": "assistant", "content": answer})

# Render chat
for msg in st.session_state.history:
    tag = "**You:**" if msg["role"] == "user" else "**SarahGPT:**"
    st.markdown(f"{tag} {msg['content']}")

# Clear button
if st.sidebar.button("Clear chat"):
    st.session_state.history = []
