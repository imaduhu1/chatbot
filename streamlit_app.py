# streamlit_app.py

import streamlit as st
from replicate_utils import ask_mistral
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

# -------------------------------
# 🔹 Load and preprocess documents
# -------------------------------
st.set_page_config(page_title="SarahGPT (Replicate)", layout="centered")
st.title("🤖 SarahGPT – Enterprise Risk Chatbot")
st.markdown("Ask any question based on the *EnterpriseRisk.txt* document below.")

# Load the enterprise risk document
loader = TextLoader("EnterpriseRisk.txt")
raw_documents = loader.load()

# Split into smaller chunks for embeddings
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(raw_documents)

# -------------------------------
# 🔹 Set up vector search
# -------------------------------
embedding_model = HuggingFaceEmbeddings()
vectordb = Chroma.from_documents(chunks, embedding_model)
retriever = vectordb.as_retriever()

# -------------------------------
# 🔹 Chat interface
# -------------------------------
user_question = st.text_input("Ask your question here:")

if user_question:
    # Retrieve relevant context from the document
    top_matches = retriever.get_relevant_documents(user_question)
    context = "\n".join([doc.page_content for doc in top_matches])

    # Query Mistral model via Replicate
    with st.spinner("SarahGPT is thinking..."):
        response = ask_mistral(prompt=user_question, context=context)

    st.markdown("### 💬 Response")
    st.markdown(f"**SarahGPT:** {response}")

