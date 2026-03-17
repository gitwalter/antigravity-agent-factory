---
agents:
- workflow-quality-specialist
- system-architecture-specialist
- project-operations-specialist
- python-ai-specialist
blueprints:
- universal
description: Antigravity workflow for dotnet-microservices-setup. Standardized for
  IDX Visual Editor.
domain: universal
name: dotnet-microservices-setup
steps:
- actions:
  - '**Agents**: `system-architecture-specialist`'
  - '**Actions**:'
  - Identify business capabilities and define boundaries.
  - Design data ownership and API contracts.
  agents:
  - system-architecture-specialist
  goal: Identify business capabilities and define microservice boundaries and data
    ownership.
  name: Design & Decomposition
  skills:
  - designing-ai-systems
  - brainstorming-ideas
  tools:
  - deepwiki
- actions:
  - '**Agents**: `python-ai-specialist`, `project-operations-specialist`'
  - '**Actions**:'
  - Create projects and implement service logic.
  - Configure databases and implement endpoints.
  - Configure sync/async communication and resilience patterns.
  agents:
  - python-ai-specialist
  - project-operations-specialist
  goal: Initialize service projects and implement core logic and communication layers
    (gRPC, REST, Message Broker).
  name: Service & Communication Setup
  skills:
  - dotnet-microservices-setup
  - developing-ai-agents
  tools:
  - dotnet-cli
  - write_to_file
- actions:
  - '**Agents**: `project-operations-specialist`, `workflow-quality-specialist`'
  - '**Actions**:'
  - Create API Gateway and configure routing.
  - Configure distributed tracing, logging, and metrics.
  - Implement health checks.
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - project-operations-specialist
  - workflow-quality-specialist
  goal: Set up the API Gateway and establish distributed tracing, logging, and metrics.
  name: Gateway & Observability
  skills:
  - cicd-pipeline
  - logging-and-monitoring
  tools:
  - yarp
  - opentelemetry
tags: []
type: sequential
version: 2.0.0
---
# Dotnet Microservices Setup

**Version:** 1.0.0

## Overview
Antigravity workflow for dotnet-microservices-setup. Standardized for IDX Visual Editor.

## Trigger Conditions
- New microservices architecture design or expansion.
- Need to establish cross-service communication and observability.
- User request: `/dotnet-microservices-setup`.

**Trigger Examples:**
- "Set up a new microservices environment for the e-commerce platform."
- "Configure the API Gateway and tracing for existing services."

## Phases

### 1. Design & Decomposition
- **Goal**: Identify business capabilities and define microservice boundaries and data ownership.
- **Agents**: `system-architecture-specialist`
- **Skills**: designing-ai-systems, brainstorming-ideas
- **Tools**: deepwiki
- **Agents**: `system-architecture-specialist`
- **Actions**:
- Identify business capabilities and define boundaries.
- Design data ownership and API contracts.

### 2. Service & Communication Setup
- **Goal**: Initialize service projects and implement core logic and communication layers (gRPC, REST, Message Broker).
- **Agents**: `python-ai-specialist`, `project-operations-specialist`
- **Skills**: dotnet-microservices-setup, developing-ai-agents
- **Tools**: dotnet-cli, write_to_file
- **Agents**: `python-ai-specialist`, `project-operations-specialist`
- **Actions**:
- Create projects and implement service logic.
- Configure databases and implement endpoints.
- Configure sync/async communication and resilience patterns.

### 3. Gateway & Observability
- **Goal**: Set up the API Gateway and establish distributed tracing, logging, and metrics.
- **Agents**: `project-operations-specialist`, `workflow-quality-specialist`
- **Skills**: cicd-pipeline, logging-and-monitoring
- **Tools**: yarp, opentelemetry
- **Agents**: `project-operations-specialist`, `workflow-quality-specialist`
- **Actions**:
- Create API Gateway and configure routing.
- Configure distributed tracing, logging, and metrics.
- Implement health checks.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
