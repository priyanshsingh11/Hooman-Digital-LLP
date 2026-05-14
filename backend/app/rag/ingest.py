import os
import chromadb
import ollama
from typing import List, Dict
import uuid

# --- CONFIGURATION ---
CHROMA_PATH = os.path.join(os.path.dirname(__file__), "../../db/chroma_db")
DOCS_PATH = os.path.join(os.path.dirname(__file__), "../../../data/help_docs")
EMBED_MODEL = "nomic-embed-text"
COLLECTION_NAME = "lumen_help_docs"

class IngestionPipeline:
    def __init__(self):
        # Initialize Persistent Chroma Client
        self.client = chromadb.PersistentClient(path=CHROMA_PATH)
        self.collection = self.client.get_or_create_collection(name=COLLECTION_NAME)

    def get_embedding(self, text: str) -> List[float]:
        """Generate embeddings using Ollama."""
        try:
            response = ollama.embeddings(model=EMBED_MODEL, prompt=text)
            return response["embedding"]
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []

    def load_documents(self) -> List[Dict]:
        """Read all .txt files from the help_docs folder."""
        documents = []
        if not os.path.exists(DOCS_PATH):
            print(f"Error: Path {DOCS_PATH} does not exist.")
            return documents

        for filename in os.listdir(DOCS_PATH):
            if filename.endswith(".txt"):
                file_path = os.path.join(DOCS_PATH, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        documents.append({
                            "id": str(uuid.uuid4()),
                            "text": content,
                            "metadata": {"filename": filename}
                        })
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
        return documents

    def run(self):
        """Execute the ingestion process."""
        print(f"--- Starting Ingestion into {COLLECTION_NAME} ---")
        
        docs = self.load_documents()
        if not docs:
            print("No documents found to ingest.")
            return

        for doc in docs:
            print(f"Processing: {doc['metadata']['filename']}...")
            embedding = self.get_embedding(doc["text"])
            
            if embedding:
                self.collection.add(
                    ids=[doc["id"]],
                    embeddings=[embedding],
                    documents=[doc["text"]],
                    metadatas=[doc["metadata"]]
                )
                print(f"Successfully ingested: {doc['metadata']['filename']}")
            else:
                print(f"Skipping {doc['metadata']['filename']} due to embedding failure.")

        print(f"--- Ingestion Complete. Total docs: {self.collection.count()} ---")

if __name__ == "__main__":
    pipeline = IngestionPipeline()
    pipeline.run()
