---
description: ML model evaluation workflow covering metrics selection, model comparison,
  and reporting. Supports classification, re...
version: 1.0.0
tags:
- model
- evaluation
- standardized
---


# Model Evaluation

ML model evaluation workflow covering metrics selection, model comparison, and reporting. Supports classification, regression, and LLM evaluation with structured reporting.

**Version:** 1.0.0
**Created:** 2026-02-10
**Applies To:** ml-models, llm-applications

## Trigger Conditions

This workflow is activated when:

- Model evaluation requested
- Model comparison needed
- Pre-deployment validation
- Benchmarking new models

**Trigger Examples:**
- "Evaluate the trained model"
- "Compare model A vs B"
- "Run evaluation and generate report"
- "Benchmark the new fine-tuned model"

## Phases

### Phase 1: Planning & Metric Selection
- **Goal**: Define the evaluation objective and select appropriate metrics for the specific model type.
- **Agents**: `python-ai-specialist`, `workflow-quality-specialist`
- **Skills**: evaluating-llms, brainstorming-ideas
- **Tools**: search_web
- **Actions**:
    - Define evaluation metrics (Classification, Regression, LLM).
    - Prepare the evaluation dataset and baseline models.

### Phase 2: Execution & Comparison
- **Goal**: Run evaluations and perform statistical comparison between models.
- **Agents**: `python-ai-specialist`
- **Skills**: evaluating-llms
- **Tools**: conda-run
- **Actions**:
    - Execute evaluation across all metrics.
    - Compare models and calculate statistical significance.

### Phase 3: Error Analysis & Reporting
- **Goal**: Analyze failure modes and generate a comprehensive performance report.
- **Agents**: `workflow-quality-specialist`
- **Skills**: evaluating-llms, generating-documentation
- **Tools**: write_to_file
- **Actions**:
    - Analyze failure modes and generate the evaluation report.
    - Share and archive results.


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...


## Trigger Examples
- "Execute this workflow."


## Best Practices
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.


## Related
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
