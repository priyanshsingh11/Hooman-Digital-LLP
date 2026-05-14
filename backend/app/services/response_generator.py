import logging
import ollama
from typing import List, Dict, Optional

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# --- Configuration ---
MODEL_NAME = "llama3:latest"

SYSTEM_PROMPT = """
You are an elite Customer Support AI for Lumen.

CONSTRAINTS:
1. Be CONCISE and OPERATIONAL. Avoid fluff or long apologies.
2. Ground your answer ONLY in the provided "Retrieved Context".
3. No more than 3-4 sentences total.
4. Match the customer's sentiment but stay professional.
5. If no answer is found in context, say: "I've reviewed our documentation and am escalating this to a specialist for further investigation."

ACTION-SPECIFIC INSTRUCTIONS:
- escalate_human: Provide a brief summary of the issue for the agent.
- close_spam: State "INTERNAL: No reply generated for spam."
- others: Provide direct instructions or the requested info based on docs.
"""

class ResponseGenerator:
    """
    Generates grounded AI responses using retrieved context and Ollama.
    """
    def __init__(self, model: str = MODEL_NAME):
        self.model = model

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
        prompt = f"""
        CUSTOMER EMAIL:
        Subject: {subject}
        Body: {body}

        CLASSIFICATION:
        Category: {classification.get('category')}
        Urgency: {classification.get('urgency')}
        Sentiment: {classification.get('sentiment')}

        WORKFLOW ACTION: {action}

        RETRIEVED CONTEXT (Use this to answer):
        {context_str}

        FINAL RESPONSE:
        """

        try:
            logger.info(f"Generating AI response for action: {action}")
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                options={"temperature": 0.2} # Slight creativity while staying grounded
            )
            
            generated_text = response['message']['content'].strip()
            return generated_text

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "We've received your request and our team is looking into it. We'll get back to you shortly."

def generate_support_response(subject: str, body: str, classification: dict, retrieved_docs: List[dict], action: str) -> str:
    """Functional wrapper for ResponseGenerator."""
    generator = ResponseGenerator()
    return generator.generate(subject, body, classification, retrieved_docs, action)
