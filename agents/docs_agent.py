# agents/docs_agent.py

from memory.vector_store import VectorStore

class DocsAgent:
    def __init__(self):
        self.vector_store = VectorStore()
        if not self.vector_store.load_index():
            raise RuntimeError("❌ FAISS index not found. Please run embedder.py first.")

    def answer_query(self, query: str) -> str:
        relevant_chunks = self.vector_store.search(query, top_k=3)

        if not relevant_chunks:
            return "I couldn't find anything relevant in the documentation."

        context = "\n---\n".join(relevant_chunks)
        response = self._summarize(query, context)
        return response

    def _summarize(self, query: str, context: str) -> str:
        """
        Simple response synthesis using heuristics or a basic prompt.
        You can replace this with OpenAI or another model in Phase 4.
        """
        return f"Based on internal documents, here's what I found:\n\n{context}"
