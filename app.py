import streamlit as st
import os
from utils.parser import extract_text_from_file
from utils.embedding import embed_and_store, load_vector_store, retrieve_similar_chunks
from utils.query import query_llm

st.title("🧠 Medical Document Q&A (RAG)")

uploaded_file = st.file_uploader("Upload a medical document", type=["pdf", "docx", "txt"])
query = st.text_input("Ask a question about the uploaded content:")

if uploaded_file:
    # ✅ Ensure the directory exists
    os.makedirs("uploaded_docs", exist_ok=True)

    # ✅ Save the uploaded file
    file_path = os.path.join("uploaded_docs", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"File '{uploaded_file.name}' uploaded successfully.")

    # ✅ Extract text and embed
    text = extract_text_from_file(file_path)
    embed_and_store(text, file_path)

if query and uploaded_file:
    # ✅ Retrieve relevant chunks
    chunks = retrieve_similar_chunks(query, file_path)

    # ✅ Query the LLM
    response = query_llm(query, chunks)

    st.markdown("### 🩺 Answer:")
    st.write(response)
