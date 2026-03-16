---
description: Comprehensive workflow for developing production-ready ASP.NET Core APIs
  with Entity Framework Core, authentication, ...
version: 1.0.0
tags:
- dotnet
- api
- development
- standardized
---


# Dotnet Api Development

Comprehensive workflow for developing production-ready ASP.NET Core APIs with Entity Framework Core, authentication, and best practices. This workflow guides through project setup, data layer implementation, API endpoints, security, and deployment.

**Version:** 1.0.0
**Created:** 2026-02-09
**Agent:** template-creator

> **Note:** Directory paths referenced in this workflow ({directories.knowledge}/, {directories.skills}/, {directories.patterns}/, etc.) are configurable via `{directories.config}/settings.json`.

## Trigger Conditions

This workflow is activated when:

- User requests "create ASP.NET Core API", "build REST API", "create .NET API"
- User mentions "Entity Framework", "EF Core", "database access"
- User requests "Minimal API" or "Controller-based API"
- User asks to "create API endpoints" or "build web service"

**Trigger Examples:**
- "Create an ASP.NET Core API for product management"
- "Build a REST API with Entity Framework Core"
- "Create Minimal API endpoints for user management"
- "Set up a .NET API with a

## Phases

### Phase 1: Initialization & Data Modeling
- **Goal**: Set up the .NET solution and define the Entity Framework Core model.
- **Agents**: `project-operations-specialist`, `python-ai-specialist`
- **Skills**: developing-ai-agents
- **Tools**: dotnet-cli
- **Actions**:
    - Create project structure and install dependencies.
    - Define entities and configure DbContext.
    - Create initial migration.

### Phase 2: Service Layer & Endpoints
- **Goal**: Implement business logic, repository pattern, and API controllers/minimal APIs.
- **Agents**: `python-ai-specialist`
- **Skills**: developing-ai-agents, designing-apis
- **Tools**: write_to_file
- **Actions**:
    - Implement Repository pattern and services.
    - Create DTOs and API endpoints.

### Phase 3: Security & Validation
- **Goal**: Implement robust authentication, authorization, and input validation.
- **Agents**: `workflow-quality-specialist`
- **Skills**: securing-ai-systems
- **Tools**: replace_file_content
- **Actions**:
    - Add validation and configure authentication/authorization.
    - Add security headers.

### Phase 4: Testing & Documentation
- **Goal**: Verify API behavior and generate Swagger documentation.
- **Agents**: `workflow-quality-specialist`, `project-operations-specialist`
- **Skills**: verifying-artifact-structures, generating-documentation
- **Tools**: dotnet-test, swagger
- **Actions**:
    - Write unit and integration tests.
    - Configure Swagger/OpenAPI and add health checks.

### Phase 5: Deployment Preparation
- **Goal**: Prepare the .NET application for production rollout.
- **Agents**: `project-operations-specialist`
- **Skills**: azure-deployment, committing-releases
- **Tools**: safe_release.py
- **Actions**:
    - Prepare for deployment.


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
