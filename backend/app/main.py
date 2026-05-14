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
from datetime import datetime

# Use absolute path for consistency
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")

def load_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading history: {e}")
    return []

def log_to_history(result):
    try:
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    
    history.append({
        "timestamp": datetime.now().isoformat(),
        **result
    })
    
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

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
    if not history:
        return []
    
    # Count occurrences of each category
    counts = {}
    for h in history:
        cat = h.get("classification", {}).get("category", "Unknown")
        counts[cat] = counts.get(cat, 0) + 1
    
    # Format for Recharts Bar Chart
    return [{"name": k.replace("_", " ").title(), "value": v} for k, v in counts.items()]

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
