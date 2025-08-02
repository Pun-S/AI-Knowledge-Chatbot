import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import os

model = SentenceTransformer('all-MiniLM-L6-v2')

def create_or_append_vector_store(chunks, store_path="vector_store"):
    embeddings = np.array(model.encode(chunks))

    if os.path.exists(f"{store_path}.idx") and os.path.exists(f"{store_path}_chunks.pkl"):
        index = faiss.read_index(f"{store_path}.idx")
        with open(f"{store_path}_chunks.pkl", "rb") as f:
            existing_chunks = pickle.load(f)

        index.add(embeddings)
        all_chunks = existing_chunks + chunks
    else:
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        all_chunks = chunks

    faiss.write_index(index, f"{store_path}.idx")
    with open(f"{store_path}_chunks.pkl", "wb") as f:
        pickle.dump(all_chunks, f)

def search(query, k=3, store_path="vector_store"):
    if not os.path.exists(f"{store_path}.idx"):
        return []
    query_vec = np.array([model.encode(query)])
    index = faiss.read_index(f"{store_path}.idx")
    with open(f"{store_path}_chunks.pkl", "rb") as f:
        chunks = pickle.load(f)
    D, I = index.search(query_vec, k)
    return [chunks[i] for i in I[0]]