import json
import logging
from typing import List, Dict, Any

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def calculate_accuracy(y_true: List[Any], y_pred: List[Any]) -> float:
    """Calculates basic accuracy score."""
    if not y_true:
        return 0.0
    correct = sum(1 for t, p in zip(y_true, y_pred) if str(t).lower() == str(p).lower())
    return (correct / len(y_true)) * 100

def print_metrics_summary(title: str, metrics: Dict[str, Any]):
    """Pretty-prints a metrics dictionary."""
    print("\n" + "=" * 50)
    print(f" {title.upper()} REPORT ")
    print("=" * 50)
    for key, value in metrics.items():
        if isinstance(value, float):
            print(f"{key:<25}: {value:>8.2f}%")
        else:
            print(f"{key:<25}: {value:>10}")
    print("=" * 50)

def print_failure_cases(failures: List[Dict[str, Any]], title: str = "Failure Cases"):
    """Prints a list of failed evaluation samples."""
    if not failures:
        print(f"\n--- No failures for {title}! ---")
        return

    print(f"\n--- Top {len(failures)} {title} ---")
    for idx, fail in enumerate(failures[:10]):  # Cap at 10 for readability
        print(f"[{idx+1}] ID: {fail.get('id')} | Category: {fail.get('category', 'N/A')}")
        print(f"    Query:    {fail.get('query', '')[:80]}...")
        print(f"    Expected: {fail.get('expected')}")
        print(f"    Got:      {fail.get('got')}")
        print("-" * 30)

def load_eval_dataset(file_path: str) -> List[Dict]:
    """Loads the evaluation JSON dataset."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load dataset from {file_path}: {e}")
        return []
