import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.IndexFlatL2(384)

def embed_and_add_to_index(text_chunks: list[str]) -> None:
    embeddings = model.encode(text_chunks)
    index.add(np.array(embeddings).astype("float32"))

def search_query(query: str, chunks: list[str]):
    query_vec = model.encode([query])
    D, I = index.search(np.array(query_vec).astype("float32"), k=3)
    return [chunks[i] for i in I[0]]
