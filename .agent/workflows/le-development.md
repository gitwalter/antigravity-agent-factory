---
agents:
- workflow-quality-specialist
- project-operations-specialist
- python-ai-specialist
blueprints:
- universal
description: Antigravity workflow for le-development. Standardized for IDX Visual
  Editor.
domain: universal
name: le-development
steps:
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Map requirements to `LIKP` and `LIPS` tables.
  agents:
  - python-ai-specialist
  goal: Define shipping and delivery requirements and identify LE tables.
  name: Requirement Analysis
  skills:
  - guiding-s4-processes
  - analyzing-code
  tools:
  - mcp_memory_search_nodes
- actions:
  - '**Agents**: `python-ai-specialist`'
  - '**Actions**:'
  - Identify enhancement points and design the logic.
  agents:
  - python-ai-specialist
  goal: Design the technical solution for shipping determination or delivery extensions.
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
  goal: Implement the LE solution using ABAP.
  name: Implementation
  skills:
  - guiding-s4-processes
  tools:
  - write_to_file
- actions:
  - '**Agents**: `workflow-quality-specialist`'
  - '**Actions**:'
  - Test LE scenarios and status tracking.
  agents:
  - workflow-quality-specialist
  goal: Validate delivery processing and shipping point determination.
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
  goal: Release transport and document LE changes.
  name: Deployment
  skills:
  - committing-releases
  - generating-documentation
  tools:
  - safe_release.py
tags: []
type: sequential
version: 2.0.0
---
# Logistics Execution (LE) Development

**Version:** 1.0.0

## Overview
Antigravity workflow for SAP Logistics Execution (LE) development in S/4HANA. Standardized for IDX Visual Editor.

## Trigger Conditions
- Business requirement for shipping, delivery, or transportation modifications.
- Need to implement logic related to delivery processing or shipping point determination.
- User request: `/le-development`.

**Trigger Examples:**
- "Implement a custom logic for determining the shipping point for international orders."
- "Extend the delivery document with custom fields for tracking high-value shipments."

## Phases

### 1. Requirement Analysis
- **Goal**: Define shipping and delivery requirements and identify LE tables.
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes, analyzing-code
- **Tools**: mcp_memory_search_nodes
- **Agents**: `python-ai-specialist`
- **Actions**:
- Map requirements to `LIKP` and `LIPS` tables.

### 2. Technical Design
- **Goal**: Design the technical solution for shipping determination or delivery extensions.
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes
- **Tools**: mcp_memory_search_nodes
- **Agents**: `python-ai-specialist`
- **Actions**:
- Identify enhancement points and design the logic.

### 3. Implementation
- **Goal**: Implement the LE solution using ABAP.
- **Agents**: `python-ai-specialist`
- **Skills**: guiding-s4-processes
- **Tools**: write_to_file
- **Agents**: `python-ai-specialist`
- **Actions**:
- Implement custom logic and logging-and-monitoring reports.

### 4. Verification
- **Goal**: Validate delivery processing and shipping point determination.
- **Agents**: `workflow-quality-specialist`
- **Skills**: verifying-artifact-structures
- **Tools**: run_tests.py
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Test LE scenarios and status tracking.

### 5. Deployment
- **Goal**: Release transport and document LE changes.
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
