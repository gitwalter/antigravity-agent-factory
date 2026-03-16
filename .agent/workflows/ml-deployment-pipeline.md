---
description: Comprehensive workflow for deploying machine learning models to production
  including model export, containerization, ...
version: 1.0.0
tags:
- ml
- deployment
- pipeline
- standardized
---


# Ml Deployment Pipeline

Comprehensive workflow for deploying machine learning models to production including model export, containerization, serving, and logging-and-monitoring.

**Version:** 1.0.0
**Created:** 2026-02-09
**Agent:** system-architecture-specialist

> **Note:** Directory paths referenced in this workflow ({directories.knowledge}/, {directories.skills}/, {directories.patterns}/, etc.) are configurable via `{directories.config}/settings.json`.

## Trigger Conditions

This workflow is activated when:

- User requests "deploy model", "model serving", "ML deployment"
- User mentions "model serving", "inference endpoint", "production model"
- User requests "deploy to production" or "model hosting"
- User asks to "serve ML model"

**Trigger Examples:**
- "Deploy PyTorch model to production"
- "Create inference endpoint for ML model"
- "Deploy model with vLLM"
- "Set up model serving on Kubernetes"

## Phases

### Phase 1: Model Optimization & Server Setup
- **Goal**: Optimize the registered model and prepare the inference infrastructure.
- **Agents**: `python-ai-specialist`, `project-operations-specialist`
- **Skills**: ml-deployment-pipeline, committing-releases
- **Tools**: conda-run
- **Actions**:
    - Export and optimize the model.
    - Create the inference server and Dockerfile.

### Phase 2: Containerization & Platform Selection
- **Goal**: Build and test the model container and select the deployment platform.
- **Agents**: `project-operations-specialist`
- **Skills**: cicd-pipeline
- **Tools**: docker
- **Actions**:
    - Build and test the container.
    - Choose the deployment platform and deploy the model service.

### Phase 3: Configuration & Deployment
- **Goal**: Configure endpoints, security, and CI/CD for the production environment.
- **Agents**: `project-operations-specialist`
- **Skills**: cicd-pipeline, securing-ai-systems
- **Tools**: safe_release.py
- **Actions**:
    - Configure endpoints and production settings.
    - Deploy to production and set up CI/CD.

### Phase 4: Scaling & Performance Monitoring
- **Goal**: Establish auto-scaling and continuous logging-and-monitoring for the deployed model.
- **Agents**: `project-operations-specialist`
- **Skills**: logging-and-monitoring
- **Tools**: prometheus, grafana
- **Actions**:
    - Configure auto-scaling and set up logging-and-monitoring.
    - Continuous logging-and-monitoring of model performance.


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
