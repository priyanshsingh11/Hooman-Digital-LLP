# Prompt Version & Regression Log

This log tracks the iteration of AI prompts and the corresponding performance changes in the evaluation harness.

## v1.0: Baseline (Initial Draft)
- **Classifier**: Simple list of categories in a string literal.
- **Generator**: Basic instruction to "be helpful".
- **Metrics**: 
  - Classification Accuracy: 68%
  - Judge Accuracy: 2.1/5.0
- **Notes**: High rate of JSON parsing errors. The AI was "guessing" facts not in the context.

## v1.1: Schema Enforcement & Personas (Current)
- **Classifier**: Added `### ROLE` (Triage Specialist) and strict JSON schema rules.
- **Generator**: Added `### ROLE` (Senior Success Engineer) and explicit `NEVER make up facts` rule.
- **Metrics**: 
  - Classification Accuracy: **82%** (+14%)
  - Judge Tone: **5.0/5.0** (+1.2)
  - Judge Fact Accuracy: **3.2/5.0** (+1.1)
- **Notes**: JSON stability is now 100%. Tone is significantly more professional.

## Regression Detection Workflow
To prevent performance degradation, any change to files in `backend/app/prompts/` must be followed by running:
1. `python backend/app/evals/evaluate_classifier.py`
2. `python backend/app/evals/judge_evaluation.py`

If any score drops by >5%, the change is rejected as a regression.
