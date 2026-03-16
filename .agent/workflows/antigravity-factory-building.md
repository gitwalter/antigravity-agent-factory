---
description: Workflow for designing, building, and structuring the antigravity-factory
  system itself using SDLC phases.
agents:
- system-architecture-specialist
- template-creator
version: 1.0.0
tags:
- antigravity
- factory
- building
- standardized
---


# Antigravity Factory System Building Process

**Version:** 1.0.0


This is the meta-workflow for building out the antigravity-agent-factory. It strictly follows the 7-Phase AI SDLC Process to convert abstract ideas into formal systemic capabilities.

## Phases

### Phase 1: Ideation & Prototype Brief
- **Goal**: Convert a raw idea or pain point into a formal, human-approved prototype brief.
- **Agents**: `system-architecture-specialist`
- **Skills**: brainstorming-ideas, briefing-prototypes
- **Tools**: mcp_memory_search_nodes
- **Actions**:
    - Generate prototype brief and obtain human approval.

### Phase 2: Requirements & Issue Formalization
- **Goal**: Formalize the approved brief into a PRD and manageable issues in Plane.
- **Agents**: `system-architecture-specialist`, `project-operations-specialist`
- **Skills**: writing-prd, managing-plane-tasks
- **Tools**: mcp_plane_create_issue
- **Actions**:
    - Write PRD and create issues in Plane.

### Phase 3: Architecture & Memory Mapping
- **Goal**: Design the technical implementation and update the system knowledge graph.
- **Agents**: `system-architecture-specialist`
- **Skills**: designing-ai-systems, repository-maintenance
- **Tools**: mcp_memory_create_relations, mcp_memory_create_entities
- **Actions**:
    - Create implementation plans and map architectural nodes in Memory.

### Phase 4: Build & Implementation
- **Goal**: Execute the build of workflows, skills, and knowledge items following TDD.
- **Agents**: `project-operations-specialist`
- **Skills**: developing-ai-agents, developing-ai-agents
- **Tools**: write_to_file, pytest-cli
- **Actions**:
    - Implement workflows, skills, and knowledge files.

### Phase 5: Verification & Evaluation
- **Goal**: Validate the systemic integrity of the implementation through comprehensive testing-agents.
- **Agents**: `workflow-quality-specialist`
- **Skills**: testing-agents, testing-agents
- **Tools**: pytest-cli, evaluate-agent
- **Actions**:
    - Run unit and integration tests to validate integrity.

### Phase 6: Deployment & Release
- **Goal**: Commit tested implementation and execute a formalized release.
- **Agents**: `project-operations-specialist`
- **Skills**: committing-releases, committing-releases
- **Tools**: git-cli
- **Actions**:
    - Finalize git commit and tag the release.

### Phase 7: Monitor & Closure
- **Goal**: Synchronize architectural insights to Plane and finalize the development loop.
- **Agents**: `knowledge-operations-specialist`, `project-operations-specialist`
- **Skills**: generating-documentation, managing-plane-tasks
- **Tools**: managing-plane-tasks.py
- **Actions**:
    - Sync insights to Plane and close the task loop.

## Systematic Structuring & Hierarchical Cataloging
When adding new workflows, agents, or skills:
1. Define the component's strict inputs and outputs.
2. Register the component within the appropriate SDLC phase folder or tagging structure.
3. Update the overarching Knowledge Graph via MCP Memory to establish semantic ties (e.g. `Workflow X uses Agent Y uses Skill Z`).


## Trigger Conditions
- Triggered by user context or meta-orchestrator.


## Trigger Examples:
- "Execute this workflow."


## Best Practices
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.


## Related
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
