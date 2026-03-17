---
agents:
- workflow-quality-specialist
- project-operations-specialist
- python-ai-specialist
- knowledge-operations-specialist
blueprints:
- universal
description: Antigravity workflow for feature-development. Standardized for IDX Visual
  Editor.
domain: universal
name: feature-development
steps:
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Use `create_task.py` to establish the `FEATURE` issue in Plane.
  - Run `sync_project_context.py` to ensure local UUIDs are current.
  - **Memory Hook**: Call `mcp_memory_open_nodes` for `TASK:[IssueKey]` and `SOP:feature-development`.
  - **Save-on-Discover**: Register missing SOP/SKILL nodes if found in local filesystem.
  agents:
  - project-operations-specialist
  goal: Establish Plane tracking for the feature using standardized scripts.
  name: Orientation & Registration
  skills:
  - managing-plane-tasks
  tools:
  - create_task.py
  - sync_project_context.py
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Review `knowledge/prd.md` and `knowledge/nfr.md`.
  agents:
  - project-operations-specialist
  goal: Deep understanding of the PRD and technical constraints.
  name: Requirements & Analysis
  skills:
  - writing-prd
  - analyzing-code
  tools:
  - view_file
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Use the appropriate builder agent (e.g., `python-ai-specialist`).
  - Follow the `developing-ai-agents.md` where applicable.
  agents:
  - python-ai-specialist
  goal: Safe and axiomatic code generation following TDD principles.
  name: Implementation & Unit Testing
  skills:
  - developing-ai-agents
  - developing-ai-agents
  tools:
  - run_command
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Run integration tests and check for side effects.
  agents:
  - workflow-quality-specialist
  goal: Verify the feature works within the larger system architecture.
  name: Integration & System Testing
  skills:
  - verifying-artifact-structures
  - testing-agents
  tools:
  - run_command
- actions:
  - '**Agents**: `project-operations-specialist`, `workflow-quality-specialist`'
  - '**Actions**:'
  - Invoke `/verifying-artifact-structures`.
  - Invoke `/generating-documentation` to generate `walkthrough.md`.
  agents:
  - project-operations-specialist
  - workflow-quality-specialist
  goal: Generate high-fidelity proof of work and complete project documentation.
  name: Quality Gate & Documentation
  skills:
  - verifying-artifact-structures
  - generating-documentation
  tools:
  - walkthrough-generator
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Invoke `/committing-releases`.
  agents:
  - project-operations-specialist
  goal: Rolls out the feature through the CI/CD pipeline.
  name: Deployment & Release
  skills:
  - committing-releases
  tools:
  - safe_release.py
- actions:
  - '**Agents**: `project-operations-specialist`, `knowledge-operations-specialist`'
  - '**Actions**:'
  - Close the Plane issue via `post_solution.py` using the rendered Jinja2 template.
  - Ensure all architectural decisions and verification proofs are captured in the solution.
  - **Memory Hook**: Synthesize learnings into a `KI:` node and link to the `TASK:`.
  - '**Phase Gates**: Never skip a phase without explicit justification in the `walkthrough.md`.'
  - '**Relative Links**: All documented links must use root-relative paths.'
  - '**Evidence First**: Use screenshots/logs in documentation.'
  - '`sdlc-meta-orchestrator.md`'
  - '`generating-documentation.md`'
  - '"Execute developing-ai-agents.md"'
  agents:
  - project-operations-specialist
  - knowledge-operations-specialist
  goal: Professional task closure and high-fidelity solution delivery in Plane.
  name: Task Closure & Solution Delivery
  skills:
  - managing-plane-tasks
  tools:
  - post_solution.py
  - update_status.py
tags: []
type: sequential
version: 1.0.0
---

# Standard Feature Delivery Cycle (SFDC)

**Version:** 1.0.0

## Overview
Antigravity workflow for standard feature development cycle. Standardized for IDX Visual Editor.

## Trigger Conditions
- New feature request initiated via Plane or stakeholder feedback.
- Requirement for an end-to-end SDLC cycle for a specific system enhancement.
- User request: `/feature-development`.

**Trigger Examples:**
- "Develop the 'Multi-factor Authentication' feature."
- "Implement the new 'Batch Analytics' module according to the PRD."

## Phases

### 1. Orientation & Registration
- **Goal**: Establish Plane tracking for the feature using standardized scripts.
- **Agents**: `project-operations-specialist`
- **Skills**: managing-plane-tasks
- **Tools**: create_task.py, sync_project_context.py
- **Agents**: `project-operations-specialist`
- **Actions**:
- Run `sync_project_context.py` to ensure local UUIDs are current.
- Use `create_task.py` to establish the `FEATURE` issue in Plane.
- **Memory Hook**: Call `mcp_memory_open_nodes` for `TASK:[IssueKey]` and `SOP:feature-development`.
- **Save-on-Discover**: Register missing SOP/SKILL nodes if found in local filesystem.

### 2. Requirements & Analysis
- **Goal**: Deep understanding of the PRD and technical constraints.
- **Agents**: `project-operations-specialist`
- **Skills**: writing-prd, analyzing-code
- **Tools**: view_file
- **Agents**: `project-operations-specialist`
- **Actions**:
- Review `knowledge/prd.md` and `knowledge/nfr.md`.

### 3. Implementation & Unit Testing
- **Goal**: Safe and axiomatic code generation following TDD principles.
- **Agents**: `python-ai-specialist`
- **Skills**: developing-ai-agents, developing-ai-agents
- **Tools**: run_command
- **Agents**: `python-ai-specialist`
- **Actions**:
- Use the appropriate builder agent (e.g., `python-ai-specialist`).
- Follow the `developing-ai-agents.md` where applicable.

### 4. Integration & System Testing
- **Goal**: Verify the feature works within the larger system architecture.
- **Agents**: `workflow-quality-specialist`
- **Skills**: verifying-artifact-structures, testing-agents
- **Tools**: run_command
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Run integration tests and check for side effects.

### 5. Quality Gate & Documentation
- **Goal**: Generate high-fidelity proof of work and complete project documentation.
- **Agents**: `project-operations-specialist`, `workflow-quality-specialist`
- **Skills**: verifying-artifact-structures, generating-documentation
- **Tools**: walkthrough-generator
- **Agents**: `project-operations-specialist`, `workflow-quality-specialist`
- **Actions**:
- Invoke `/verifying-artifact-structures`.
- Invoke `/generating-documentation` to generate `walkthrough.md`.

### 6. Deployment & Release
- **Goal**: Rolls out the feature through the CI/CD pipeline.
- **Agents**: `project-operations-specialist`
- **Skills**: committing-releases
- **Tools**: safe_release.py
- **Agents**: `project-operations-specialist`
- **Actions**:
- Invoke `/committing-releases`.

### 7. Task Closure & Solution Delivery
- **Goal**: Professional task closure and high-fidelity solution delivery in Plane.
- **Agents**: `project-operations-specialist`, `knowledge-operations-specialist`
- **Skills**: managing-plane-tasks
- **Tools**: post_solution.py, update_status.py
- **Agents**: `project-operations-specialist`, `knowledge-operations-specialist`
- **Actions**:
- Close the Plane issue via `post_solution.py` using the rendered Jinja2 template.
- Ensure all architectural decisions and verification proofs are captured in the solution.
- **Memory Hook**: Synthesize learnings into a `KI:` node and link to the `TASK:`.
- **Phase Gates**: Never skip a phase without explicit justification in the `walkthrough.md`.
- **Relative Links**: All documented links must use root-relative paths.
- **Evidence First**: Use screenshots/logs in documentation.
- `sdlc-meta-orchestrator.md`
- `generating-documentation.md`
- "Execute developing-ai-agents.md"
