# agents/common_agent.py

from agents.base_agent import BaseAgent
from sentence_transformers import SentenceTransformer
import faiss
import os
import numpy as np
import pickle

class CommonAgent(BaseAgent):
    def __init__(self, config: dict):
        super().__init__(config)
        self.index = None
        self.documents = []
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index_path = "data/faiss_index/common_agent.index"
        self.doc_store_path = "data/faiss_index/documents.pkl"
        self.load_resources()

    def load_resources(self):
        """Load FAISS index and doc store or create them if missing"""
        if os.path.exists(self.index_path) and os.path.exists(self.doc_store_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.doc_store_path, "rb") as f:
                self.documents = pickle.load(f)
            print("✅ CommonAgent: FAISS index and documents loaded.")
        else:
            print("⚠️ FAISS index not found. Run indexing first.")

    def respond(self, session_id: str, user_input: str) -> str:
        """Search FAISS and return top matching result"""
        if not self.index:
            return "CommonAgent is not ready. Index missing."

        query_embedding = self.model.encode([user_input])
        D, I = self.index.search(np.array(query_embedding).astype("float32"), k=1)

        if I[0][0] < 0:
            return "Sorry, I couldn't find relevant info."

        result = self.documents[I[0][0]]
        return f"📄 Most relevant info:\n\n{result}"

