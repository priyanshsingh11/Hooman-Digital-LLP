import os
import sys
import logging

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from backend.app.workflow.workflow import run_orchestrator
from backend.app.evals.metrics_utils import (
    load_eval_dataset, calculate_accuracy, print_metrics_summary, print_failure_cases
)

# --- Configuration ---
DATASET_PATH = os.path.join(os.path.dirname(__file__), "../../../data/emails.json")

def run_workflow_evaluation():
    """Evaluates the end-to-end decision logic of the AI workflow."""
    dataset = load_eval_dataset(DATASET_PATH)
    if not dataset:
        return

    actual_actions = []
    predicted_actions = []
    failures = []

    print(f"Starting workflow evaluation on {len(dataset)} samples...")

    for entry in dataset:
        subject = entry.get("subject", "")
        body = entry.get("body", "")
        expected_action = entry.get("expected_action")

        if not expected_action:
            continue

        try:
            result = run_orchestrator(subject, body)
            pred_action = result.get("action")

            actual_actions.append(expected_action)
            predicted_actions.append(pred_action)

            if str(expected_action).lower() != str(pred_action).lower():
                failures.append({
                    "id": entry.get("id"),
                    "query": f"{subject}",
                    "expected": expected_action,
                    "got": pred_action
                })

        except Exception as e:
            logging.error(f"Error evaluating workflow for ID {entry.get('id')}: {e}")

    # Calculate Metrics
    accuracy = calculate_accuracy(actual_actions, predicted_actions)

    # Print Report
    print_metrics_summary("Workflow Decisions", {
        "Total Samples": len(actual_actions),
        "Decision Accuracy": accuracy,
        "Decision Failures": len(failures)
    })

    print_failure_cases(failures, "Workflow Failures")

if __name__ == "__main__":
    run_workflow_evaluation()
