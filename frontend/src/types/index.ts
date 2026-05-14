export interface Classification {
  category: string;
  urgency: string;
  sentiment: string;
  reasoning: string;
  confidence?: number;
}

export interface RetrievedDoc {
  filename: string;
  content: string;
  score?: number;
  source: string;
}

export interface WorkflowResult {
  classification: Classification;
  retrieved_docs: RetrievedDoc[];
  retrieval_confidence?: number;
  action: string;
  generated_response: string;
  workflow_summary: string;
  timestamp: string;
  latency?: {
    classification: number;
    retrieval: number;
    generation: number;
    total: number;
  };
}

export interface Metrics {
  classification_accuracy: number;
  retrieval_hit_rate: number;
  workflow_accuracy: number;
  total_processed: number;
}
