import streamlit as st
import openai

# ✅ Initialize new v1.x OpenAI client
client = openai.OpenAI(api_key="sk-...")  # Replace with your key

# 📄 Page config
st.set_page_config(
    page_title="SarahGPT 🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ⚙️ Sidebar settings
st.sidebar.title("Settings")
model = st.sidebar.selectbox("Model", ["gpt-4o", "gpt-3.5-turbo"])
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)

# 💬 Chat history session state
if "history" not in st.session_state:
    st.session_state.history = []

# 🧠 Title & intro
st.title("SarahGPT")
st.markdown("Ask anything — Sarah is here to help!")

# 🗣️ User prompt
prompt = st.text_input("You:", placeholder="Type your question here…")

# 🚀 On send
if st.button("Send") and prompt:
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.spinner("Sarah is thinking..."):
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are Sarah, a friendly assistant."}
            ] + st.session_state.history,
            temperature=temperature,
        )
    answer = response.choices[0].message.content
    st.session_state.history.append({"role": "assistant", "content": answer})

# 📜 Render conversation
for msg in st.session_state.history:
    tag = "**You:**" if msg["role"] == "user" else "**SarahGPT:**"
    st.markdown(f"{tag} {msg['content']}")

# 🧹 Clear history
if st.sidebar.button("Clear chat"):
    st.session_state.history = []

