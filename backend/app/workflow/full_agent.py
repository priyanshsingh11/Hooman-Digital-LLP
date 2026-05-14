import logging
import os
import sys

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from backend.app.workflow.workflow import AIWorkflowOrchestrator
from backend.app.services.response_generator import generate_support_response

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class SupportAIAgent:
    """
    The main agent that orchestrates the entire AI support pipeline:
    Classify -> Retrieve -> Orchestrate -> Generate Response.
    """
    def __init__(self):
        self.orchestrator = AIWorkflowOrchestrator()

    def handle_customer_email(self, subject: str, body: str) -> dict:
        """
        Processes an incoming email end-to-end and returns the final result.
        """
        logger.info(f"--- AGENT START: Processing '{subject}' ---")
        
        try:
            # 1. Run Core Workflow (Classification + Retrieval + Decision)
            workflow_result = self.orchestrator.process_email(subject, body)
            
            # Extract components from workflow
            classification = workflow_result.get("classification", {})
            retrieved_docs = workflow_result.get("retrieved_docs", [])
            action = workflow_result.get("action", "escalate_human")
            
            # 2. Generate Final Response Step
            logger.info("Agent: Generating final grounded response...")
            generated_response = generate_support_response(
                subject=subject,
                body=body,
                classification=classification,
                retrieved_docs=retrieved_docs,
                action=action
            )
            
            # 3. Compile Final Result
            return {
                "classification": classification,
                "retrieved_docs": retrieved_docs,
                "action": action,
                "generated_response": generated_response,
                "workflow_summary": workflow_result.get("workflow_summary")
            }

        except Exception as e:
            logger.error(f"Agent failed to process email: {e}")
            return {
                "error": str(e),
                "action": "escalate_human",
                "generated_response": "I'm sorry, I encountered an internal error. I've escalated your ticket to our human support team.",
                "workflow_summary": "Internal Agent Error."
            }

def run_support_agent(subject: str, body: str) -> dict:
    """Entry point for the full AI Support Agent."""
    agent = SupportAIAgent()
    return agent.handle_customer_email(subject, body)
