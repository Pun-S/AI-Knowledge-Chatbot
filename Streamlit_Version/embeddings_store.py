import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def create_vector_store(chunks, store_path="vector_store"):
    embeddings = np.array(model.encode(chunks))
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, f"{store_path}.idx")
    with open(f"{store_path}_chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

def search(query, k=3, store_path="vector_store"):
    query_vec = np.array([model.encode(query)])
    index = faiss.read_index(f"{store_path}.idx")
    with open(f"{store_path}_chunks.pkl", "rb") as f:
        chunks = pickle.load(f)
    D, I = index.search(query_vec, k)
    return [chunks[i] for i in I[0]]
