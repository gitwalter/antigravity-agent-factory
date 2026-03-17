---
agents:
- workflow-quality-specialist
- system-architecture-specialist
- project-operations-specialist
- knowledge-operations-specialist
blueprints:
- universal
description: Antigravity workflow for antigravity-factory-building. Standardized for
  IDX Visual Editor.
domain: universal
name: antigravity-factory-building
steps:
- actions:
  - '**Agents**: `system-architecture-specialist`'
  - '**Actions**:'
  - Generate prototype brief and obtain human approval.
  agents:
  - system-architecture-specialist
  goal: Convert a raw idea or pain point into a formal, human-approved prototype brief.
  name: Ideation & Prototype Brief
  skills:
  - brainstorming-ideas
  - briefing-prototypes
  tools:
  - mcp_memory_search_nodes
- actions:
  - '**Agents**: `system-architecture-specialist`, `project-operations-specialist`'
  - '**Actions**:'
  - Write PRD and create issues in Plane.
  agents:
  - system-architecture-specialist
  - project-operations-specialist
  goal: Formalize the approved brief into a PRD and manageable issues in Plane.
  name: Requirements & Issue Formalization
  skills:
  - writing-prd
  - managing-plane-tasks
  tools:
  - mcp_plane_create_issue
- actions:
  - '**Agents**: `system-architecture-specialist`'
  - '**Actions**:'
  - Create implementation plans and map architectural nodes in Memory.
  agents:
  - system-architecture-specialist
  goal: Design the technical implementation and update the system knowledge graph.
  name: Architecture & Memory Mapping
  skills:
  - designing-ai-systems
  - repository-maintenance
  tools:
  - mcp_memory_create_relations
  - mcp_memory_create_entities
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Implement workflows, skills, and knowledge files.
  agents:
  - project-operations-specialist
  goal: Execute the build of workflows, skills, and knowledge items following TDD.
  name: Build & Implementation
  skills:
  - developing-ai-agents
  - developing-ai-agents
  tools:
  - write_to_file
  - pytest-cli
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Run unit and integration tests to validate integrity.
  agents:
  - workflow-quality-specialist
  goal: Validate the systemic integrity of the implementation through comprehensive
    testing-agents.
  name: Verification & Evaluation
  skills:
  - testing-agents
  - testing-agents
  tools:
  - pytest-cli
  - evaluate-agent
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Finalize git commit and tag the release.
  agents:
  - project-operations-specialist
  goal: Commit tested implementation and execute a formalized release.
  name: Deployment & Release
  skills:
  - committing-releases
  - committing-releases
  tools:
  - git-cli
- actions:
  - '**Agents**: `knowledge-operations-specialist`, `project-operations-specialist`'
  - '**Actions**:'
  - Sync insights to Plane and close the task loop.
  - Triggered by user context or meta-orchestrator.
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - knowledge-operations-specialist
  - project-operations-specialist
  goal: Synchronize architectural insights to Plane and finalize the development loop.
  name: Monitor & Closure
  skills:
  - generating-documentation
  - managing-plane-tasks
  tools:
  - managing-plane-tasks.py
tags: []
type: sequential
version: 2.0.0
---
# Antigravity Factory System Building Process

**Version:** 1.0.0

## Overview
This workflow governs the full lifecycle of building AI systems within the Antigravity Agent Factory, from initial ideation and prototype briefing to formal PRD creation, implementation, and verified release.

## Trigger Conditions
- User requests a new AI system or feature.
- Meta-orchestrator identifies a gap in the system architecture.

**Trigger Examples:**
- "Build a new agent for data processing."
- "Execute the factory building process for a new prototype."

## Phases

### 1. Ideation & Prototype Brief
- **Goal**: Convert a raw idea or pain point into a formal, human-approved prototype brief.
- **Agents**: `system-architecture-specialist`
- **Skills**: brainstorming-ideas, briefing-prototypes
- **Tools**: mcp_memory_search_nodes
- **Agents**: `system-architecture-specialist`
- **Actions**:
- Generate prototype brief and obtain human approval.

### 2. Requirements & Issue Formalization
- **Goal**: Formalize the approved brief into a PRD and manageable issues in Plane.
- **Agents**: `system-architecture-specialist`, `project-operations-specialist`
- **Skills**: writing-prd, managing-plane-tasks
- **Tools**: mcp_plane_create_issue
- **Agents**: `system-architecture-specialist`, `project-operations-specialist`
- **Actions**:
- Write PRD and create issues in Plane.

### 3. Architecture & Memory Mapping
- **Goal**: Design the technical implementation and update the system knowledge graph.
- **Agents**: `system-architecture-specialist`
- **Skills**: designing-ai-systems, repository-maintenance
- **Tools**: mcp_memory_create_relations, mcp_memory_create_entities
- **Agents**: `system-architecture-specialist`
- **Actions**:
- Create implementation plans and map architectural nodes in Memory.

### 4. Build & Implementation
- **Goal**: Execute the build of workflows, skills, and knowledge items following TDD.
- **Agents**: `project-operations-specialist`
- **Skills**: developing-ai-agents, developing-ai-agents
- **Tools**: write_to_file, pytest-cli
- **Agents**: `project-operations-specialist`
- **Actions**:
- Implement workflows, skills, and knowledge files.
- **Root Cleanliness**: Ensure all scratch scripts used during implementation are stored in `tmp/` and cleaned up.

### 5. Verification & Evaluation
- **Goal**: Validate the systemic integrity of the implementation through comprehensive testing-agents.
- **Agents**: `workflow-quality-specialist`
- **Skills**: testing-agents, testing-agents
- **Tools**: pytest-cli, evaluate-agent
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Run unit and integration tests to validate integrity.

### 6. Deployment & Release
- **Goal**: Commit tested implementation and execute a formalized release.
- **Agents**: `project-operations-specialist`
- **Skills**: committing-releases, committing-releases
- **Tools**: git-cli
- **Agents**: `project-operations-specialist`
- **Actions**:
- Finalize git commit and tag the release.

### 7. Monitor & Closure
- **Goal**: Synchronize architectural insights to Plane and finalize the development loop.
- **Agents**: `knowledge-operations-specialist`, `project-operations-specialist`
- **Skills**: generating-documentation, managing-plane-tasks
- **Tools**: managing-plane-tasks.py
- **Agents**: `knowledge-operations-specialist`, `project-operations-specialist`
- **Actions**:
- Sync insights to Plane and close the task loop.
- Triggered by user context or meta-orchestrator.
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
