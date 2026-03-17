---
agents:
- workflow-quality-specialist
- project-operations-specialist
- python-ai-specialist
blueprints:
- universal
description: Antigravity workflow for bugfix-resolution. Standardized for IDX Visual
  Editor.
domain: universal
name: bugfix-resolution
steps:
- actions:
  - 'Actions:'
  - Check if an issue exists in Plane.
  - If not, create an issue using `create_task.py`.
  - Ensure the issue has a `BUG` label and is set to "In Progress".
  - Memory Hook: Call `mcp_memory_open_nodes` for `TASK:[IssueKey]` and `SOP:bugfix-resolution`.
  - Save-on-Discover: Register missing SOP/SKILL nodes if found in local filesystem.
  agents:
  - project-operations-specialist
  goal: Ensure the bug is tracked in the project management system.
  name: Issue Creation & Ticket Details
  skills:
  - managing-plane-tasks
  tools: []
- actions:
  - 'Actions:'
  - Query the Active Consciousness for similar bugs or domain context.
  - Use `mcp_memory_search_nodes` against the Tier 0 Graph.
  - If zero-context is found for a critical domain, use `notify_user` for clarification.
  agents:
  - project-operations-specialist
  goal: Leverage existing knowledge and avoid repeating anti-patterns.
  name: Context Engineering (Memory-First)
  skills:
  - managing-memory-bank
  tools: []
- actions:
  - 'Actions:'
  - Classify bug severity and impact.
  - Ground the data model and gather relevant code context.
  - Reproduce the bug locally with a minimal script or test.
  - Trace the error origin and identify recent changes in the area.
  agents:
  - python-ai-specialist
  goal: Identify the exact cause and reproduction steps.
  name: Root Cause Analysis
  skills: []
  tools: []
- actions:
  - 'Actions:'
  - Form a hypothesis for the fix.
  - Create a detailed `implementation_plan.md`.
  - Write a regression test that fails before the fix.
  agents:
  - python-ai-specialist
  goal: Design a verifiable fix.
  name: Implementation Planning
  skills: []
  tools: []
- actions:
  - 'Actions:'
  - Implement the technical solution.
  - Verify the fix locally using the regression test (Red-Green-Refactor).
  agents:
  - python-ai-specialist
  goal: Apply the fix and ensure it solves the reported issue.
  name: Fix Implementation & Local Verification
  skills: []
  tools: []
- actions:
  - 'Actions:'
  - Run the full test suite using `pytest`.
  - Perform a code review of the changes.
  agents:
  - workflow-quality-specialist
  goal: Ensure no regressions and maintain code health.
  name: System Quality Gate
  skills: []
  tools: []
- actions:
  - 'Actions:'
  - Update the status in Plane to 'Done'.
  - Generate `walkthrough.md` via `/generating-documentation`.
  - Close the issue using `managing-plane-tasks.py` to render the solution via Jinja2.
  - Induct new patterns into the memory bank.
  - Memory Hook: Synthesize fix into a `KI:` node and link to the `TASK:`.
  - 'Memory First: Always check memory before starting technical work.'
  - 'Traceability: All fixes must be tied to a Plane issue.'
  - 'High-Fidelity: Use Jinja2 templates for all Plane updates.'
  - '"Execute bugfix-resolution.md"'
  - '[workflow-standard.md](file:///.agent/rules/workflow-standard.md)'
  agents:
  - project-operations-specialist
  goal: Update tracking and persist knowledge.
  name: Documentation & Closure
  skills:
  - managing-plane-tasks
  - generating-documentation
  tools: []
tags: []
type: sequential
version: 2.0.0
---
# Bugfix Resolution

**Version:** 1.0.0

## Overview
Antigravity workflow for bugfix-resolution. Standardized for IDX Visual Editor.

## Trigger Conditions
- Bug identified and reported in Plane.
- Regression detected in CI/CD pipeline.
- User request: `/bugfix-resolution`.

**Trigger Examples:**
- "Fix the bug reported in AGENT-123."
- "Resolve the failed test in `test_core.py`."

## Phases

### 1. Issue Creation & Ticket Details
- **Goal**: Ensure the bug is tracked in the project management system.
- **Agents**: `project-operations-specialist`
- **Skills**: managing-plane-tasks
- **Actions**:
- Check if an issue exists in Plane.
- If not, create an issue using `create_task.py`.
- Ensure the issue has a `BUG` label and is set to "In Progress".
- **Memory Hook**: Call `mcp_memory_open_nodes` for `TASK:[IssueKey]` and `SOP:bugfix-resolution`.
- **Save-on-Discover**: Register missing SOP/SKILL nodes if found in local filesystem.

### 2. Context Engineering (Memory-First)
- **Goal**: Leverage existing knowledge and avoid repeating anti-patterns.
- **Agents**: `project-operations-specialist`
- **Skills**: managing-memory-bank
- **Actions**:
- Query the Active Consciousness for similar bugs or domain context.
- Use `mcp_memory_search_nodes` against the Tier 0 Graph.
- If zero-context is found for a critical domain, use `notify_user` for clarification.

### 3. Root Cause Analysis
- **Goal**: Identify the exact cause and reproduction steps.
- **Agents**: `python-ai-specialist`
- **Actions**:
- Classify bug severity and impact.
- Ground the data model and gather relevant code context.
- Reproduce the bug locally with a minimal script or test.
- Trace the error origin and identify recent changes in the area.

### 4. Implementation Planning
- **Goal**: Design a verifiable fix.
- **Agents**: `python-ai-specialist`
- **Actions**:
- Form a hypothesis for the fix.
- Create a detailed `implementation_plan.md`.
- Write a regression test that fails before the fix.

### 5. Fix Implementation & Local Verification
- **Goal**: Apply the fix and ensure it solves the reported issue.
- **Agents**: `python-ai-specialist`
- **Actions**:
- Implement the technical solution.
- Verify the fix locally using the regression test (Red-Green-Refactor).

### 6. System Quality Gate
- **Goal**: Ensure no regressions and maintain code health.
- **Agents**: `workflow-quality-specialist`
- **Actions**:
- Run the full test suite using `pytest`.
- Perform a code review of the changes.

### 7. Documentation & Closure
- **Goal**: Update tracking and persist knowledge.
- **Agents**: `project-operations-specialist`
- **Skills**: managing-plane-tasks, generating-documentation
- **Actions**:
- Update the status in Plane to 'Done'.
- Generate `walkthrough.md` via `/generating-documentation`.
- Close the issue using `managing-plane-tasks.py` to render the solution via Jinja2.
- Induct new patterns into the memory bank.
- **Memory Hook**: Synthesize fix into a `KI:` node and link to the `TASK:`.
- **Memory First**: Always check memory before starting technical work.
- **Traceability**: All fixes must be tied to a Plane issue.
- **High-Fidelity**: Use Jinja2 templates for all Plane updates.
- "Execute bugfix-resolution.md"
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
