import json
import logging
import re
import ollama
from typing import Dict, Optional

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

import os

# --- Configuration ---
MODEL_NAME = "llama3.2"
PROMPT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts", "classifier.txt")

class EmailClassifier:
    def __init__(self, model: str = MODEL_NAME):
        self.model = model
        try:
            with open(PROMPT_PATH, "r", encoding="utf-8") as f:
                self.system_prompt = f.read()
        except Exception as e:
            logger.error(f"Failed to load prompt: {e}")
            self.system_prompt = "You are a support classifier. Return JSON."

    def classify(self, subject: str, body: str) -> Dict:
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Subject: {subject}\nBody: {body}"}
                ],
                format="json",
                options={"temperature": 0}
            )
            
            result = json.loads(response['message']['content'])
            return result
        except Exception as e:
            logger.error(f"Error during Ollama chat: {e}")
            return {
                "category": "technical_issue",
                "urgency": "medium",
                "sentiment": "neutral",
                "reasoning": "Fallback used due to classification failure."
            }

def classify_support_email(subject: str, body: str) -> Dict:
    """Functional wrapper for EmailClassifier."""
    classifier = EmailClassifier()
    return classifier.classify(subject, body)
