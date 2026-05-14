import sys
import os

# Add the project root to path so we can import from app.rag
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from backend.app.rag.retriever import search_support_docs

def run_retrieval_tests():
    """
    Executes a series of test queries to validate the semantic search system.
    """
    test_queries = [
        "My refund hasn't arrived",
        "I can't reset my password",
        "Why am I getting 429 errors?"
    ]

    print("=" * 60)
    print("AI SUPPORT RETRIEVAL SYSTEM - SEMANTIC TEST SUITE")
    print("=" * 60)

    for query in test_queries:
        print(f"\n[QUERY]: '{query}'")
        print("-" * 30)
        
        results = search_support_docs(query, top_k=2)
        
        if not results:
            print("No relevant documents found for this query.")
            continue

        for i, res in enumerate(results):
            print(f"RESULT #{i+1}")
            print(f"FILE: {res['filename']}")
            print(f"SCORE: {res['score']} (Lower is more similar)")
            
            # Print a clean snippet of the content
            content = res['text'].strip()
            snippet = (content[:300] + '...') if len(content) > 300 else content
            print(f"CONTENT: {snippet}")
            print("-" * 20)
        
        print("\n" + "*" * 40)

if __name__ == "__main__":
    try:
        run_retrieval_tests()
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
    except KeyboardInterrupt:
        print("\nTest suite stopped by user.")
