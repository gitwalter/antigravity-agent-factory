---
description: Systematic workflow for resolving bugs from ticket analysis through implementation
  and verification. This workflow ensures thorough root cause analysis, proper fix
  implementation, and comprehensive testing-agents.
version: 1.1.0
tags:
- bugfix
- resolution
- standardized
---


# Bugfix Resolution

Systematic workflow for resolving bugs from ticket analysis through implementation and verification.

**Agent:** `workflow-quality-specialist`
**Version:** 1.1.0

**Trigger Examples:**
- "Fix the bug in the login flow"
- "Resolve the crash reported in AGENT-134"
- "Investigation of the failing validation tests"

## Trigger Conditions
- Jira, GitHub, GitLab, or Plane issue is mentioned
- User reports a bug or defect
- Error report requires investigation
- Test failure needs resolution

## Steps

### 1. Issue Creation & Ticket Details
- **Goal**: Ensure the bug is tracked in the project management system.
- **Agent**: `project-operations-specialist`
- **Skills**: managing-plane-tasks
- **Actions**:
    - Check if an issue exists in Plane.
    - If not, create an issue using `create_task.py`.
    - Ensure the issue has a `BUG` label and is set to "In Progress".

### 2. Context Engineering (Memory-First)
- **Goal**: Leverage existing knowledge and avoid repeating anti-patterns.
- **Agent**: `project-operations-specialist`
- **Skills**: managing-memory-bank
- **Actions**:
    - Query the Active Consciousness for similar bugs or domain context.
    - Use `mcp_memory_search_nodes` against the Tier 0 Graph.
    - If zero-context is found for a critical domain, use `notify_user` for clarification.

### 3. Root Cause Analysis
- **Goal**: Identify the exact cause and reproduction steps.
- **Agent**: `python-ai-specialist`
- **Actions**:
    - Classify bug severity and impact.
    - Ground the data model and gather relevant code context.
    - Reproduce the bug locally with a minimal script or test.
    - Trace the error origin and identify recent changes in the area.

### 4. Implementation Planning
- **Goal**: Design a verifiable fix.
- **Agent**: `python-ai-specialist`
- **Actions**:
    - Form a hypothesis for the fix.
    - Create a detailed `implementation_plan.md`.
    - Write a regression test that fails before the fix.

### 5. Fix Implementation & Local Verification
- **Goal**: Apply the fix and ensure it solves the reported issue.
- **Agent**: `python-ai-specialist`
- **Actions**:
    - Implement the technical solution.
    - Verify the fix locally using the regression test (Red-Green-Refactor).

### 6. System Quality Gate
- **Goal**: Ensure no regressions and maintain code health.
- **Agent**: `workflow-quality-specialist`
- **Actions**:
    - Run the full test suite using `pytest`.
    - Perform a code review of the changes.

### 7. Documentation & Closure
- **Goal**: Update tracking and persist knowledge.
- **Agent**: `project-operations-specialist`
- **Skills**: managing-plane-tasks, generating-documentation
- **Actions**:
    - Update the status in Plane to 'Done'.
    - Generate `walkthrough.md` via `/generating-documentation`.
    - Close the issue using `managing-plane-tasks.py` to render the solution via Jinja2.
    - Induct new patterns into the memory bank.

## Best Practices
- **Memory First**: Always check memory before starting technical work.
- **Traceability**: All fixes must be tied to a Plane issue.
- **High-Fidelity**: Use Jinja2 templates for all Plane updates.


## Trigger Examples
- "Execute bugfix-resolution.md"


## Related
- [workflow-standard.md](file:///.agent/rules/workflow-standard.md)
