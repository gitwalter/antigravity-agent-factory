---
agents:
- workflow-quality-specialist
- project-operations-specialist
- python-ai-specialist
blueprints:
- universal
description: Antigravity workflow for fastapi-api-development. Standardized for IDX
  Visual Editor.
domain: universal
name: fastapi-api-development
steps:
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Create project structure and install dependencies.
  - Configure project settings and environment variables.
  agents:
  - project-operations-specialist
  goal: Establish a production-ready FastAPI environment with proper dependency management.
  name: Project Setup & Configuration
  skills:
  - developing-ai-agents
  tools:
  - conda-run
  - write_to_file
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Define SQLAlchemy models and create Pydantic schemas.
  - Configure database and create the initial migration.
  agents:
  - python-ai-specialist
  goal: Design the data layer using SQLAlchemy and Pydantic for validation.
  name: Domain Modeling & Schema Definition
  skills:
  - designing-apis
  - analyzing-code
  tools:
  - multi_replace_file_content
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Implement service layer and repository pattern.
  - Create API endpoints and configure dependencies.
  - Add middleware for logging and security.
  agents:
  - python-ai-specialist
  goal: Implement the service layer, repository pattern, and RESTful endpoints.
  name: Business Logic & API Implementation
  skills:
  - developing-ai-agents
  tools:
  - replace_file_content
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Set up test infrastructure and write unit/integration tests.
  agents:
  - workflow-quality-specialist
  goal: Ensure robustness through unit and integration testing-agents.
  name: Testing & Quality Assurance
  skills:
  - verifying-artifact-structures
  tools:
  - pytest
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Configure production settings and add health checks.
  - Create Dockerfile and configure application server (e.g., Uvicorn).
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - project-operations-specialist
  goal: Prepare the application for production deployment with Docker and health logging-and-monitoring.
  name: Containerization & Ops
  skills:
  - cicd-pipeline
  - logging-and-monitoring
  tools:
  - docker
  - write_to_file
tags: []
type: sequential
version: 1.0.0
---

# FastAPI API Development

**Version:** 1.0.0

## Overview
Antigravity workflow for FastAPI API development. Standardized for IDX Visual Editor.

## Trigger Conditions
- Requirement for a high-performance Python-based RESTful API.
- Need for asynchronous processing and type-safe data modeling.
- User request: `/fastapi-api-development`.

**Trigger Examples:**
- "Develop a FastAPI microservice for order processing."
- "Implement an asynchronous background task for data synchronization."

## Phases

### 1. Project Setup & Configuration
- **Goal**: Establish a production-ready FastAPI environment with proper dependency management.
- **Agents**: `project-operations-specialist`
- **Skills**: developing-ai-agents
- **Tools**: conda-run, write_to_file
- **Agents**: `project-operations-specialist`
- **Actions**:
- Create project structure and install dependencies.
- Configure project settings and environment variables.

### 2. Domain Modeling & Schema Definition
- **Goal**: Design the data layer using SQLAlchemy and Pydantic for validation.
- **Agents**: `python-ai-specialist`
- **Skills**: designing-apis, analyzing-code
- **Tools**: multi_replace_file_content
- **Agents**: `python-ai-specialist`
- **Actions**:
- Define SQLAlchemy models and create Pydantic schemas.
- Configure database and create the initial migration.

### 3. Business Logic & API Implementation
- **Goal**: Implement the service layer, repository pattern, and RESTful endpoints.
- **Agents**: `python-ai-specialist`
- **Skills**: developing-ai-agents
- **Tools**: replace_file_content
- **Agents**: `python-ai-specialist`
- **Actions**:
- Implement service layer and repository pattern.
- Create API endpoints and configure dependencies.
- Add middleware for logging and security.

### 4. Testing & Quality Assurance
- **Goal**: Ensure robustness through unit and integration testing-agents.
- **Agents**: `workflow-quality-specialist`
- **Skills**: verifying-artifact-structures
- **Tools**: pytest
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Set up test infrastructure and write unit/integration tests.

### 5. Containerization & Ops
- **Goal**: Prepare the application for production deployment with Docker and health logging-and-monitoring.
- **Agents**: `project-operations-specialist`
- **Skills**: cicd-pipeline, logging-and-monitoring
- **Tools**: docker, write_to_file
- **Agents**: `project-operations-specialist`
- **Actions**:
- Configure production settings and add health checks.
- Create Dockerfile and configure application server (e.g., Uvicorn).
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
