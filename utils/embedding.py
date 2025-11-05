from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
import hashlib # For creating a unique hash based on file path

# Initialize the embedding model
# The embedding model is different from the chat model
embeddings = GoogleGenerativeAIEmbeddings(model="text-embedding-004") 

def get_faiss_store_path(file_path):
    """Creates a unique and deterministic path for the FAISS store."""
    # Use a hash of the file path to ensure a unique store per document
    file_hash = hashlib.md5(file_path.encode()).hexdigest()
    return f"faiss_index_{file_hash}"

def embed_and_store(text, file_path):
    """Splits text, generates embeddings, and saves them to a FAISS vector store."""
    
    # 1. Split the text into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    
    # 2. Generate embeddings and create the FAISS store
    vector_store = FAISS.from_texts(chunks, embeddings)
    
    # 3. Save the vector store locally (using a unique path)
    store_path = get_faiss_store_path(file_path)
    vector_store.save_local(store_path)

def load_vector_store(file_path):
    """Loads a FAISS vector store from disk."""
    store_path = get_faiss_store_path(file_path)
    if os.path.exists(store_path):
        return FAISS.load_local(store_path, embeddings, allow_dangerous_deserialization=True)
    return None

def retrieve_similar_chunks(query, file_path, k=4):
    """Loads the vector store and retrieves the top-k most relevant text chunks."""
    vector_store = load_vector_store(file_path)
    if vector_store is not None:
        # Uses similarity search to find relevant documents (chunks)
        docs = vector_store.similarity_search(query, k=k)
        # Return the content of the document objects
        return [doc.page_content for doc in docs]
    return []
