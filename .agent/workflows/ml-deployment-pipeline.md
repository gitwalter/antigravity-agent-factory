---
agents:
- project-operations-specialist
- python-ai-specialist
blueprints:
- universal
description: Antigravity workflow for ml-deployment-pipeline. Standardized for IDX
  Visual Editor.
domain: universal
name: ml-deployment-pipeline
steps:
- actions:
  - '**Agents**: `python-ai-specialist`, `project-operations-specialist`'
  - '**Actions**:'
  - Export and optimize the model.
  - Create the inference server and Dockerfile.
  agents:
  - python-ai-specialist
  - project-operations-specialist
  goal: Optimize the registered model and prepare the inference infrastructure.
  name: Model Optimization & Server Setup
  skills:
  - ml-deployment-pipeline
  - committing-releases
  tools:
  - conda-run
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Build and test the container.
  - Choose the deployment platform and deploy the model service.
  agents:
  - project-operations-specialist
  goal: Build and test the model container and select the deployment platform.
  name: Containerization & Platform Selection
  skills:
  - cicd-pipeline
  tools:
  - docker
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Configure endpoints and production settings.
  - Deploy to production and set up CI/CD.
  agents:
  - project-operations-specialist
  goal: Configure endpoints, security, and CI/CD for the production environment.
  name: Configuration & Deployment
  skills:
  - cicd-pipeline
  - securing-ai-systems
  tools:
  - safe_release.py
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Configure auto-scaling and set up logging-and-monitoring.
  - Continuous logging-and-monitoring of model performance.
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - project-operations-specialist
  goal: Establish auto-scaling and continuous logging-and-monitoring for the deployed
    model.
  name: Scaling & Performance Monitoring
  skills:
  - logging-and-monitoring
  tools:
  - prometheus
  - grafana
tags: []
type: sequential
version: 2.0.0
---
# ML Deployment Pipeline

**Version:** 1.0.0

## Overview
Antigravity workflow for machine learning model deployment pipelines. Standardized for IDX Visual Editor.

## Trigger Conditions
- A machine learning model is registered and ready for production deployment.
- Requirement for automated inference infrastructure and scaling.
- User request: `/ml-deployment-pipeline`.

**Trigger Examples:**
- "Deploy the 'Sales Forecast v2' model to the production Kubernetes cluster."
- "Set up a deployment pipeline for the 'Customer Churn' model with auto-scaling."

## Phases

### 1. Model Optimization & Server Setup
- **Goal**: Optimize the registered model and prepare the inference infrastructure.
- **Agents**: `python-ai-specialist`, `project-operations-specialist`
- **Skills**: ml-deployment-pipeline, committing-releases
- **Tools**: conda-run
- **Agents**: `python-ai-specialist`, `project-operations-specialist`
- **Actions**:
- Export and optimize the model.
- Create the inference server and Dockerfile.

### 2. Containerization & Platform Selection
- **Goal**: Build and test the model container and select the deployment platform.
- **Agents**: `project-operations-specialist`
- **Skills**: cicd-pipeline
- **Tools**: docker
- **Agents**: `project-operations-specialist`
- **Actions**:
- Build and test the container.
- Choose the deployment platform and deploy the model service.

### 3. Configuration & Deployment
- **Goal**: Configure endpoints, security, and CI/CD for the production environment.
- **Agents**: `project-operations-specialist`
- **Skills**: cicd-pipeline, securing-ai-systems
- **Tools**: safe_release.py
- **Agents**: `project-operations-specialist`
- **Actions**:
- Configure endpoints and production settings.
- Deploy to production and set up CI/CD.

### 4. Scaling & Performance Monitoring
- **Goal**: Establish auto-scaling and continuous logging-and-monitoring for the deployed model.
- **Agents**: `project-operations-specialist`
- **Skills**: logging-and-monitoring
- **Tools**: prometheus, grafana
- **Agents**: `project-operations-specialist`
- **Actions**:
- Configure auto-scaling and set up logging-and-monitoring.
- Continuous logging-and-monitoring of model performance.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
