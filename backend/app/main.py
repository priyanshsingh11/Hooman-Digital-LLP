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

@app.post("/api/process-email")
async def process_email(request: EmailRequest):
    try:
        result = run_support_agent(request.subject, request.body)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
