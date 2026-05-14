import logging
import os
import sys

# Add project root to path to allow imports from other services
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from backend.app.services.classifier import classify_support_email
from backend.app.rag.retriever import search_support_docs

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class AIWorkflowOrchestrator:
    """
    Orchestrates the support automation pipeline: Classification -> Retrieval -> Decision.
    """
    
    def determine_action(self, classification: dict, body: str = "") -> str:
        """
        Implements deterministic business logic to decide the next workflow step.
        """
        category = classification.get("category", "").strip().lower()
        urgency = classification.get("urgency", "low").strip().lower()
        sentiment = classification.get("sentiment", "neutral").strip().lower()
        body_lower = body.lower()

        # --- Priority 1: Immediate Human Escalation (Safety, Legal, Extreme Frustration, Urgent) ---
        # Heuristic 1: Immediate Human Escalation for high-risk/high-frustration content
        body_lower = body.lower()
        # Removed "waiting", "urgent", "priority" as they are too common in normal emails
        critical_keywords = ["lawsuit", "sue you", "legal action", "attorney", "better business bureau"]
        extreme_frustration = ["terrible service", "ridiculous", "unacceptable", "disgusting"]
        
        if any(word in body_lower for word in critical_keywords):
            return "escalate_human"
            
        if any(word in body_lower for word in extreme_frustration) and sentiment == "frustrated":
            return "escalate_human"

        if urgency == "high" and sentiment == "frustrated":
            return "escalate_human"

        if any(word in body_lower for word in critical_keywords):
            return "escalate_human"

        if category in ["security_concern", "prompt_injection_attempt"]:
            return "escalate_human"

        # --- Priority 2: Specific Routing (Better for Accuracy) ---
        if any(word in body_lower for word in ["invoice", "receipt", "bill for last month"]):
            return "auto_reply"

        if category in ["billing", "refund_request"]:
            return "route_billing"

        if category in ["subscription_cancellation", "feature_request"]:
            return "auto_reply"
            
        if category == "technical_issue":
            return "route_technical"
            
        if category == "account_access":
            if urgency == "high":
                return "escalate_human"
            return "route_technical"

        # --- Priority 4: Automation & Auto-Replies ---
        if category == "spam":
            return "close_spam"

        if category in ["subscription_cancellation", "feature_request"]:
            # We want to handle these with a polite auto-reply (maybe with a retention offer)
            return "auto_reply"

        # --- Fallback ---
        if category == "multilingual_or_non_english":
            return "route_technical" # Route to support for translation/handling

        return "request_clarification"

    def process_email(self, subject: str, body: str) -> dict:
        """
        Runs the full workflow for a single incoming email.
        """
        logger.info(f"--- Starting Workflow for: {subject} ---")
        
        try:
            # 1. Classification Step
            classification = classify_support_email(subject, body)
            logger.info(f"Classification Complete: {classification.get('category', 'unknown')} ({classification.get('urgency', 'medium')})")
            
            # 2. Retrieval Step (Context Discovery)
            # We search based on both subject and body for better context
            search_query = f"{subject} {body[:200]}"
            retrieved_docs = search_support_docs(search_query, top_k=2)
            logger.info(f"Retrieval Complete: Found {len(retrieved_docs)} relevant snippets.")
            
            # 3. Decision Logic Step
            action = self.determine_action(classification, body)
            logger.info(f"Workflow Action Determined: {action}")
            
            # 4. Generate Workflow Summary
            summary = f"Email classified as {classification.get('category', 'unknown')} with {classification.get('urgency', 'medium')} urgency. " \
                      f"System selected action: {action}."
            
            # Assemble Final Response
            return {
                "classification": classification,
                "retrieved_docs": [
                    {"source": doc["filename"], "content": doc["text"]} for doc in retrieved_docs
                ],
                "action": action,
                "workflow_summary": summary
            }

        except Exception as e:
            logger.error(f"Workflow Error: {e}")
            return {
                "error": str(e),
                "action": "escalate_human",
                "workflow_summary": "System error during orchestration. Escalating to human."
            }

def run_orchestrator(subject: str, body: str) -> dict:
    """Entry point for the workflow engine."""
    orchestrator = AIWorkflowOrchestrator()
    return orchestrator.process_email(subject, body)
