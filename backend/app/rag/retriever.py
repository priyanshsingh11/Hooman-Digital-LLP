import os
import chromadb
import ollama
from typing import List, Dict

# --- CONFIGURATION ---
CHROMA_PATH = os.path.join(os.path.dirname(__file__), "../../db/chroma_db")
EMBED_MODEL = "nomic-embed-text"
COLLECTION_NAME = "lumen_help_docs"

class SupportRetriever:
    def __init__(self):
        # Initialize Persistent Chroma Client
        self.client = chromadb.PersistentClient(path=CHROMA_PATH)
        self.collection = self.client.get_collection(name=COLLECTION_NAME)

    def get_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for the user query."""
        try:
            response = ollama.embeddings(model=EMBED_MODEL, prompt=query)
            return response["embedding"]
        except Exception as e:
            print(f"Error generating query embedding: {e}")
            return []

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search ChromaDB for relevant context."""
        query_embedding = self.get_query_embedding(query)
        
        if not query_embedding:
            return []

        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=["documents", "metadatas", "distances"]
            )

            formatted_results = []
            # Chroma returns lists of lists; iterate through the first index
            for i in range(len(results["ids"][0])):
                formatted_results.append({
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "score": results["distances"][0][i]
                })
            
            return formatted_results

        except Exception as e:
            print(f"Error during retrieval: {e}")
            return []

def search_knowledge_base(query: str):
    """Clean entry point for retrieval."""
    retriever = SupportRetriever()
    results = retriever.retrieve(query)
    
    if not results:
        print("No relevant documents found.")
        return

    print(f"\n--- Top Results for: '{query}' ---")
    for res in results:
        print(f"\nSource: {res['metadata']['filename']} (Distance: {res['score']:.4f})")
        print(f"Content: {res['text'][:200]}...")
    
    return results

if __name__ == "__main__":
    # Example usage
    sample_query = "What is your refund policy for monthly plans?"
    search_knowledge_base(sample_query)
