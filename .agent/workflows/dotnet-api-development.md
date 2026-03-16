---
agents:
- workflow-quality-specialist
- project-operations-specialist
- python-ai-specialist
blueprints:
- universal
description: Antigravity workflow for dotnet-api-development. Standardized for IDX
  Visual Editor.
domain: universal
name: dotnet-api-development
steps:
- actions:
  - '**Agents**: `project-operations-specialist`, `python-ai-specialist`'
  - '**Actions**:'
  - Create project structure and install dependencies.
  - Define entities and configure DbContext.
  - Create initial migration.
  agents:
  - project-operations-specialist
  - python-ai-specialist
  goal: Set up the .NET solution and define the Entity Framework Core model.
  name: Initialization & Data Modeling
  skills:
  - developing-ai-agents
  tools:
  - dotnet-cli
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Implement Repository pattern and services.
  - Create DTOs and API endpoints.
  agents:
  - python-ai-specialist
  goal: Implement business logic, repository pattern, and API controllers/minimal
    APIs.
  name: Service Layer & Endpoints
  skills:
  - developing-ai-agents
  - designing-apis
  tools:
  - write_to_file
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Add validation and configure authentication/authorization.
  - Add security headers.
  agents:
  - workflow-quality-specialist
  goal: Implement robust authentication, authorization, and input validation.
  name: Security & Validation
  skills:
  - securing-ai-systems
  tools:
  - replace_file_content
- actions:
  - '**Agents**: `workflow-quality-specialist`, `project-operations-specialist`'
  - '**Actions**:'
  - Write unit and integration tests.
  - Configure Swagger/OpenAPI and add health checks.
  agents:
  - workflow-quality-specialist
  - project-operations-specialist
  goal: Verify API behavior and generate Swagger documentation.
  name: Testing & Documentation
  skills:
  - verifying-artifact-structures
  - generating-documentation
  tools:
  - dotnet-test
  - swagger
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Prepare for deployment.
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - project-operations-specialist
  goal: Prepare the .NET application for production rollout.
  name: Deployment Preparation
  skills:
  - azure-deployment
  - committing-releases
  tools:
  - safe_release.py
tags: []
type: sequential
version: 1.0.0
---

# Dotnet Api Development

**Version:** 1.0.0

## Overview
Antigravity workflow for dotnet-api-development. Standardized for IDX Visual Editor.

## Trigger Conditions
- Requirement for a new .NET Core API or expansion of an existing one.
- Need for data modeling and service layer implementation in C#.
- User request: `/dotnet-api-development`.

**Trigger Examples:**
- "Develop an API for user profile management."
- "Implement a new service layer for the booking system."

## Phases

### 1. Initialization & Data Modeling
- **Goal**: Set up the .NET solution and define the Entity Framework Core model.
- **Agents**: `project-operations-specialist`, `python-ai-specialist`
- **Skills**: developing-ai-agents
- **Tools**: dotnet-cli
- **Agents**: `project-operations-specialist`, `python-ai-specialist`
- **Actions**:
- Create project structure and install dependencies.
- Define entities and configure DbContext.
- Create initial migration.

### 2. Service Layer & Endpoints
- **Goal**: Implement business logic, repository pattern, and API controllers/minimal APIs.
- **Agents**: `python-ai-specialist`
- **Skills**: developing-ai-agents, designing-apis
- **Tools**: write_to_file
- **Agents**: `python-ai-specialist`
- **Actions**:
- Implement Repository pattern and services.
- Create DTOs and API endpoints.

### 3. Security & Validation
- **Goal**: Implement robust authentication, authorization, and input validation.
- **Agents**: `workflow-quality-specialist`
- **Skills**: securing-ai-systems
- **Tools**: replace_file_content
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Add validation and configure authentication/authorization.
- Add security headers.

### 4. Testing & Documentation
- **Goal**: Verify API behavior and generate Swagger documentation.
- **Agents**: `workflow-quality-specialist`, `project-operations-specialist`
- **Skills**: verifying-artifact-structures, generating-documentation
- **Tools**: dotnet-test, swagger
- **Agents**: `workflow-quality-specialist`, `project-operations-specialist`
- **Actions**:
- Write unit and integration tests.
- Configure Swagger/OpenAPI and add health checks.

### 5. Deployment Preparation
- **Goal**: Prepare the .NET application for production rollout.
- **Agents**: `project-operations-specialist`
- **Skills**: azure-deployment, committing-releases
- **Tools**: safe_release.py
- **Agents**: `project-operations-specialist`
- **Actions**:
- Prepare for deployment.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
