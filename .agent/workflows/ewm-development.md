---
agents:
- workflow-quality-specialist
- project-operations-specialist
- python-ai-specialist
blueprints:
- universal
description: Antigravity workflow for ewm-development. Standardized for IDX Visual
  Editor.
domain: universal
name: ewm-development
steps:
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Identify warehouse types and movement structures.
  agents:
  - python-ai-specialist
  goal: Define warehouse logic and map entities to EWM structures.
  name: Requirements & Mapping
  skills:
  - guiding-s4-processes
  - analyzing-code
  tools:
  - mcp_memory_search_nodes
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Identify BAPIs or enhancement points.
  agents:
  - python-ai-specialist
  goal: Design the EWM extension or report for warehouse tasks.
  name: Technical Design
  skills:
  - guiding-s4-processes
  tools:
  - mcp_memory_search_nodes
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Implement custom logic and logging-and-monitoring reports.
  agents:
  - python-ai-specialist
  goal: Build the EWM solution in S/4HANA.
  name: Implementation
  skills:
  - guiding-s4-processes
  tools:
  - write_to_file
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Test warehouse tasks and putaway/picking strategies.
  agents:
  - workflow-quality-specialist
  goal: Validate warehouse tasks and movement strategies.
  name: Verification
  skills:
  - verifying-artifact-structures
  tools:
  - run_tests.py
- actions:
  - '**Agents**: `project-operations-specialist`'
  - '**Actions**:'
  - Release transport and update documentation.
  - Is the requirement clear?
  - Are the tests passing?
  - '"Execute this workflow."'
  - '**Axiomatic Alignment**: Ensure Truth, Beauty, and Love.'
  - '**Memory First**: Check context before execution.'
  - '**Verifiability**: Document every step.'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - project-operations-specialist
  goal: Release transport and document EWM changes.
  name: Deployment
  skills:
  - committing-releases
  - generating-documentation
  tools:
  - safe_release.py
tags: []
type: sequential
version: 1.0.0
---

# EWM Development

**Version:** 1.0.0

## Overview
Antigravity workflow for Extended Warehouse Management (EWM) development in S/4HANA. Standardized for IDX Visual Editor.

## Trigger Conditions
- New warehouse process requirement or movement strategy design.
- Need to extend standard EWM functionality via BAPIs or enhancement points.
- User request: `/ewm-development`.

**Trigger Examples:**
- "Design a new putaway strategy for the 'Cold Storage' warehouse."
- "Implement a custom warehouse task report for high-priority shipments."

## Phases

### 1. Requirements & Mapping
- **Goal**: Define warehouse logic and map entities to EWM structures.
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes, analyzing-code
- **Tools**: mcp_memory_search_nodes
- **Agents**: `python-ai-specialist`
- **Actions**:
- Identify warehouse types and movement structures.

### 2. Technical Design
- **Goal**: Design the EWM extension or report for warehouse tasks.
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes
- **Tools**: mcp_memory_search_nodes
- **Agents**: `python-ai-specialist`
- **Actions**:
- Identify BAPIs or enhancement points.

### 3. Implementation
- **Goal**: Build the EWM solution in S/4HANA.
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes
- **Tools**: write_to_file
- **Agents**: `python-ai-specialist`
- **Actions**:
- Implement custom logic and logging-and-monitoring reports.

### 4. Verification
- **Goal**: Validate warehouse tasks and movement strategies.
- **Agents**: `workflow-quality-specialist`
- **Skills**: verifying-artifact-structures
- **Tools**: run_tests.py
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Test warehouse tasks and putaway/picking strategies.

### 5. Deployment
- **Goal**: Release transport and document EWM changes.
- **Agents**: `project-operations-specialist`
- **Skills**: committing-releases, generating-documentation
- **Tools**: safe_release.py
- **Agents**: `project-operations-specialist`
- **Actions**:
- Release transport and update documentation.
- Is the requirement clear?
- Are the tests passing?
- "Execute this workflow."
- **Axiomatic Alignment**: Ensure Truth, Beauty, and Love.
- **Memory First**: Check context before execution.
- **Verifiability**: Document every step.
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
