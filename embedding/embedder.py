# embedding/embedder.py

import os
from memory.vector_store import VectorStore

def load_documents(folder_path: str):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
                text = f.read()
                documents.extend(split_into_chunks(text))
    return documents

def split_into_chunks(text: str, max_length: int = 500) -> list:
    """
    Naive splitter by sentences. (Can be upgraded to LangChain splitters)
    """
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks, chunk = [], ""
    for sentence in sentences:
        if len(chunk) + len(sentence) <= max_length:
            chunk += " " + sentence
        else:
            chunks.append(chunk.strip())
            chunk = sentence
    if chunk:
        chunks.append(chunk.strip())
    return chunks

def main():
    folder = "data/company_docs/"
    documents = load_documents(folder)
    
    if not documents:
        print("❌ No documents found in data/company_docs/")
        return
    
    vector_store = VectorStore()
    vector_store.build_index(documents)
    print(f"✅ Indexed {len(documents)} document chunks to FAISS.")

if __name__ == "__main__":
    main()
