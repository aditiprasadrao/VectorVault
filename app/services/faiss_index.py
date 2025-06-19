import faiss
import numpy as np

def save_to_faiss(vectors, path):
    index = faiss.IndexFlatL2(len(vectors[0]))
    index.add(np.array(vectors).astype('float32'))
    faiss.write_index(index, path)

def search_faiss(vector, path, k=5):
    index = faiss.read_index(path)
    D, I = index.search(np.array([vector]).astype('float32'), k)
    return I[0].tolist()
