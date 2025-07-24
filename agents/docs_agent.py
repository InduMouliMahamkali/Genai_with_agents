# agents/docs_agent.py

from memory.vector_store import VectorStore
from caching.cache_decorator import cache_response

class DocsAgent:
    def __init__(self, agent_id="docs_agent", config=None):
        self.agent_id = agent_id
        self.config = config or {}
        self.vector_store = VectorStore()
        if not self.vector_store.load_index():
            raise RuntimeError("❌ FAISS index not found. Please run embedder.py first.")


    @cache_response(ttl=600)
    def answer_query(self, query: str) -> str:
        relevant_chunks = self.vector_store.search(query, top_k=3)

        if not relevant_chunks:
            return "📄 I couldn't find anything relevant in the documentation."

        context = "\n---\n".join(relevant_chunks)
        response = self._summarize(query, context)
        return response

    def _summarize(self, query: str, context: str) -> str:
        """
        Basic synthesis response — upgradeable in Phase 4 to LLM-based summarization.
        """
        return f"📄 Based on internal documents, here's what I found:\n\n{context}"
