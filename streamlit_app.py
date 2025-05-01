import os
import streamlit as st
from dotenv import load_dotenv

# Import the new client
from openai import OpenAI

# Load API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Instantiate v1 client
client = OpenAI(api_key=api_key)

# Page configuration
st.set_page_config(
    page_title="SarahGPT 🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Sidebar settings
st.sidebar.title("Settings")
model = st.sidebar.selectbox("Model", ["gpt-4o-mini", "gpt-3.5-turbo"])
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# App header
st.title("SarahGPT")
st.markdown("Ask anything — Sarah is here to help!")

# User input
prompt = st.text_input("You:", placeholder="Type your question here…")

# Send button triggers API call
if st.button("Send") and prompt:
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.spinner("Sarah is thinking..."):
        # Use the new client.chat.completions endpoint
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": "You are Sarah, a friendly assistant."}]
                     + st.session_state.history,
            temperature=temperature,
        )
    answer = response.choices[0].message.content
    st.session_state.history.append({"role": "assistant", "content": answer})

# Display chat history
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**SarahGPT:** {msg['content']}")

# Clear chat history
if st.sidebar.button("Clear chat"):
    st.session_state.history = []

