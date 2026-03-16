---
description: Comprehensive workflow for developing production-ready FastAPI applications
  with SQLAlchemy async patterns, Pydantic ...
version: 1.0.0
tags:
- fastapi
- api
- development
- standardized
---


# Fastapi Api Development

Comprehensive workflow for developing production-ready FastAPI applications with SQLAlchemy async patterns, Pydantic validation, and best practices. This workflow guides through project setup, domain modeling, API endpoints, testing-agents, and deployment.

**Version:** 1.0.0
**Created:** 2026-02-09
**Agent:** template-creator

> **Note:** Directory paths referenced in this workflow ({directories.knowledge}/, {directories.skills}/, {directories.patterns}/, etc.) are configurable via `{directories.config}/settings.json`.

## Trigger Conditions

This workflow is activated when:

- User requests "create FastAPI API", "build Python API", "FastAPI endpoint"
- User mentions "SQLAlchemy", "async database", "Pydantic schema"
- User requests "Python web service" or "async Python API"
- User asks to "create REST API with Python"

**Trigger Examples:**
- "Create a FastAPI API for managing products"
- "Build an async Python API with SQLAlchemy"
- "Create FastAPI endpoints with Pydantic validation"
- "Set up a Python web service with database acce

## Phases

### Phase 1: Project Setup & Configuration
- **Goal**: Establish a production-ready FastAPI environment with proper dependency management.
- **Agents**: `project-operations-specialist`
- **Skills**: developing-ai-agents
- **Tools**: conda-run, write_to_file
- **Actions**:
    - Create project structure and install dependencies.
    - Configure project settings and environment variables.

### Phase 2: Domain Modeling & Schema Definition
- **Goal**: Design the data layer using SQLAlchemy and Pydantic for validation.
- **Agents**: `python-ai-specialist`
- **Skills**: designing-apis, analyzing-code
- **Tools**: multi_replace_file_content
- **Actions**:
    - Define SQLAlchemy models and create Pydantic schemas.
    - Configure database and create the initial migration.

### Phase 3: Business Logic & API Implementation
- **Goal**: Implement the service layer, repository pattern, and RESTful endpoints.
- **Agents**: `python-ai-specialist`
- **Skills**: developing-ai-agents
- **Tools**: replace_file_content
- **Actions**:
    - Implement service layer and repository pattern.
    - Create API endpoints and configure dependencies.
    - Add middleware for logging and security.

### Phase 4: Testing & Quality Assurance
- **Goal**: Ensure robustness through unit and integration testing-agents.
- **Agents**: `workflow-quality-specialist`
- **Skills**: verifying-artifact-structures
- **Tools**: pytest
- **Actions**:
    - Set up test infrastructure and write unit/integration tests.

### Phase 5: Containerization & Ops
- **Goal**: Prepare the application for production deployment with Docker and health logging-and-monitoring.
- **Agents**: `project-operations-specialist`
- **Skills**: cicd-pipeline, logging-and-monitoring
- **Tools**: docker, write_to_file
- **Actions**:
    - Configure production settings and add health checks.
    - Create Dockerfile and configure application server (e.g., Uvicorn).


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
