---
description: Standard Feature Delivery Cycle (SFDC) for developing new features from
  specifications through to completion.
tags:
- feature
- development
- sdlc
- sfdc
version: 2.0.0
---


# Standard Feature Delivery Cycle (SFDC)

**Version:** 2.0.0

The formal process for developing and delivering new features within the Antigravity Agent Factory.

## Trigger Conditions
- New feature request in Plane or via user prompt.
- Transition from Phase 3 (Architecture) to Phase 4 (Build).

**Trigger Examples:**
- "Build a new agent for sentiment analysis."
- "Implement the user profile feature as described in the PRD."
- "Add a new skill for database migration."
- "Execute the feature development workflow for the 'Payment Integration' ticket."

## Phases

## Phases

### Phase 0: Orientation & Registration
- **Goal**: Establish the memory trail and Plane tracking for the feature.
- **Agents**: `project-operations-specialist`
- **Skills**: managing-plane-tasks, managing-memory
- **Tools**: mcp_memory_open_nodes
- **Actions**:
    - Use `mcp_memory_open_nodes` with `SYS:Consciousness` and `SOP:Feature-Development`.
    - Create the `TASK:[IssueKey]` node and link it to the SOP.
    - Use `managing-plane-tasks` to create a `FEATURE` issue.

### Phase 1: Requirements & Analysis
- **Goal**: Deep understanding of the PRD and technical constraints.
- **Agents**: `project-operations-specialist`
- **Skills**: writing-prd, analyzing-code
- **Tools**: view_file
- **Actions**:
    - Review `knowledge/prd.md` and `knowledge/nfr.md`.

### Phase 2: Implementation & Unit Testing
- **Goal**: Safe and axiomatic code generation following TDD principles.
- **Agents**: `python-ai-specialist`
- **Skills**: developing-ai-agents, developing-ai-agents
- **Tools**: run_command
- **Actions**:
    - Use the appropriate builder agent (e.g., `python-ai-specialist`).
    - Follow the `developing-ai-agents.md` where applicable.

### Phase 3: Integration & System Testing
- **Goal**: Verify the feature works within the larger system architecture.
- **Agents**: `workflow-quality-specialist`
- **Skills**: verifying-artifact-structures, testing-agents
- **Tools**: run_command
- **Actions**:
    - Run integration tests and check for side effects.

### Phase 4: Quality Gate & Documentation
- **Goal**: Generate high-fidelity proof of work and complete project documentation.
- **Agents**: `project-operations-specialist`, `workflow-quality-specialist`
- **Skills**: verifying-artifact-structures, generating-documentation
- **Tools**: walkthrough-generator
- **Actions**:
    - Invoke `/verifying-artifact-structures`.
    - Invoke `/generating-documentation` to generate `walkthrough.md`.

### Phase 5: Deployment & Release
- **Goal**: Rolls out the feature through the CI/CD pipeline.
- **Agents**: `project-operations-specialist`
- **Skills**: committing-releases
- **Tools**: safe_release.py
- **Actions**:
    - Invoke `/committing-releases`.

### Phase 6: Memory Induction & Task Closure
- **Goal**: Persist new patterns and clean up operational state in Plane and Memory.
- **Agents**: `project-operations-specialist`, `knowledge-operations-specialist`
- **Skills**: managing-memory-bank, managing-plane-tasks
- **Tools**: managing-plane-tasks.py, memory_mcp
- **Actions**:
    - Update `KI:` nodes in Memory MCP with any new patterns discovered.
    - Transition the `TASK:` node observations to a final summary.
    - Close the Plane issue via `managing-plane-tasks.py` using the Jinja2 solution template.

## Best Practices
- **Phase Gates**: Never skip a phase without explicit justification in the `walkthrough.md`.
- **Relative Links**: All documented links must use root-relative paths.
- **Evidence First**: Use screenshots/logs in documentation.

## Related
- `sdlc-meta-orchestrator.md`
- `generating-documentation.md`


## Trigger Examples
- "Execute developing-ai-agents.md"
