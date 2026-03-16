---
agents:
- workflow-quality-specialist
- project-operations-specialist
- python-ai-specialist
blueprints:
- universal
description: Antigravity workflow for model-training-pipeline. Standardized for IDX
  Visual Editor.
domain: universal
name: model-training-pipeline
steps:
- actions:
  - '**Agents**: `project-operations-specialist`, `python-ai-specialist`'
  - '**Actions**:'
  - Load and explore data.
  - Preprocess, split, and validate the dataset.
  agents:
  - project-operations-specialist
  - python-ai-specialist
  goal: Ingest, explore, and preprocess data for model training.
  name: Data Preparation & Exploration
  skills:
  - data-pipeline-orchestration
  - analyzing-code
  tools:
  - conda-run
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Define model architecture and configure training loop.
  - Set up experiment tracking (e.g., MLflow, WandB).
  agents:
  - python-ai-specialist
  goal: Define the model structure and configure the training loop and experiment
    tracking.
  name: Architecture & Setup
  skills:
  - ml-experiment
  tools:
  - write_to_file
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Initial training run and hyperparameter optimization.
  - Final training and evaluation on the test set.
  agents:
  - python-ai-specialist
  goal: Execute training runs and optimize hyperparameters for maximum performance.
  name: Training & Optimization
  skills:
  - ml-experiment
  tools:
  - conda-run
- actions:
  - '**Agents**: `workflow-quality-specialist`, `python-ai-specialist`'
  - '**Actions**:'
  - Perform error analysis and register the model.
  - Export the model and create deployment artifacts.
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - workflow-quality-specialist
  - python-ai-specialist
  goal: Perform detailed error analysis and register the best performing model.
  name: Error Analysis & Registration
  skills:
  - evaluating-llms
  - committing-releases
  tools:
  - write_to_file
tags: []
type: sequential
version: 1.0.0
---

# Model Training Pipeline

**Version:** 1.0.0

## Overview
Antigravity workflow for machine learning model training and experiment tracking. Standardized for IDX Visual Editor.

## Trigger Conditions
- New data available for model retraining or initial training phase.
- Need to experiment with different model architectures or training parameters.
- User request: `/model-training-pipeline`.

**Trigger Examples:**
- "Train a new sentiment analysis model using the 'Twitter 2024' dataset."
- "Execute a training pipeline for the 'Recommendation Engine' with MLflow tracking."

## Phases

### 1. Data Preparation & Exploration
- **Goal**: Ingest, explore, and preprocess data for model training.
- **Agents**: `project-operations-specialist`, `python-ai-specialist`
- **Skills**: data-pipeline-orchestration, analyzing-code
- **Tools**: conda-run
- **Agents**: `project-operations-specialist`, `python-ai-specialist`
- **Actions**:
- Load and explore data.
- Preprocess, split, and validate the dataset.

### 2. Architecture & Setup
- **Goal**: Define the model structure and configure the training loop and experiment tracking.
- **Agents**: `python-ai-specialist`
- **Skills**: ml-experiment
- **Tools**: write_to_file
- **Agents**: `python-ai-specialist`
- **Actions**:
- Define model architecture and configure training loop.
- Set up experiment tracking (e.g., MLflow, WandB).

### 3. Training & Optimization
- **Goal**: Execute training runs and optimize hyperparameters for maximum performance.
- **Agents**: `python-ai-specialist`
- **Skills**: ml-experiment
- **Tools**: conda-run
- **Agents**: `python-ai-specialist`
- **Actions**:
- Initial training run and hyperparameter optimization.
- Final training and evaluation on the test set.

### 4. Error Analysis & Registration
- **Goal**: Perform detailed error analysis and register the best performing model.
- **Agents**: `workflow-quality-specialist`, `python-ai-specialist`
- **Skills**: evaluating-llms, committing-releases
- **Tools**: write_to_file
- **Agents**: `workflow-quality-specialist`, `python-ai-specialist`
- **Actions**:
- Perform error analysis and register the model.
- Export the model and create deployment artifacts.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
