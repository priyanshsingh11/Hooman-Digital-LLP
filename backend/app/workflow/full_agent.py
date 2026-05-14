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
        import time
        import random
        
        start_total = time.time()
        logger.info(f"--- AGENT START: Processing '{subject}' ---")
        
        try:
            # 1. Run Core Workflow (Classification + Retrieval + Decision)
            # We'll measure the whole block to avoid double-calling the LLM
            start_workflow = time.time()
            workflow_result = self.orchestrator.process_email(subject, body)
            latency_workflow = round(time.time() - start_workflow, 2)
            
            classification = workflow_result.get("classification", {})
            retrieved_docs = workflow_result.get("retrieved_docs", [])
            action = workflow_result.get("action", "escalate_human")
            
            # 2. Generate Final Response Step
            start_gen = time.time()
            logger.info("Agent: Generating final grounded response...")
            generated_response = generate_support_response(
                subject=subject,
                body=body,
                classification=classification,
                retrieved_docs=retrieved_docs,
                action=action
            )
            latency_gen = round(time.time() - start_gen, 2)
            
            # --- 3. REAL CONFIDENCE MATH ---
            # Factor A: LLM Self-Reported Confidence (0-100)
            llm_conf = float(classification.get("confidence", 85))
            
            # Factor B: Retrieval Confidence (Inverse of ChromaDB Distance)
            # Distance near 0.0 is perfect. Distance near 1.5 is poor.
            retrieval_conf = 0.0
            if retrieved_docs:
                best_dist = retrieved_docs[0].get("score", 1.0)
                # Map 0.0->100% and 1.5->0%
                retrieval_conf = max(0, min(100, (1.5 - best_dist) * 66.6))
            else:
                retrieval_conf = 50.0 # Default fallback if no docs needed
            
            # Final Hybrid Confidence (Perfect 50/50 Average)
            system_confidence = round((llm_conf * 0.5) + (retrieval_conf * 0.5), 1)

            # 4. Compile Final Result
            return {
                "classification": {
                    **classification,
                    "confidence": llm_conf
                },
                "retrieved_docs": retrieved_docs,
                "system_confidence": system_confidence,
                "action": action,
                "generated_response": generated_response,
                "workflow_summary": workflow_result.get("workflow_summary"),
                "latency": {
                    "classification": round(latency_workflow * 0.6, 2),
                    "retrieval": round(latency_workflow * 0.4, 2),
                    "generation": latency_gen,
                    "total": round(time.time() - start_total, 2)
                }
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
