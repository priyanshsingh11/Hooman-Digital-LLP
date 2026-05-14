# Lumen AI: Production-Grade Customer Support Orchestration System

Lumen AI is a high-fidelity, local-first support automation engine designed to bridge the gap between raw LLM reasoning and deterministic business logic. By combining **Semantic RAG Retrieval**, **Hybrid Orchestration**, and **Real-Time Observability**, Lumen provides a scalable solution for SaaS companies to automate their support workflows without sacrificing accuracy or data privacy.

---

## 🏗 Architecture Overview

Lumen follows a modular pipeline design, ensuring each request is classified, grounded, and validated before any response is generated.

```text
       Customer Email
             ↓
[ 1. AI Intent Classifier ] → (Category, Urgency, Sentiment)
             ↓
[ 2. Semantic Retriever ] ← (ChromaDB + Help Docs)
             ↓
[ 3. Workflow Orchestrator ] → (Deterministic Routing Rules)
             ↓
[ 4. Response Generator ] → (Grounded Contextual Reply)
             ↓
[ 5. Observability Dashboard ] → (Metrics, Latency, Logs)
```

---

## 🚀 Core Features

*   **Semantic Classification**: Zero-shot intent detection using Llama 3.1 to extract category, urgency, and user sentiment.
*   **Grounded RAG Retrieval**: High-precision search across internal documentation using `nomic-embed-text` and ChromaDB.
*   **Hybrid Orchestration**: A unique blend of LLM intelligence and deterministic Python-based "guardrail" logic.
*   **Automated Escalation**: Intelligent routing that identifies legal threats or extreme frustration for immediate human intervention.
*   **Security-First Design**: Local-first inference via Ollama ensures customer data never leaves the local environment.
*   **Real-Time Dashboard**: Comprehensive Next.js interface for live log monitoring and performance visualization.
*   **Evaluation Framework**: Built-in scripts to measure system accuracy and retrieval hit rates against ground-truth datasets.

---

## 💻 Tech Stack

### Frontend
*   **Framework**: Next.js 14 (App Router)
*   **Styling**: Tailwind CSS
*   **Icons/UI**: Lucide React, Framer Motion
*   **Visualization**: Recharts

### Backend
*   **Language**: Python 3.10+
*   **API Framework**: FastAPI
*   **Vector DB**: ChromaDB
*   **AI Inference**: Ollama (Llama 3.1 8B, Llama 3.2 3B)
*   **Embeddings**: nomic-embed-text

---

## 🔄 Workflow Explanation

The Lumen pipeline processes every interaction through five distinct phases:

1.  **Classification**: The raw email is analyzed by Llama 3.1 to identify the "User Intent." We extract structured JSON containing category, urgency, and sentiment.
2.  **Retrieval**: The system performs a vector search in ChromaDB to find the most relevant help documentation, calculating a "Retrieval Fit Score."
3.  **Routing**: The **Orchestrator** applies business rules. For example, if the category is "Security" or urgency is "High," it bypasses automation and routes to a human agent.
4.  **Response Generation**: If automated, the generator synthesizes a reply grounded *strictly* in the retrieved documents, avoiding hallucinations.
5.  **Hybrid Orchestration**: This "Hybrid" approach ensures that while the AI handles the language, the business maintains control over the **Decisions**.

---

## 📊 Evaluation Metrics

Continuous improvement is driven by our automated evaluation suite.

| Metric | Score | Note |
| :--- | :--- | :--- |
| **Classification Accuracy** | 82.0% | Success in identifying intent categories. |
| **Retrieval Hit Rate** | 78.0% | Percentage of queries where correct docs were found. |
| **Workflow Decision Accuracy** | 62.0% | Correctness of the final routing decision. |

### Engineering Insights:
*   **Workflow Evaluation**: This is significantly harder than simple text generation because it requires the system to make the "correct" business choice (e.g., Refund vs. Technical Support).
*   **Iterative Refinement**: We use failure reports to refine our "Heuristic Guardrails" in `workflow.py`, gradually increasing accuracy through policy tuning.

---

## ⚠️ Failure Analysis & Engineering Learnings

| Failure Type | Description | Solution |
| :--- | :--- | :--- |
| **Over-Aggressive Escalation** | AI routing simple tasks to humans too often. | Refined the urgency threshold for technical queries. |
| **Multilingual Issues** | Foreign language emails breaking JSON parsing. | Added a dedicated `multilingual` category. |
| **Retrieval Edge Cases** | Queries about "Dark Mode" when docs don't exist. | Improved "No-Doc" fallback responses. |
| **Prompt Injection** | Users trying to trick the AI into giving refunds. | Implemented a secondary classification check for malicious intent. |

---

## 🖥 Frontend Dashboard

The Lumen Dashboard provides a command-center view of the entire AI system:

*   **Email Simulator**: Test any subject/body combo to see the AI's "thought process" in real-time.
*   **Retrieval Visualization**: See exactly which documents the RAG system pulled and their match percentage.
*   **Execution Timeline**: A live step-by-step breakdown of the pipeline progress (Intent -> Search -> Action -> Reply).
*   **Metrics View**: High-level charts showing automation rates, average confidence, and system latency.

---

## 🛠 Local Setup

### 1. Prerequisites
*   Install [Ollama](https://ollama.ai/)
*   Pull required models:
    ```bash
    ollama pull llama3.1
    ollama pull nomic-embed-text
    ```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # venv/Scripts/activate on Windows
pip install -r requirements.txt
python app/main.py
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 📧 Example Demo Emails

Try these in the Simulator to see the Orchestrator in action:

*   **Refund Request**: `Subject: Need a refund | Body: I was charged twice this month and want my money back.`
*   **Technical Outage**: `Subject: URGENT: Dashboard down | Body: My team cannot access our analytics since this morning.`
*   **Security Concern**: `Subject: Suspicious Login | Body: I just got an email about a login from a device I don't recognize.`
*   **Spam**: `Subject: You Won! | Body: Claim your $1M lottery prize by clicking this link.`

---

## 🏗 Engineering Design Decisions

*   **Why Deterministic Routing?**: Pure LLM routing is prone to "drifting." By using Python-based rules for final decisions, we guarantee that high-risk tickets (Legal/Security) **always** reach a human.
*   **Why Hybrid Orchestration?**: It combines the "Soft Skills" of an LLM with the "Hard Logic" of a software system, creating a safer and more predictable support agent.
*   **Why Local-First?**: For support systems handling sensitive customer data (SSNs, Billing IDs), local inference via Ollama is the only way to guarantee 100% data privacy.

---

## 🔮 Future Improvements

*   🔍 **Chunk-Level Retrieval**: Moving from full-doc retrieval to granular chunking for better precision.
*   📈 **Cross-Reranking**: Implementing a second-stage reranker to refine document relevance.
*   🌊 **Streaming Responses**: Adding WebSocket support for real-time AI typing effects.
*   🐳 **Dockerization**: Containerizing the entire stack for one-click deployment.

---

*This project was developed for Hooman Digital LLP as a high-fidelity AI Orchestration prototype.*
