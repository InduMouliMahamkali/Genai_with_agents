# memory/vector_store.py

import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

DOC_DIR = "data/company_docs"
INDEX_PATH = "data/faiss_index/common_agent.index"
DOC_STORE_PATH = "data/faiss_index/documents.pkl"

def load_documents():
    documents = []
    for filename in os.listdir(DOC_DIR):
        if filename.endswith(".txt"):
            with open(os.path.join(DOC_DIR, filename), "r", encoding="utf-8") as f:
                content = f.read()
                chunks = content.split("\n\n")  # Naive paragraph chunking
                documents.extend([chunk.strip() for chunk in chunks if chunk.strip()])
    return documents

def embed_and_index_documents():
    print("📚 Loading and embedding documents...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    documents = load_documents()
    embeddings = model.encode(documents, convert_to_numpy=True).astype("float32")

    print(f"🔢 Total Chunks: {len(documents)}")
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    print("💾 Saving FAISS index and documents...")
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    faiss.write_index(index, INDEX_PATH)

    with open(DOC_STORE_PATH, "wb") as f:
        pickle.dump(documents, f)

    print("✅ Indexing Complete!")

if __name__ == "__main__":
    embed_and_index_documents()
