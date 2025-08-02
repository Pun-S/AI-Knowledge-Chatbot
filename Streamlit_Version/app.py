import streamlit as st
import os
from document_loader import load_pdf, load_docx, load_txt, chunk_text
from embeddings_store import create_vector_store
from chat_logic import ask_bot

st.set_page_config(page_title="AI Knowledge Chatbot", page_icon="🤖")
st.title("📚 AI Knowledge Chatbot (Free Mistral-7B)")

uploaded_file = st.file_uploader("Upload a PDF, DOCX, or TXT file", type=["pdf", "docx", "txt"])

if uploaded_file:
    with open("temp_file", "wb") as f:
        f.write(uploaded_file.read())
    
    if uploaded_file.name.endswith(".pdf"):
        text = load_pdf("temp_file")
    elif uploaded_file.name.endswith(".docx"):
        text = load_docx("temp_file")
    elif uploaded_file.name.endswith(".txt"):
        text = load_txt("temp_file")
    else:
        st.error("Unsupported file format.")
        st.stop()

    chunks = chunk_text(text)
    create_vector_store(chunks)
    st.success("Document processed successfully! You can now ask questions.")

query = st.text_input("Ask a question about your document:")

if query:
    answer = ask_bot(query)
    st.write("**Answer:**", answer)