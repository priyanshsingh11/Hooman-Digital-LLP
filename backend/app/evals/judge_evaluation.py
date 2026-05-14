import os
import sys
import json
import logging
import ollama
from tqdm import tqdm

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from backend.app.workflow.full_agent import run_support_agent

# --- Configuration ---
DATASET_PATH = os.path.join(os.path.dirname(__file__), "../../../data/emails.json")
JUDGE_PROMPT_PATH = os.path.join(os.path.dirname(__file__), "../prompts/judge.txt")
JUDGE_MODEL = "llama3.2"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_prompt():
    with open(JUDGE_PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()

def run_qualitative_eval():
    """Runs LLM-as-a-Judge evaluation on the dataset."""
    if not os.path.exists(DATASET_PATH):
        print(f"Error: Dataset not found at {DATASET_PATH}")
        return

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    judge_prompt_template = load_prompt()
    results = []
    
    print(f"🚀 Starting Qualitative Evaluation (Judge: {JUDGE_MODEL})...")
    
    # We'll evaluate a subset (e.g., first 5) to save time, or all if short
    test_subset = dataset[:5] 

    for entry in tqdm(test_subset, desc="Judging Responses"):
        subject = entry.get("subject", "")
        body = entry.get("body", "")
        
        # 1. Run the actual agent
        agent_output = run_support_agent(subject, body)
        ai_response = agent_output.get("generated_response", "")
        
        # Prepare context for judge
        docs = agent_output.get("retrieved_docs", [])
        context_str = "\n".join([d.get("content", "") for d in docs]) or "No docs found."

        # 2. Ask the Judge to score it
        prompt = judge_prompt_template.replace("{email_body}", body) \
                                      .replace("{context}", context_str) \
                                      .replace("{ai_response}", ai_response)

        try:
            response = ollama.chat(
                model=JUDGE_MODEL,
                messages=[{"role": "user", "content": prompt}],
                format="json",
                options={"temperature": 0}
            )
            judge_result = json.loads(response['message']['content'])
            results.append(judge_result)
        except Exception as e:
            logger.error(f"Judging failed for entry: {e}")

    # 3. Aggregate Scores
    if not results:
        print("No results to report.")
        return

    metrics = ["tone", "accuracy", "empathy", "clarity", "resolution"]
    averages = {m: sum(r['scores'].get(m, 0) for r in results) / len(results) for m in metrics}

    print("\n" + "="*40)
    print("      QUALITATIVE EVALUATION REPORT")
    print("="*40)
    for m, score in averages.items():
        bar = "█" * int(score * 4)
        print(f"{m.capitalize():12} | {score:.2f}/5.0 {bar}")
    print("="*40)
    print(f"Justification Summary: {results[0].get('justification', 'N/A')[:100]}...")
    print("="*40 + "\n")

if __name__ == "__main__":
    run_qualitative_eval()
