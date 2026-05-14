import os
import sys
import logging

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from backend.app.services.classifier import classify_support_email
from backend.app.evals.metrics_utils import (
    load_eval_dataset, calculate_accuracy, print_metrics_summary, print_failure_cases
)

# --- Configuration ---
DATASET_PATH = os.path.join(os.path.dirname(__file__), "../../../data/emails.json")

def run_classifier_evaluation():
    """Runs end-to-end evaluation of the email classification pipeline."""
    dataset = load_eval_dataset(DATASET_PATH)
    if not dataset:
        return

    actual_categories = []
    predicted_categories = []
    actual_urgencies = []
    predicted_urgencies = []
    
    cat_failures = []
    urg_failures = []

    print(f"Starting classification evaluation on {len(dataset)} samples...")

    for entry in dataset:
        subject = entry.get("subject", "")
        body = entry.get("body", "")
        expected_cat = entry.get("expected_category")
        expected_urg = entry.get("expected_urgency")

        # Skip if ground truth is missing
        if not expected_cat or not expected_urg:
            continue

        try:
            result = classify_support_email(subject, body)
            pred_cat = result.get("category")
            pred_urg = result.get("urgency")

            actual_categories.append(expected_cat)
            predicted_categories.append(pred_cat)
            actual_urgencies.append(expected_urg)
            predicted_urgencies.append(pred_urg)

            # Log category failures
            if str(expected_cat).lower() != str(pred_cat).lower():
                cat_failures.append({
                    "id": entry.get("id"),
                    "query": f"{subject}",
                    "expected": expected_cat,
                    "got": pred_cat
                })

            # Log urgency failures
            if str(expected_urg).lower() != str(pred_urg).lower():
                urg_failures.append({
                    "id": entry.get("id"),
                    "query": f"{subject}",
                    "expected": expected_urg,
                    "got": pred_urg
                })

        except Exception as e:
            logging.error(f"Error evaluating entry {entry.get('id')}: {e}")

    # Calculate Metrics
    cat_acc = calculate_accuracy(actual_categories, predicted_categories)
    urg_acc = calculate_accuracy(actual_urgencies, predicted_urgencies)

    # Print Report
    print_metrics_summary("Classification Metrics", {
        "Total Samples": len(actual_categories),
        "Category Accuracy": cat_acc,
        "Urgency Accuracy": urg_acc,
        "Category Failures": len(cat_failures),
        "Urgency Failures": len(urg_failures)
    })

    print_failure_cases(cat_failures, "Category Failures")
    print_failure_cases(urg_failures, "Urgency Failures")

if __name__ == "__main__":
    run_classifier_evaluation()
