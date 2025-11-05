import streamlit as st
import os
from utils.parser import extract_text_from_file
from utils.embedding import embed_and_store, retrieve_similar_chunks
from utils.query import query_llm
from google import genai # Import genai for API key setup

# --- Configuration ---
# Set the API Key from Streamlit Secrets or Environment Variable
# You MUST set GEMINI_API_KEY as an environment variable or in a .streamlit/secrets.toml file
# st.session_state is used to prevent the setup from running on every rerun
if "api_key_set" not in st.session_state:
    try:
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        st.session_state["api_key_set"] = True
    except Exception as e:
        st.error(f"Error configuring Gemini API: {e}. Please ensure the GEMINI_API_KEY environment variable is set.")
        st.stop()
# ---

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

    try:
        # ✅ Extract text and embed
        with st.spinner("Processing document..."):
            text = extract_text_from_file(file_path)
            embed_and_store(text, file_path)
        st.success("Document processed and embedded.")
    except Exception as e:
        st.error(f"Error during document processing/embedding: {e}")


if query and uploaded_file:
    try:
        with st.spinner("Finding answer..."):
            # ✅ Retrieve relevant chunks
            chunks = retrieve_similar_chunks(query, file_path)

            # ✅ Query the LLM
            response = query_llm(query, chunks)

        st.markdown("### 🩺 Answer:")
        st.write(response)
    except Exception as e:
        st.error(f"Error during query: {e}")
