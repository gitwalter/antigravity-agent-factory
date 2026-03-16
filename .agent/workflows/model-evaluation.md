---
agents:
- workflow-quality-specialist
- python-ai-specialist
blueprints:
- universal
description: Antigravity workflow for model-evaluation. Standardized for IDX Visual
  Editor.
domain: universal
name: model-evaluation
steps:
- actions:
  - '**Agents**: `python-ai-specialist`, `workflow-quality-specialist`'
  - '**Actions**:'
  - Define evaluation metrics (Classification, Regression, LLM).
  - Prepare the evaluation dataset and baseline models.
  agents:
  - python-ai-specialist
  - workflow-quality-specialist
  goal: Define the evaluation objective and select appropriate metrics for the specific
    model type.
  name: Planning & Metric Selection
  skills:
  - evaluating-llms
  - brainstorming-ideas
  tools:
  - search_web
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Execute evaluation across all metrics.
  - Compare models and calculate statistical significance.
  agents:
  - python-ai-specialist
  goal: Run evaluations and perform statistical comparison between models.
  name: Execution & Comparison
  skills:
  - evaluating-llms
  tools:
  - conda-run
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Analyze failure modes and generate the evaluation report.
  - Share and archive results.
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - workflow-quality-specialist
  goal: Analyze failure modes and generate a comprehensive performance report.
  name: Error Analysis & Reporting
  skills:
  - evaluating-llms
  - generating-documentation
  tools:
  - write_to_file
tags: []
type: sequential
version: 1.0.0
---

# Model Evaluation

**Version:** 1.0.0

## Overview
Antigravity workflow for comprehensive evaluation of machine learning models. Standardized for IDX Visual Editor.

## Trigger Conditions
- Completion of a model training or fine-tuning phase.
- Need for quantitative and qualitative performance assessment.
- User request: `/model-evaluation`.

**Trigger Examples:**
- "Evaluate the accuracy of the new 'Classification' model on the test dataset."
- "Perform error analysis for the 'LLM Summarization' task to identify common failure modes."

## Phases

### 1. Planning & Metric Selection
- **Goal**: Define the evaluation objective and select appropriate metrics for the specific model type.
- **Agents**: `python-ai-specialist`, `workflow-quality-specialist`
- **Skills**: evaluating-llms, brainstorming-ideas
- **Tools**: search_web
- **Agents**: `python-ai-specialist`, `workflow-quality-specialist`
- **Actions**:
- Define evaluation metrics (Classification, Regression, LLM).
- Prepare the evaluation dataset and baseline models.

### 2. Execution & Comparison
- **Goal**: Run evaluations and perform statistical comparison between models.
- **Agents**: `python-ai-specialist`
- **Skills**: evaluating-llms
- **Tools**: conda-run
- **Agents**: `python-ai-specialist`
- **Actions**:
- Execute evaluation across all metrics.
- Compare models and calculate statistical significance.

### 3. Error Analysis & Reporting
- **Goal**: Analyze failure modes and generate a comprehensive performance report.
- **Agents**: `workflow-quality-specialist`
- **Skills**: evaluating-llms, generating-documentation
- **Tools**: write_to_file
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Analyze failure modes and generate the evaluation report.
- Share and archive results.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
