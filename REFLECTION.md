# Engineering Reflection: Lumen AI Orchestrator

## 1. Architectural Choices & Trade-offs

### Deterministic vs. Probabilistic Orchestration
I chose a **Hybrid Orchestration** model. While the intent classification is handled by Llama 3.2 (probabilistic), the final routing decision is gated by a Python-based orchestrator (deterministic). 
- **The Trade-off**: I sacrificed the flexibility of a "pure agent" (like LangChain's ReAct) for 100% predictability in high-risk scenarios. In a real support environment, we cannot allow an LLM to accidentally authorize a refund; it must follow business rules.

### Local-First Inference
The system runs entirely on **Ollama (Llama 3.2 3B)**. 
- **The Trade-off**: We saved thousands in API costs and guaranteed 100% data privacy for customer PII. However, the qualitative evaluation showed a **3.2/5 in Fact Accuracy**, indicating that the 3B model occasionally struggles with complex document grounding compared to larger models like GPT-4.

## 2. Qualitative Evaluation Analysis
Our "LLM-as-a-Judge" report revealed a high **Tone (5.0/5.0)** but lower **Fact Accuracy (3.2/5.0)**. 
- **Insight**: The AI sounds professional but sometimes misses the specific technical nuances in the help documentation.
- **Trust Factor**: I trust the **Classification** and **Tone** the most. I trust the **RAG Grounding** the least. If I had another week, I would implement a "Self-Correction" loop where a second LLM pass verifies the response against the context before showing it to the human operator.

## 3. Human-in-the-Loop (HITL) Philosophy
The dashboard was designed for a **Support Lead**, not a developer. I implemented an "Approval Queue" because AI in its current state should be an *accelerator*, not a *replacement*. By allowing humans to edit and approve drafts, we reduce "engineering load" while maintaining a 0% hallucination rate for the end customer.

## 4. Scalability & Future Roadmap
If given three more months, I would focus on:
1. **Dynamic Few-Shot Injection**: Automatically pulling past successful human-approved tickets into the prompt to improve the 3.2/5 accuracy score.
2. **Multimodal Support**: Integrating Whisper for voice-note support tickets.
3. **Regression Testing**: Ensuring that updating a prompt for a "Billing" issue doesn't break a "Technical" classification.

## 5. Definition of Success
Three months after launch, I would measure success by the **Human Override Rate**. If agents are approving 90%+ of AI drafts without editing them, the system is a success. If the override rate is high, it indicates a failure in our RAG retrieval or prompt engineering.
