# streamlit_app.py
import streamlit as st
from replicate_utils import ask_mistral
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
import os

# Load documents
loader = TextLoader("Insurance.txt")  
raw_docs = loader.load()

# Split into chunks
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(raw_docs)

# Create vector store
embedding_model = HuggingFaceEmbeddings()
vectordb = Chroma.from_documents(docs, embedding_model)
retriever = vectordb.as_retriever()

# Streamlit UI
st.set_page_config(page_title="SarahGPT (Replicate)", layout="centered")
st.title("🤖 SarahGPT – Custom Document Chatbot")
st.markdown("Ask anything based on your uploaded documents.")

user_input = st.text_input("Your Question:")
if user_input:
    matched_docs = retriever.get_relevant_documents(user_input)
    context = "\n".join([doc.page_content for doc in matched_docs])
    with st.spinner("Thinking..."):
        response = ask_mistral(prompt=user_input, context=context)
    st.markdown(f"**Answer:** {response}")


