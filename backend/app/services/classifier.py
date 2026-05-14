import json
import logging
import re
import ollama
from typing import Dict, Optional

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# --- Configuration ---
MODEL_NAME = "llama3.1:8b"

SYSTEM_PROMPT = """
You are an expert customer support email classifier for a SaaS company. 
Your task is to analyze the provided email and return a structured JSON response.

CLASSIFICATION CRITERIA:
1. Category: [billing, technical_issue, account_access, feature_request, refund_request, security_concern, spam]
2. Urgency: [low, medium, high]
3. Sentiment: [calm, frustrated, angry, confused]

RULES:
- Return ONLY valid JSON.
- Do not include any conversational text or explanation.
- Ensure all keys are present: "category", "urgency", "sentiment", "reasoning".
- Be precise and objective.
"""

class EmailClassifier:
    """
    Classifies support emails using Ollama's Llama 3.1 model with structured output.
    """
    def __init__(self, model: str = MODEL_NAME):
        self.model = model

    def _extract_json(self, text: str) -> Optional[Dict]:
        """Attempt to extract and parse JSON from the model's raw string output."""
        try:
            # Use regex to find anything between curly braces if the model adds markdown
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group())
            return json.loads(text)
        except (json.JSONDecodeError, AttributeError) as e:
            logger.error(f"JSON parsing failed: {e}")
            return None

    def classify(self, subject: str, body: str, max_retries: int = 3) -> Dict:
        """
        Main method to classify an email with retry logic for JSON enforcement.
        """
        email_content = f"Subject: {subject}\nBody: {body}"
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Classifying email (Attempt {attempt + 1}/{max_retries})...")
                
                response = ollama.chat(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": email_content}
                    ],
                    options={"temperature": 0}  # Low temperature for consistent JSON
                )
                
                raw_output = response['message']['content']
                result = self._extract_json(raw_output)
                
                if result and all(key in result for key in ["category", "urgency", "sentiment"]):
                    logger.info(f"Successfully classified as: {result['category']}")
                    return result
                
                logger.warning(f"Invalid or incomplete JSON on attempt {attempt + 1}. Retrying...")
                
            except Exception as e:
                logger.error(f"Error during Ollama chat: {e}")
            
        # Fallback if all retries fail
        return {
            "category": "technical_issue",
            "urgency": "medium",
            "sentiment": "calm",
            "reasoning": "Fallback used due to classification failure."
        }

def classify_support_email(subject: str, body: str) -> Dict:
    """Functional wrapper for the EmailClassifier."""
    classifier = EmailClassifier()
    return classifier.classify(subject, body)
