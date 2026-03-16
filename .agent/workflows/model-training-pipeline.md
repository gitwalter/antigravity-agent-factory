---
description: Comprehensive workflow for training machine learning models from data
  preparation through hyperparameter optimization...
version: 1.0.0
tags:
- model
- training
- pipeline
- standardized
---


# Model Training Pipeline

Comprehensive workflow for training machine learning models from data preparation through hyperparameter optimization to model registry and deployment readiness.

**Version:** 1.0.0
**Created:** 2026-02-09
**Agent:** template-creator

> **Note:** Directory paths referenced in this workflow ({directories.knowledge}/, {directories.skills}/, {directories.patterns}/, etc.) are configurable via `{directories.config}/settings.json`.

## Trigger Conditions

This workflow is activated when:

- User requests "train model", "model training", "ML training"
- User mentions "PyTorch training", "distributed training", "hyperparameter tuning"
- User requests "model development" or "ML pipeline"
- User asks to "build ML model"

**Trigger Examples:**
- "Train a PyTorch model for image classification"
- "Set up distributed training pipeline"
- "Create ML training workflow with hyperparameter tuning"
- "Train model with MLflow tracking"

## Phases

### Phase 1: Data Preparation & Exploration
- **Goal**: Ingest, explore, and preprocess data for model training.
- **Agents**: `project-operations-specialist`, `python-ai-specialist`
- **Skills**: data-pipeline-orchestration, analyzing-code
- **Tools**: conda-run
- **Actions**:
    - Load and explore data.
    - Preprocess, split, and validate the dataset.

### Phase 2: Architecture & Setup
- **Goal**: Define the model structure and configure the training loop and experiment tracking.
- **Agents**: `python-ai-specialist`
- **Skills**: ml-experiment
- **Tools**: write_to_file
- **Actions**:
    - Define model architecture and configure training loop.
    - Set up experiment tracking (e.g., MLflow, WandB).

### Phase 3: Training & Optimization
- **Goal**: Execute training runs and optimize hyperparameters for maximum performance.
- **Agents**: `python-ai-specialist`
- **Skills**: ml-experiment
- **Tools**: conda-run
- **Actions**:
    - Initial training run and hyperparameter optimization.
    - Final training and evaluation on the test set.

### Phase 4: Error Analysis & Registration
- **Goal**: Perform detailed error analysis and register the best performing model.
- **Agents**: `workflow-quality-specialist`, `python-ai-specialist`
- **Skills**: evaluating-llms, committing-releases
- **Tools**: write_to_file
- **Actions**:
    - Perform error analysis and register the model.
    - Export the model and create deployment artifacts.


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
