# memory/vector_store.py

import os
import faiss
import pickle
from typing import List
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, index_path='data/faiss_index/index.faiss', meta_path='data/faiss_index/docs.pkl'):
        self.index_path = index_path
        self.meta_path = meta_path
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.metadata = []

    def embed_text(self, texts: List[str]):
        return self.embedding_model.encode(texts, show_progress_bar=False)

    def build_index(self, docs: List[str]):
        vectors = self.embed_text(docs)
        self.index = faiss.IndexFlatL2(vectors.shape[1])
        self.index.add(vectors)
        self.metadata = docs
        self.save_index()

    def save_index(self):
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, 'wb') as f:
            pickle.dump(self.metadata, f)

    def load_index(self):
        if os.path.exists(self.index_path) and os.path.exists(self.meta_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.meta_path, 'rb') as f:
                self.metadata = pickle.load(f)
            return True
        return False

    def search(self, query: str, top_k: int = 3) -> List[str]:
        if not self.index:
            self.load_index()
        query_vec = self.embed_text([query])
        _, indices = self.index.search(query_vec, top_k)
        return [self.metadata[i] for i in indices[0] if i < len(self.metadata)]
