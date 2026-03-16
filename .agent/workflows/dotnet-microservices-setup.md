---
description: Comprehensive workflow for designing and implementing microservices architectures
  with .NET. This workflow covers ser...
version: 1.0.0
tags:
- dotnet
- microservices
- setup
- standardized
---


# Dotnet Microservices Setup

Comprehensive workflow for designing and implementing microservices architectures with .NET. This workflow covers service decomposition, service creation, communication layer setup, API Gateway configuration, and observability implementation.

**Version:** 1.0.0
**Created:** 2026-02-09
**Agent:** system-architecture-specialist

> **Note:** Directory paths referenced in this workflow ({directories.knowledge}/, {directories.skills}/, {directories.patterns}/, etc.) are configurable via `{directories.config}/settings.json`.

## Trigger Conditions

This workflow is activated when:

- User requests "microservices architecture", "service decomposition"
- User mentions "API Gateway", "YARP", "service communication"
- User requests "distributed system", "service mesh"
- User asks to "break down monolith" or "create microservices"

**Trigger Examples:**
- "Design a microservices architecture for e-commerce platform"
- "Set up API Gateway with YARP for my services"
- "Create microservices with gRPC communication"
- "Implement service-to-service

## Phases

### Phase 1: Design & Decomposition
- **Goal**: Identify business capabilities and define microservice boundaries and data ownership.
- **Agents**: `system-architecture-specialist`
- **Skills**: designing-ai-systems, brainstorming-ideas
- **Tools**: deepwiki
- **Actions**:
    - Identify business capabilities and define boundaries.
    - Design data ownership and API contracts.

### Phase 2: Service & Communication Setup
- **Goal**: Initialize service projects and implement core logic and communication layers (gRPC, REST, Message Broker).
- **Agents**: `python-ai-specialist`, `project-operations-specialist`
- **Skills**: dotnet-microservices-setup, developing-ai-agents
- **Tools**: dotnet-cli, write_to_file
- **Actions**:
    - Create projects and implement service logic.
    - Configure databases and implement endpoints.
    - Configure sync/async communication and resilience patterns.

### Phase 3: Gateway & Observability
- **Goal**: Set up the API Gateway and establish distributed tracing, logging, and metrics.
- **Agents**: `project-operations-specialist`, `workflow-quality-specialist`
- **Skills**: cicd-pipeline, logging-and-monitoring
- **Tools**: yarp, opentelemetry
- **Actions**:
    - Create API Gateway and configure routing.
    - Configure distributed tracing, logging, and metrics.
    - Implement health checks.


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
