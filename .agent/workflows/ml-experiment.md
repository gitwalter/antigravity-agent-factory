---
agents:
- workflow-quality-specialist
- project-operations-specialist
- python-ai-specialist
blueprints:
- universal
description: Antigravity workflow for ml-experiment. Standardized for IDX Visual Editor.
domain: universal
name: ml-experiment
steps:
- actions:
  - '**Agents**: `python-ai-specialist`, `project-operations-specialist`'
  - '**Actions**:'
  - Formulate hypothesis and design the experiment.
  agents:
  - python-ai-specialist
  - project-operations-specialist
  goal: Define the hypothesis and establish the experimental framework.
  name: Research & Experiment Design
  skills:
  - brainstorming-ideas
  - researching-first
  tools:
  - search_web
  - deepwiki
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Prepare data and set up the compute environment.
  agents:
  - project-operations-specialist
  goal: Prepare datasets and configure the training environment.
  name: Data & Environment Readiness
  skills:
  - data-pipeline-orchestration
  tools:
  - conda-run
  - write_to_file
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Run training and hyperparameter search.
  agents:
  - python-ai-specialist
  goal: Run model training and perform hyperparameter search for optimal results.
  name: Execution & Optimization
  skills:
  - ml-experiment
  tools:
  - conda-run
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Evaluate model and interpret/report results.
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - workflow-quality-specialist
  goal: Assess model performance and document findings for reproducibility.
  name: Evaluation & Reporting
  skills:
  - evaluating-llms
  tools:
  - write_to_file
tags: []
type: sequential
version: 2.0.0
---
# ML Experimentation Workflow

**Version:** 1.0.0

## Overview
Antigravity workflow for conducting and documenting machine learning experiments. Standardized for IDX Visual Editor.

## Trigger Conditions
- Formulation of a new machine learning hypothesis or model architecture idea.
- Need to conduct hyperparameter optimization or data experimentation.
- User request: `/ml-experiment`.

**Trigger Examples:**
- "Conduct an experiment to compare Transformer models with LSTM for time-series forecasting."
- "Perform hyperparameter search for the 'Object Detection' model using the new dataset."

## Phases

### 1. Research & Experiment Design
- **Goal**: Define the hypothesis and establish the experimental framework.
- **Agents**: `python-ai-specialist`, `project-operations-specialist`
- **Skills**: brainstorming-ideas, researching-first
- **Tools**: search_web, deepwiki
- **Agents**: `python-ai-specialist`, `project-operations-specialist`
- **Actions**:
- Formulate hypothesis and design the experiment.

### 2. Data & Environment Readiness
- **Goal**: Prepare datasets and configure the training environment.
- **Agents**: `project-operations-specialist`
- **Skills**: data-pipeline-orchestration
- **Tools**: conda-run, write_to_file
- **Agents**: `project-operations-specialist`
- **Actions**:
- Prepare data and set up the compute environment.

### 3. Execution & Optimization
- **Goal**: Run model training and perform hyperparameter search for optimal results.
- **Agents**: `python-ai-specialist`
- **Skills**: ml-experiment
- **Tools**: conda-run
- **Agents**: `python-ai-specialist`
- **Actions**:
- Run training and hyperparameter search.

### 4. Evaluation & Reporting
- **Goal**: Assess model performance and document findings for reproducibility.
- **Agents**: `workflow-quality-specialist`
- **Skills**: evaluating-llms
- **Tools**: write_to_file
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Evaluate model and interpret/report results.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
