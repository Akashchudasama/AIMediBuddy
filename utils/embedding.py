import os
import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer

# Load the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Ensure vector store directory exists
if not os.path.exists("vector_store"):
    os.makedirs("vector_store")


def split_text_into_blocks(text, block_size=5):
    """
    Splits text into blocks of N lines each for better semantic meaning.
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    blocks = ['\n'.join(lines[i:i + block_size]) for i in range(0, len(lines), block_size)]
    return blocks


def embed_and_store(text, doc_path):
    """
    Create and store FAISS index and text chunks from document.
    """
    chunks = split_text_into_blocks(text)
    embeddings = model.encode(chunks)
    embeddings = np.array(embeddings).astype('float32')

    base_name = os.path.basename(doc_path).split('.')[0]
    faiss.write_index(faiss.IndexFlatL2(embeddings.shape[1]), f"vector_store/{base_name}.index")
    index = faiss.read_index(f"vector_store/{base_name}.index")
    index.add(embeddings)

    # Save FAISS index and corresponding text chunks
    faiss.write_index(index, f"vector_store/{base_name}.index")
    with open(f"vector_store/{base_name}_chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)


def load_vector_store(doc_path):
    """
    Load FAISS index and chunks for given document.
    """
    base_name = os.path.basename(doc_path).split('.')[0]
    index = faiss.read_index(f"vector_store/{base_name}.index")
    with open(f"vector_store/{base_name}_chunks.pkl", "rb") as f:
        chunks = pickle.load(f)
    return index, chunks


def retrieve_similar_chunks(query, doc_path, k=5):
    """
    Search FAISS index for top-k similar chunks to the query.
    """
    index, chunks = load_vector_store(doc_path)
    query_embedding = model.encode([query]).astype('float32')
    D, I = index.search(query_embedding, k)
    return [chunks[i] for i in I[0] if i < len(chunks)]
