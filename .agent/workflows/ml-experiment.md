---
description: ML experiment workflow from hypothesis formation through results analysis.
  Covers experiment setup, training, trackin...
version: 1.0.0
tags:
- ml
- experiment
- standardized
---


# Ml Experiment

ML experiment workflow from hypothesis formation through results analysis. Covers experiment setup, training, tracking, and interpretation for reproducible researching-first.

**Version:** 1.0.0
**Created:** 2026-02-10
**Applies To:** training-models, ml-researching-first

## Trigger Conditions

This workflow is activated when:

- New ML experiment proposed
- Model training or fine-tuning needed
- Hypothesis to validate
- Hyperparameter search requested

**Trigger Examples:**
- "Run an experiment with these hyperparameters"
- "Train a model for this task"
- "Fine-tune the model on our data"
- "Validate this architectural change"

## Phases

### Phase 1: Research & Experiment Design
- **Goal**: Define the hypothesis and establish the experimental framework.
- **Agents**: `python-ai-specialist`, `project-operations-specialist`
- **Skills**: brainstorming-ideas, researching-first
- **Tools**: search_web, deepwiki
- **Actions**:
    - Formulate hypothesis and design the experiment.

### Phase 2: Data & Environment Readiness
- **Goal**: Prepare datasets and configure the training environment.
- **Agents**: `project-operations-specialist`
- **Skills**: data-pipeline-orchestration
- **Tools**: conda-run, write_to_file
- **Actions**:
    - Prepare data and set up the compute environment.

### Phase 3: Execution & Optimization
- **Goal**: Run model training and perform hyperparameter search for optimal results.
- **Agents**: `python-ai-specialist`
- **Skills**: ml-experiment
- **Tools**: conda-run
- **Actions**:
    - Run training and hyperparameter search.

### Phase 4: Evaluation & Reporting
- **Goal**: Assess model performance and document findings for reproducibility.
- **Agents**: `workflow-quality-specialist`
- **Skills**: evaluating-llms
- **Tools**: write_to_file
- **Actions**:
    - Evaluate model and interpret/report results.


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
