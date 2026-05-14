import os
import sys
import logging

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from backend.app.rag.retriever import search_support_docs
from backend.app.evals.metrics_utils import (
    load_eval_dataset, print_metrics_summary, print_failure_cases
)

# --- Configuration ---
DATASET_PATH = os.path.join(os.path.dirname(__file__), "../../../data/emails.json")

# Ground truth mapping: which files should ideally be retrieved for each category
EXPECTED_DOCS_MAPPING = {
    "billing": ["billing_faq.txt", "refund_policy.txt"],
    "refund_request": ["refund_policy.txt", "billing_faq.txt"],
    "technical_issue": ["api_rate_limits.txt", "enterprise_support.txt"],
    "account_access": ["password_reset.txt", "workspace_permissions.txt"],
    "security_concern": ["security_policy.txt", "password_reset.txt"],
    "feature_request": ["enterprise_support.txt"],
    "subscription_cancel": ["subscription_cancel.txt", "billing_faq.txt"],
    "spam": [] 
}

def run_retrieval_evaluation(top_k: int = 2):
    """Evaluates the semantic retrieval engine against expected document mappings."""
    dataset = load_eval_dataset(DATASET_PATH)
    if not dataset:
        return

    hits = 0
    total_relevant_queries = 0
    failures = []

    print(f"Starting retrieval evaluation on {len(dataset)} samples...")

    for entry in dataset:
        category = entry.get("expected_category")
        if not category or category == "spam":
            continue  # Skip spam or missing categories

        total_relevant_queries += 1
        subject = entry.get("subject", "")
        body = entry.get("body", "")
        query = f"{subject} {body[:100]}"

        expected_files = EXPECTED_DOCS_MAPPING.get(category, [])
        
        try:
            results = search_support_docs(query, top_k=top_k)
            retrieved_files = [res["filename"] for res in results]

            # Check if any of the expected files are in the retrieved results
            is_hit = any(expected in retrieved_files for expected in expected_files)
            
            if is_hit:
                hits += 1
            else:
                failures.append({
                    "id": entry.get("id"),
                    "query": query,
                    "category": category,
                    "expected": f"Any of {expected_files}",
                    "got": f"{retrieved_files}"
                })

        except Exception as e:
            logging.error(f"Error evaluating retrieval for ID {entry.get('id')}: {e}")

    # Calculate Metrics
    hit_rate = (hits / total_relevant_queries * 100) if total_relevant_queries > 0 else 0

    # Print Report
    print_metrics_summary("Retrieval Metrics", {
        "Total Evaluated": total_relevant_queries,
        "Hits": hits,
        "Hit Rate (Top-K)": hit_rate,
        "Total Failures": len(failures)
    })

    print_failure_cases(failures, "Retrieval Failures")

if __name__ == "__main__":
    run_retrieval_evaluation()
