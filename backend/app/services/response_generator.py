import logging
import ollama
from typing import List, Dict, Optional

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

import os

# --- Configuration ---
MODEL_NAME = "llama3.2"
PROMPT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts", "generator.txt")

class ResponseGenerator:
    """
    Generates grounded AI responses using retrieved context and Ollama.
    """
    def __init__(self, model: str = MODEL_NAME):
        self.model = model
        try:
            with open(PROMPT_PATH, "r", encoding="utf-8") as f:
                self.system_prompt = f.read()
        except Exception as e:
            logger.error(f"Failed to load prompt: {e}")
            self.system_prompt = "You are a support agent. Write a helpful email."

    def generate(self, 
                 subject: str, 
                 body: str, 
                 classification: dict, 
                 retrieved_docs: List[dict], 
                 action: str) -> str:
        """
        Generates a final support response based on the full workflow context.
        """
        # Handle internal/non-reply actions immediately
        if action == "close_spam":
            return "INTERNAL: This email was identified as spam. No response sent to customer."
        
        # Prepare context string from retrieved documents
        context_str = "\n\n".join([f"--- Source: {doc['source']} ---\n{doc['content']}" for doc in retrieved_docs])
        if not context_str:
            context_str = "No specific help documentation found for this query."

        # Construct the generation prompt
        prompt = f"Customer Message: {body}\n\nHelp Documentation:\n{context_str}\n\nPlease write the professional email reply now:"

        try:
            logger.info(f"Generating AI response for action: {action}")
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                options={"temperature": 0.1} # Lower temp for more predictability
            )
            
            generated_text = response['message']['content'].strip()
            
            # --- STRIKE: Clean up any leaked internal labels ---
            labels_to_scrub = ["escalate_human:", "auto_reply:", "route_technical:", "Action:", "FINAL RESPONSE:"]
            for label in labels_to_scrub:
                if generated_text.startswith(label):
                    generated_text = generated_text[len(label):].strip()
                generated_text = generated_text.replace(label, "")
            
            return generated_text.strip()

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "We've received your request and our team is looking into it. We'll get back to you shortly."

def generate_support_response(subject: str, body: str, classification: dict, retrieved_docs: List[dict], action: str) -> str:
    """Functional wrapper for ResponseGenerator."""
    generator = ResponseGenerator()
    return generator.generate(subject, body, classification, retrieved_docs, action)
