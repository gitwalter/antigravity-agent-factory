---
name: subagent-driven-development
description: "Execute plan by dispatching specialized subagents per task. Ensures isolated context and high precision."
type: skill
version: 1.0.0
category: execution
agents:
- master-system-orchestrator
- python-ai-specialist
---

# Subagent-Driven Development

## When to Use
Execute an approved plan by dispatching specialized subagents for each task. This ensures isolated context and high precision.

## Prerequisites
- Approved `implementation_plan.md`.
- Specialized agents defined and available.

## Process
The process follows the decomposition of the implementation plan into sub-tasks assigned to agents.

### Core Process
For each task in the approved `implementation_plan.md`:
1.  **Dispatch Implementer**: Provide full task description and specific context (files, KIs).
2.  **Verify RED**: Subagent must provide evidence of a failing test before implementation.
3.  **Execute GREEN**: Subagent implements minimal code to pass the test.
4.  **Verify GREEN**: Subagent provides proof of passing tests.
5.  **Review Loop**:
    - **Spec Review**: Confirm implementation matches requirements exactly.
    - **Quality Review**: Check for idiomatic code, performance, and best practices.
6.  **Refactor & Commit**: Merge the task changes once approved.

## Best Practices
Apply these best practices for efficient subagent coordination.

### Model Selection
- **Mechanical Tasks**: Use fast/cheap models (1-2 files, clear spec).
- **Integration Tasks**: Use standard models (multi-file, pattern matching).
- **Architecture/Design**: Use the most capable models (judgment-heavy).

### Red Flags
- Skipping RED verification.
- Over-building or under-building relative to the spec.
- Mixing context from multiple tasks in a single subagent invocation.
