import os
import logging
import chromadb
import ollama
from typing import List, Dict

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# --- Configuration ---
CHROMA_PATH = os.path.join(os.path.dirname(__file__), "../../db/chroma_db")
EMBED_MODEL = "nomic-embed-text"
COLLECTION_NAME = "lumen_help_docs"

class SupportRetriever:
    """
    A semantic search retriever that connects to ChromaDB and uses Ollama
    for generating query embeddings.
    """
    def __init__(self, collection_name: str = COLLECTION_NAME):
        self.collection_name = collection_name
        try:
            # Initialize Persistent Chroma Client
            self.client = chromadb.PersistentClient(path=CHROMA_PATH)
            self.collection = self.client.get_collection(name=self.collection_name)
            logger.info(f"Connected to ChromaDB at {CHROMA_PATH}. Collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise

    def get_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for the user query using Ollama."""
        try:
            logger.debug(f"Generating embedding for query: {query[:50]}...")
            response = ollama.embeddings(model=EMBED_MODEL, prompt=query)
            return response["embedding"]
        except Exception as e:
            logger.error(f"Error generating query embedding with Ollama: {e}")
            return []

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Search ChromaDB for relevant documents using semantic similarity.
        
        Returns:
            List[Dict]: Contains 'text', 'metadata', 'filename', and 'score'.
        """
        if not query.strip():
            logger.warning("Empty query received.")
            return []

        query_embedding = self.get_query_embedding(query)
        
        if not query_embedding:
            logger.error("Could not retrieve documents because embedding generation failed.")
            return []

        try:
            logger.info(f"Retrieving top {top_k} results for: '{query}'")
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=["documents", "metadatas", "distances"]
            )

            formatted_results = []
            
            # Extract and format results
            # ChromaDB returns lists of lists for multiple queries; we take the first index [0]
            if results["ids"] and len(results["ids"][0]) > 0:
                for i in range(len(results["ids"][0])):
                    doc_text = results["documents"][0][i]
                    metadata = results["metadatas"][0][i]
                    score = results["distances"][0][i]
                    
                    formatted_results.append({
                        "text": doc_text,
                        "metadata": metadata,
                        "filename": metadata.get("filename", "Unknown Source"),
                        "score": round(score, 4)
                    })
            
            logger.info(f"Successfully retrieved {len(formatted_results)} documents.")
            return formatted_results

        except Exception as e:
            logger.error(f"Error during retrieval process: {e}")
            return []

def search_support_docs(query: str, top_k: int = 3) -> List[Dict]:
    """
    Clean functional entry point for the retrieval pipeline.
    """
    try:
        retriever = SupportRetriever()
        return retriever.retrieve(query, top_k=top_k)
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return []

if __name__ == "__main__":
    # Internal module testing
    sample_query = "What is the refund policy?"
    results = search_support_docs(sample_query)
    
    for idx, res in enumerate(results):
        print(f"\n[{idx+1}] Source: {res['filename']} (Similarity Score: {res['score']})")
        print(f"Snippet: {res['text'][:200]}...")
