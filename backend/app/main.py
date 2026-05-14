from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from backend.app.workflow.full_agent import run_support_agent

app = FastAPI(title="Lumen AI Support API")

# Enable CORS so the Next.js frontend can talk to the FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailRequest(BaseModel):
    subject: str
    body: str

import json
import time
import logging
from datetime import datetime

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Use absolute path for consistency
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")

def load_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading history: {e}")
    return []

def log_to_history(result):
    try:
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        history = load_history()
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    
    # Add metadata for Human-in-the-Loop
    result["status"] = "pending"
    result["timestamp"] = datetime.now().isoformat()
    history.append(result)
    
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)
    
    # --- Auto-Red-Teaming: Capture malicious inputs for future testing ---
    malicious_categories = ["spam", "security_concern", "prompt_injection_attempt"]
    if result.get("classification", {}).get("category") in malicious_categories:
        try:
            red_team_path = os.path.join(os.path.dirname(__file__), "../../data/red_team.json")
            red_team_data = []
            if os.path.exists(red_team_path):
                with open(red_team_path, "r", encoding="utf-8") as f:
                    red_team_data = json.load(f)
            
            # Avoid duplicate entries
            if not any(entry.get("body") == result.get("body") for entry in red_team_data):
                new_entry = {
                    "id": f"AUTO_{result.get('id', 'unknown')}",
                    "subject": result.get("subject", "N/A"),
                    "body": result.get("body", "N/A"),
                    "expected_action": result.get("action", "escalate_human"),
                    "threat_type": f"Auto-Detected: {result.get('classification', {}).get('category', 'unknown')}"
                }
                red_team_data.append(new_entry)
                with open(red_team_path, "w", encoding="utf-8") as f:
                    json.dump(red_team_data, f, indent=2)
                logger.info(f"🛡️ Auto-Red-Teaming: Malicious input saved to red_team.json")
        except Exception as e:
            logger.error(f"Failed to auto-save to red-team: {e}")

@app.post("/api/process-email")
async def process_email(request: EmailRequest):
    try:
        result = run_support_agent(request.subject, request.body)
        log_to_history(result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats():
    history = load_history()

    if not history:
        return {
            "total_tickets": 0, "avg_latency": "0s", "accuracy": "0%", 
            "automation_rate": "0%", "success_rate": "0%", "avg_confidence": "0%"
        }

    total = len(history)
    # Using 'latency' and 'total' keys to match full_agent.py
    avg_latency = sum(h.get("latency", {}).get("total", 0) for h in history) / total
    
    # Automation logic: anything not escalated is "automated"
    automated = [h for h in history if h.get("action") != "escalate_human"]
    automation_rate = (len(automated) / total) * 100
    
    # Real Success Rate: Define success as interactions with high system confidence (>80%)
    high_confidence_tickets = [h for h in history if h.get("system_confidence", 0) >= 80]
    success_rate = (len(high_confidence_tickets) / total) * 100
    
    # Avg System Confidence (Only for tickets that have the field)
    valid_confidences = [h.get("system_confidence") for h in history if "system_confidence" in h]
    avg_conf = sum(valid_confidences) / len(valid_confidences) if valid_confidences else 0
    
    return {
        "total_tickets": total,
        "avg_latency": f"{avg_latency:.2f}s",
        "automation_rate": f"{int(automation_rate)}%",
        "success_rate": f"{int(success_rate)}%",
        "avg_confidence": f"{int(avg_conf)}%"
    }

@app.get("/api/chart-data")
async def get_chart_data():
    history = load_history()
    counts = {}
    for entry in history:
        cat = entry.get("classification", {}).get("category", "unknown")
        counts[cat] = counts.get(cat, 0) + 1
    
    # --- Cost Analysis Logic ---
    # GPT-4o Est. Cost: $0.01 per ticket (Avg. 1k tokens)
    # Local Llama 3.2 Cost: $0.00
    total_tickets = len(history)
    simulated_gpt_cost = round(total_tickets * 0.01, 2)
    
    data = [{"name": cat.replace("_", " ").title(), "value": count} for cat, count in counts.items()]
    return {
        "distribution": data,
        "metrics": {
            "total_tickets": total_tickets,
            "cost_saved": simulated_gpt_cost,
            "latency_avg": "2.4s"
        }
    }

@app.post("/api/approve-ticket/{ticket_id}")
async def approve_ticket(ticket_id: str):
    history = load_history()
    for h in history:
        if h.get("id") == ticket_id:
            h["status"] = "approved"
            h["finalized_at"] = datetime.now().isoformat()
            break
    
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)
    return {"status": "success"}

@app.post("/api/update-ticket-response")
async def update_ticket_response(data: dict):
    ticket_id = data.get("ticket_id")
    new_response = data.get("response")
    
    history = load_history()
    for h in history:
        if h.get("id") == ticket_id:
            h["response"] = new_response
            h["status"] = "overridden"
            h["finalized_at"] = datetime.now().isoformat()
            break
            
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)
    return {"status": "success"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
